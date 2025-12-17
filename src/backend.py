import os
import threading
from flask import Flask, jsonify, send_file
from perceived_node import PerceivedNodes


class Backend:
    """Flask server backend that serves the UI and provides node position data."""

    def __init__(self, perceived_nodes: PerceivedNodes, host: str = "0.0.0.0", port: int = 5000):
        """
        Initialize the Backend server.

        Args:
            perceived_nodes: PerceivedNodes instance to get node positions from.
            host: Host address to bind the server to.
            port: Port number to bind the server to.
        """
        self.perceived_nodes = perceived_nodes
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self._setup_routes()
        self._server_thread = None

    def _setup_routes(self):
        """Set up Flask routes."""
        
        @self.app.route("/")
        def index():
            """Serve the index.html file."""
            html_path = os.path.join(os.path.dirname(__file__), "index.html")
            return send_file(html_path)

        @self.app.route("/positions")
        def positions():
            """Return JSON of active nodes positions."""
            return jsonify(self.perceived_nodes.get_active_nodes_dicts())
        
        @self.app.route("/i2cat_logo.png")
        def serve_logo():
            """Serve the i2cat_logo.png file."""
            logo_path = os.path.join(os.path.dirname(__file__), "i2cat_logo.png")
            return send_file(logo_path)

    def run(self, threaded: bool = False):
        """
        Run the Flask server.

        Args:
            threaded: If True, run the server in a background thread.
        """
        if threaded:
            self._server_thread = threading.Thread(
                target=self._run_server,
                daemon=True
            )
            self._server_thread.start()
        else:
            self._run_server()

    def _run_server(self):
        """Internal method to start the Flask server."""
        self.app.run(host=self.host, port=self.port, debug=False, use_reloader=False)


if __name__ == "__main__":
    # Example usage for testing
    perceived_nodes = PerceivedNodes()
    backend = Backend(perceived_nodes, host="0.0.0.0", port=5000)
    backend.run()
