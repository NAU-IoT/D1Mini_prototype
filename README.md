Repository for a D1Mini pro prototype for the Northern Arizona University Internet of Things (IoT) lab.

Authors
[Akiel Aries](https://www.github.com/aba275)


# Introduction
This repository contains code that transmits values read
from a BME280 and published them via MQTT to an Instance of
InfluxDB hosted on an RPI 4 with additional peripherals to be added.

#### D1Mini_proto
##### *(MQTT publish code currently decoupled from main())*
Folder contains a rough sketch on sending values read
from the BME280 and publishing the data through the ESP
module located on the D1 mini dev board via MQTT. The
data is then sent into an instance of InfluxDB hosted on
a Raspberry Pi 4.

#### MQTT
Folder contains rough sketch of how values will be
transmitted from the host microcontroller(D1 Mini Pro)
to the raspberry pi that will store these values.


#### Schematic 
![CIP_schematic_v0 with KiCad](https://github.com/NAU-IoT/CIP_prod/blob/main/img/KICAD_CIP_SCHEMATIC_V0.png)

# Dependencies
#### *Todo*

# Build
*Explain how to build this project. Want this to be
executed with running docker only*

Clone the repository and build from the Dockerimage:

    $ cd climate_indicator_proj
    $ docker build --rm -t climate_indicator_proj .
*Todo:*


# How to Contribute to this project...
#### *Todo:*
