# Battery-Information
A little standalone tool for monitoring battery status on laptops, written in python. 

Battery Information Version 1.0 

# Introduction
This script provides a graphical user interface (GUI) to display real-time information about the battery status on a Windows system. It utilizes the wx library for the GUI, psutil for retrieving battery information, and winsound for playing an alert sound when the battery level is low.

# Features
Displays the percentage of battery remaining.
Shows the approximate time remaining until the battery is fully discharged when unplugged.
Indicates whether the power cable is connected or not.
Plays an alert sound when the battery level is below 30% and the power cable is disconnected.

# Requirements
Python 3.x
wxPython: pip install wxpython
psutil: pip install psutil

# Usage
Ensure that Python and the required libraries are installed.
Run the script Battery_information.py.
A GUI window will open displaying the battery information.
The window will update automatically every second with the latest battery status.

# File Structure
battery_info_popup.py: Main Python script containing the application code.
quack_5.wav: Sound file for the low battery alert. Replace with your desired sound file if needed.

# Important Notes
This script is specifically designed for Windows systems.
Make sure to adjust the file path for the alert sound (quack_5.wav) according to your system configuration.
Feel free to customize the GUI layout or add additional features as per your requirements.

# Credits
This script was created by Enrico Mostacci.
