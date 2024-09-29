# DSO138_mini_Data_Extractor
Made for ```DSO 138 mini oscilloscope```. Parameters and Plot data will saved in two separate JSON files named ```<FILENAME>_param.json & <FILENAME>_data.json```. return oci_paramerters and plot_data dictionary and a list respectively.

##  Requirements
* UART Adapter and 3 jumper wires for Connection
* Windows or Linux PC

##  Setup
*  Power up the device first.
*  connect to the Serial Connection
*  ```(PC) TXD -> RXD (HOST)```,
*  ```(PC) RXD -> TXD (HOST)```,
*  ```(PC) GND -> GND (HOST)```

## Run the Script in your work folder
*  Usage: ```python DSO138mini.py -h ``` or ``` python DSO138mini.py --help ``` for help
*  Usage: ```python DSO138mini.py <COM> <BAUDRATE> <FILENAME> ```
*  Example: ``` python DSO138mini.py COM9 115200 square_wave```
*  You will prompt that ```Waiting for data``` if the connection is success
*  Just hold down the SEL button for 3s. 
