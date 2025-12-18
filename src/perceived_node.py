from __future__ import annotations
import time
import threading
from flexstack.utils.time_service import TimeService
from flexstack.facilities.local_dynamic_map.ldm_classes import RequestDataObjectsResp
from flexstack.facilities.ca_basic_service.cam_transmission_management import GenerationDeltaTime

class PerceivedNode:
    sation_id: int
    last_update_ts_millis: int
    latitude: float
    longitude: float
    station_type: int
    heading: float
    speed: float
    ego: bool = False

    def __init__(self, station_id: int, last_update_ts_millis: int, latitude: float, longitude: float, station_type: int, heading: float, speed: float):
        self.station_id = station_id
        self.last_update_ts_millis = last_update_ts_millis
        self.latitude = latitude
        self.longitude = longitude
        self.station_type = station_type
        self.heading = heading
        self.speed = speed
        self.ego = False

    def mark_as_ego(self):
        self.ego = True

    def update(self, last_update_ts_millis: int, latitude: float, longitude: float, station_type: int, heading: float, speed: float):
        self.last_update_ts_millis = last_update_ts_millis
        self.latitude = latitude
        self.longitude = longitude
        self.station_type = station_type
        self.heading = heading
        self.speed = speed

    def is_active(self) -> bool:
        # Consider a node active if updated within the last 5 seconds
        current_ts_millis = int(TimeService.time() * 1000)
        return (current_ts_millis - self.last_update_ts_millis) < 5000

    def to_dict(self) -> dict:
        return {
            "station_id": self.station_id,
            "last_update_ts_millis": self.last_update_ts_millis,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "station_type": self.station_type,
            "heading": self.heading,
            "speed": self.speed,
            "ego": self.ego
        }


class PerceivedNodes:
    nodes: dict[int, PerceivedNode]
    lock: threading.Lock = threading.Lock()
    event: threading.Event = threading.Event()

    def __init__(self, ego_station_id: int):
        self.nodes = {}
        self.nodes[ego_station_id] = PerceivedNode(
                    ego_station_id, int(TimeService.time() * 1000), 0.0, 0.0, 0, 0.0, 0.0)
        self.nodes[ego_station_id].mark_as_ego()
        self.lock = threading.Lock()
        self.event = threading.Event()
        self.gc_thread = threading.Thread(
            target=self.garbage_collector_thread_func, daemon=True)
        self.gc_thread.start()

    def update_node(self, station_id: int, last_update_ts_millis: int, latitude: float, longitude: float, station_type: int, heading: float, speed: float):
        if station_id in self.nodes:
            with self.lock:
                self.nodes[station_id].update(
                    last_update_ts_millis, latitude, longitude, station_type, heading, speed)
        else:
            with self.lock:
                self.nodes[station_id] = PerceivedNode(
                    station_id, last_update_ts_millis, latitude, longitude, station_type, heading, speed)

    def mark_node_as_ego(self, station_id: int):
        if station_id in self.nodes:
            with self.lock:
                self.nodes[station_id].mark_as_ego()

    def get_active_nodes(self) -> list[PerceivedNode]:
        with self.lock:
            return [node for node in self.nodes.values() if node.is_active()]

    def get_active_nodes_dicts(self) -> list[dict]:
        with self.lock:
            return [node.to_dict() for node in self.nodes.values() if node.is_active()]

    def garbage_collector_thread_func(self):
        while not self.event.is_set():
            time.sleep(10)  # Run every 10 seconds
            with self.lock:
                inactive_nodes = [station_id for station_id, node in self.nodes.items(
                ) if not node.is_active() and not node.ego]
                for station_id in inactive_nodes:
                    del self.nodes[station_id]

    def vam_ldm_subscription_callback(self, data: RequestDataObjectsResp) -> None:
        for obj in data.data_objects:
            try:
                vam = obj["dataObject"]
                gen_delta_time = GenerationDeltaTime(
                    msec=vam["vam"]["generationDeltaTime"])
                
                self.update_node(
                    station_id=vam["header"]["stationId"],
                    last_update_ts_millis=int(gen_delta_time.as_timestamp_in_certain_point(int(TimeService.time() * 1000))),
                    latitude=vam["vam"]["vamParameters"]["basicContainer"]["referencePosition"]["latitude"] / 10**7,
                    longitude=vam["vam"]["vamParameters"]["basicContainer"]["referencePosition"]["longitude"] / 10**7,
                    station_type=vam["vam"]["vamParameters"]["basicContainer"]["stationType"],
                    heading=vam["vam"]["vamParameters"]["vruHighFrequencyContainer"]["heading"]["value"] / 10,
                    speed=vam["vam"]["vamParameters"]["vruHighFrequencyContainer"]["speed"]["speedValue"] / 100
                )
            except Exception as e:
                print(f"Error processing VAM data: {e}")
                continue

    def cam_ldm_subscription_callback(self, data: RequestDataObjectsResp) -> None:
        for obj in data.data_objects:
            try:
                cam = obj["dataObject"]
                gen_delta_time = GenerationDeltaTime(
                    msec=cam["cam"]["generationDeltaTime"])
                self.update_node(
                    station_id=cam["header"]["stationId"],
                    last_update_ts_millis=int(gen_delta_time.as_timestamp_in_certain_point(int(TimeService.time() * 1000))),
                    latitude=cam["cam"]["camParameters"]["basicContainer"]["referencePosition"]["latitude"] / 10**7,
                    longitude=cam["cam"]["camParameters"]["basicContainer"]["referencePosition"]["longitude"] / 10**7,
                    station_type=cam["cam"]["camParameters"]["basicContainer"]["stationType"],
                    heading=cam["cam"]["camParameters"]["highFrequencyContainer"][1]["heading"]["headingValue"] / 10,
                    speed=cam["cam"]["camParameters"]["highFrequencyContainer"][1]["speed"]["speedValue"] / 100
                )
            except Exception as e:
                print(f"Error processing CAM data: {e}")
                continue
