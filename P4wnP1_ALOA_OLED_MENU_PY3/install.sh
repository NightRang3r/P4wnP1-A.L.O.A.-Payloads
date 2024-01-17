#!/bin/sh

# Setup for P4wnP1 LCD
echo "[*] Setting up P4wnP1 LCD..."
mkdir /root/BeBoXGui/ || { echo "Failed to create directory /root/BeBoXGui/. Exiting."; exit 1; }
cp *.py /root/BeBoXGui/ || { echo "Failed to copy Python scripts. Exiting."; exit 1; }
mkdir /root/BeBoXGui/images || { echo "Failed to create images directory. Exiting."; exit 1; }
cp images/* /root/BeBoXGui/images/ || { echo "Failed to copy images. Exiting."; exit 1; }
cp scripts/runmenu.sh /usr/local/P4wnP1/scripts/ || { echo "Failed to copy runmenu.sh script. Exiting."; exit 1; }

echo "All files are ready"
echo "To run with P4wnP1 boot, go through the web interface"
echo "and set the run script sh to 'runmenu.sh' in the trigger section."
echo "Enjoy"
echo "Note: By default, gui.py uses the SPI interface."
echo "If you use an I2C LCD, edit gui.py and set I2C_USER=1"

echo "[*] Script execution completed."
