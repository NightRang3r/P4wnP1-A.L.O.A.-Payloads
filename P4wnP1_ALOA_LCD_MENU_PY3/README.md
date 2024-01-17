# P4wnP1_ALOA_LCD_MENU

## Introduction

This project is a fork of the [P4wnP1_ALOA_OLED_MENU_V2](https://github.com/beboxos/P4wnP1_ALOA_OLED_MENU_V2) by BeBoXoS. It has been updated to Python 3 and modified for compatibility with the Waveshare 1.3inch LCD HAT for Raspberry Pi. More information about this LCD HAT is available [here](https://www.waveshare.com/1.3inch-lcd-hat.htm).

**LCD Specifications:**

- Driver: ST7789
- Interface: SPI
- Resolution: 240x240

## Installation Instructions

### Prerequisites

- BeBoX P4wnP1 ALOHA v0.1.1 image: [Download here](https://mega.nz/#!YYtS2S6A!Q5OgMvLUtAM_x7jt7vBTY8Zu8lHdyyPoaLdsipVufWg).

### Installation Steps

- Connect to your P4wnP1 ALOHA via usb and ssh into it.
- Login to the P4wnP1 ALOHA via web interface at http://172.16.0.1:8000/ and go to the "WIFI SETTINGS" tab.
- You will need to connect to your WIFI network as "Station (Client)" mode for the installation to work.

Then run the following commands:

```bash
git clone https://github.com/NightRang3r/P4wnP1_ALOA_LCD_MENU.git
cd P4wnP1_ALOA_LCD_MENU
./install.sh

```

### Compatibility

- The script may be compatible with other Waveshare LCD displays, but adjustments to the `gui.py` file will likely be necessary.

### Configuration Steps

1. **Display Driver Modification**

   Update the driver in `gui.py`:

   ```python
   from luma.lcd.device import st7789  # Change to your display driver
````

2. **Setting Display Dimensions**

   Configure the display width and height in `gui.py`:

   ```python
   width = 240  # Change to your display width
   height = 240  # Change to your display height
   ```

3. **Pin Configuration**

   Adjust the PIN settings to match your LCD display:

   ```python
   RST = 27
   CS = 8
   DC = 25

   # GPIO definition and LCD configuration
   RST_PIN = 27  # Waveshare settings
   CS_PIN = 8    # Waveshare settings
   DC_PIN = 25   # Waveshare settings
   KEY_UP_PIN = 6     # Stick up
   KEY_DOWN_PIN = 19  # Stick down
   KEY_LEFT_PIN = 5   # Stick left / go back
   KEY_RIGHT_PIN = 26 # Stick right / go in / validate
   KEY_PRESS_PIN = 13 # Stick center button
   KEY1_PIN = 21      # Key 1 / up
   KEY2_PIN = 20      # Key 2 / cancel/go back
   KEY3_PIN = 16      # Key 3 / down
   USER_I2C = 0       # Set to 1 if your OLED is I2C or 0 if using SPI interface
   ```

4. **Adjusting Padding**

   Modify padding values if text is overlapping:

   ```python
   padding = -2
   top = padding
   bottom = height - padding
   line1 = top
   line2 = top + 20
   line3 = top + 40
   line4 = top + 60
   line5 = top + 80
   line6 = top + 100
   line7 = top + 120
   brightness = 255  # Max brightness
   ```

5. **SPI Configuration**

   Update SPI settings and PINs:

   ```python
   serial = spi(device=0, port=0, gpio_DC=25, gpio_RST=27)
   ```

6. **Splash Image Size Adjustment**

   Configure the display size for the splash image. You may need to resize the image in the image folder to match your display size:

   ```python
   device.width = 240
   device.height = 240
   c = (240 - 220) / 2
   f = (240 - 350) / 2
   ```
