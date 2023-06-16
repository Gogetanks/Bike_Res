# Bike Reservation System
## Compilation of a linux system for Raspberry Pi zero

After running the script initialize.sh and specigyin all personal setting, go to directory buildroot-2023.02
and run command 'make' command to start compilation. Depending on performance of your PC it can take 
from 10 to 90 minutes. Resulting images you will find in directory buildroot-2023.02/output/imagesi/
Copythe image sdcard.img into your SD card with the help of command
sudo dd if=sdcard.img of=/dev/mmc... status=progress
