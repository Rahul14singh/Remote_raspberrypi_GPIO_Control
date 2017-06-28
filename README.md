# Remote_raspberrypi_GPIO_control

This code is specially written for Raspberry Pi 3 Model B. But can be customised for any raspberry pi model by changing the GPIO pin configurations used in the code according to the model of Pi you are using.

## Usage:

GUI based application which is built to remotely control or access the GPIO Pins of a Raspberry Pi. This could be used as a base for developing very good and massive applications and live projects.

Pyinstaller can be used to make an executable file of the application and then can be used on any system without any Python or it's supporting libraries.

## Requirements:

1. Python 3 or later 
2. PyQt5 installed " pip3 install PyQt5 " command on cmd to install library
3. Paramiko installed " pip3 install paramiko " command on cmd to install library
4. A weaved or remote3.it accounts it's free for a limited number of devices control and can be made from the given link below.
5. Some other necessary supporting libraries.

Install  [Python](https://www.python.org/downloads/) . Do install Python3 or later.

if facing difficulty in installing libraries here is the link for the HELP:

1. [PyQt5](https://pypi.python.org/pypi/PyQt5)

2. [Paramiko](http://www.paramiko.org/)

3. [WEAVED](https://www.remot3.it/web/)

> Do change the Image URLs given in the code for a Window Icon and a Background Image for the GUI application.

> Do replace the userName and password of the weaved account that you made if you want to set some default login account i.e want to login from same account every time without entering it everytime in the GUI or else can manually enter the details once you run the application in the GUI and can change login account there. 

## Instructions and Setup Environment:

- The GPIO Pins of the Raspberry Pi will be controlled remotely via the Internet with the help of a GUI application.
- Your Device running the GUI application named "control_gpio_GUI.py" must be connected to the Internet.
- Your Raspberry should also be connected to the Internet.
- Raspberry Pi should be properly configured as per the Instructions that are given in the weaved. Instructions(http://forum.weaved.com/t/how-to-get-started-with-remot3-it-for-pi/1029/6)
- The folder named "control_gpio_pi" should be placed on the Desktop in raspberry such that the location of the folder is  "/home/pi/Desktop/control_gpio_pi" or manually edit the code according to your preference and location of the folder later.
- The correct weaved (remote3.it) credentials should be given or replaced or entered in GUI of the application.
- If the default Username "pi" and Password "raspberry" for the raspberry is changed then change the same in the code since these details are hard coded. 

## Run:

```
  python control_gpio_GUI.py
```
