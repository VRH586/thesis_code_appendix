Instructions for Simple Smart Badge Demo

Do not connect the Raspberry Pi to WiFi, this causes problems with BLE

#1
Connect each Nicla Vision Board to the corresponding badge, the number 
for each Nicla Vision board is on the back of box. The badges start
running on their own.

#2
Open three terminals in the DEMO_TALLINN directory.

#3
Run each of the 3 programs from each terminal with python3:
Notes:
-If ble_connect.py fails to run, reset every badge by pressing the small
button next to the camera

-The real time video feed and animation are closed by pressing 'q'.

-If the badges and Nicla Vision boards get switched around, their 
numbers can be checked by connecting the board to a PC and checking the 
number in the boards main.py file.

-Both the badges and base station sets the camera white balance when 
turned on, restart if it looks wierd.
