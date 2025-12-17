# FlexStack UI Example Application

<!--<img src="doc/img/logo.png" alt="V2X Flex Stack" width="200"/>--> <img src="https://raw.githubusercontent.com/Fundacio-i2CAT/FlexStack/refs/heads/master/doc/img/i2cat_logo.png" alt="i2CAT Logo" width="200"/>

# Short description

The FlexStack UI is a web-based application that provides a user-friendly interface for visualizing V2X (Vehicle-to-Everything) communications. It allows users to monitor real-time updates, coming from Coopeative Awareness Messages (CAMs) and VRU Awareness Messages (VAMs).


# Pre-requisites

## Supported Operating Systems

This application works on Linux-based operating systems.
It requires Python 3.8 or higher.
Must be run with root privileges to access the network interfaces in promiscuous mode.
Before running calling `sudo su` is recommended.


## Dependencies

All dependecies can be found in the `requirements.txt` file. To install them, run the following command:

```
pip install -r requirements.txt
```

A **Python virtual environment** is recommended to avoid conflicts with other Python packages installed in the system.


## Usage

The application can be started by running the following command:

```
python src/flexstack_ui.py
```

By default, the application will start a web server on `http://localhost:5000`. You can access the web interface by opening a web browser and navigating to this URL. And it will start sending CAM messages through the `lo` interface.

The behaviour of the application can be customized changing the following environment variables:

| Environment Variable                     | Description                                                                                     |
|------------------------------------------|-------------------------------------------------------------------------------------------------|
| `GPSD_HOST`                             | Hostname for the GPSD service (default: `localhost`).                                         |
| `GPSD_PORT`                             | Port number for the GPSD service (default: `2947`).                                           |
| `SEND_CAMS`                             | Flag to enable sending CAM messages (default: `True`).                                        |
| `SEND_VAMS`                             | Flag to enable sending VAM messages (default: `False`).                                       |
| `V2X_INTERFACE`                         | Network interface for V2X communication (default: `lo`).                                      |
| `HTTP_SERVER_PORT`                      | Port number for the HTTP server (default: `5000`).                                            |
| `HTTP_SERVER_ACCEPTED_ADDRESSES`       | Accepted addresses for the HTTP server (default: `0.0.0.0`).                                   |

## Developers

- Jordi Marias-i-Parella (jordi.marias@i2cat.net)
- Daniel Ulied Guevara (daniel.ulied@i2cat.net)
- Adrià Pons Serra (adria.pons@i2cat.net)
- Marc Codina Bartumeus (marc.codina@i2cat.net)
- Lluc Feixa Morancho (lluc.feixa@i2cat.net)

# Source

This code can be considered an appendix to the V2X Flexstack library, which can be found at:

[FlexStack Library](https://github.com/Fundacio-i2CAT/FlexStack) - Official repository

Visit [flexstack.eu](https://flexstack.eu) for more information.

# Copyright

This code has been developed by Fundació Privada Internet i Innovació Digital a Catalunya (i2CAT).

FlexStack is a registered trademark of i2CAT. Unauthorized use is strictly prohibited.

i2CAT is a **non-profit research and innovation centre that** promotes mission-driven knowledge to solve business challenges, co-create solutions with a transformative impact, empower citizens through open and participative digital social innovation with territorial capillarity, and promote pioneering and strategic initiatives. i2CAT **aims to transfer** research project results to private companies in order to create social and economic impact via the out-licensing of intellectual property and the creation of spin-offs. Find more information of i2CAT projects and IP rights at https://i2cat.net/tech-transfer/

# License

This code is licensed under the terms of the AGPL. Information about the license can be located at https://www.gnu.org/licenses/agpl-3.0.html.

Please, refer to FlexStack Community Edition as a dependence of your works.

If you find that this license doesn't fit with your requirements regarding the use, distribution or redistribution of our code for your specific work, please, don’t hesitate to contact the intellectual property managers in i2CAT at the following address: techtransfer@i2cat.net Also, in the following page you’ll find more information about the current commercialization status or other licensees: Under Development.

# Attributions

Attributions of Third Party Components of this work:

- `v2xflexstack` Version 0.10.8 - Imported python library - https://pypi.org/project/v2xflexstack/ - AGPL-3.0 license
- `Flask` Version 3.1.2 - Imported python library - https://palletsprojects.com/p/flask/ - BSD-3-Clause license