# Zumi + alwaysAI Demo

## Requirements
- [alwaysAI account](https://dashboard.alwaysai.co/auth?register=true)
- [Zumi Robot*](https://www.robolink.com/zumi/)

*NOTE: These instructions require the use of a Raspberry Pi 3B+ in place of the default Raspberry Pi Zero that currently comes with the default Zumi package.

## Setup
The following instructions are for fresh installs using a Raspberry Pi and blank microSD Card. If your Zumi is already setup, skip to step 9.

1. Download Zumi image from [Robolink](https://forum.robolink.com/topic/475/new-sd-card-image-is-here)
2. Flash the image onto a microSD card per [Robolink instructions](https://www.youtube.com/watch?v=CV6Jtr138ms)
3. Setup Zumi per the [Robolink instructions](https://drive.google.com/file/d/13wVFnDWOo-79_rO7av3L4SAzrmaQ1Rtn/view)
4. Connect to a monitor, keyboard and mouse to complete the next steps 5-7
5. Run `sudo raspi-config` from the command line to configure the correct locale and keyboard layout
6. Create a python file called `wifi.py` And paste the following code in it, adding your wifi credentials (unless you'll be programming purely via ethernet):
```
import zumidashboard.scripts as scripts
#add your info in here then run this program
network_name = ""
network_password = ""
scripts.get_ssid_list()
scripts.kill_supplicant()
scripts.add_wifi(network_name,network_password)
scripts.check_wifi()
```
7. Run the above script: `sudo python3 wifi.py`
8. Reboot the Zumi: `sudo reboot`

**From here you can either ssh to the Zumi or continue using the monitor, keyboard, mouse option. Default ssh path will be something like `ssh pi@zumi1234.local` and the default password is `pi`** 

9. Install Docker: `curl -sSL https://get.docker.com | sh`
10. Giver user Docker permissions: `sudo usermod -aG docker $USER`

## alwaysAI
The following adjustments should be made to run alwaysAI apps on a Zumi:
1. Add a `requirements.txt` file to your project's root directory with the following dependencies:
```
rpi.gpio
Adafruit_SSD1306
Pillow
```
2. Add a script called `update_zumi.sh` to your project's root folder with the following bash script:
```
#!/bin/bash
# This script will replace the hardcoded offsets.txt file path
# Run AFTER `aai app deploy` has copied the zumi package to the
# app's root folder under /venv/s

if sed -i 's+/home/pi/offsets.txt+/offsets.txt+g' ./usr/local/lib/python3.6/site-packages/zumi/zumi.py; then
    echo 'Updated zumi.py'
else
    echo 'Unable to update zumi.py'
fi
```
3. Add the following to your project's existing `Dockerfile`:
```
RUN apt-get install libjpeg-dev && apt-get install zlib1g-dev && apt-get install libpng-dev
RUN pip install setuptools zumi
COPY update_zumi.sh /update_zumi.sh
RUN /bin/bash /update_zumi.sh
```

When you run `aai app deploy` from your dev machine all the required Zumi and alwaysAI dependencies will be copied to a folder path on the Zumi specified by the `aai app configure` command. The `update_zumi.sh` script will then run to update the project's copy of the zumi library (but not the Zumi's host copy) so that the python code within the alwaysai docker image will properly generate the zumi's calibration `offset.txt` file.

Now you'll be able to run all the [Zumi functions](http://docs.robolink.com/zumi-library) with an alwaysAI app on a Zumi.

## Autostart
If you want to start your alwaysAI app when the Zumi starts, do the following:
1. Create a standlone docker image by running the included `build_standalone.sh` script, which is a convenience from the [alwaysAI instructions](https://alwaysai.co/docs/application_development/packaging_app_as_docker_image.html)
2. Then in modify the `/etc/rc.local` file with a line like the following:
```
bash /home/pi/<project_path_as_specified_in_aai_app_configure>/start_standalone.sh &
```
Be sure the `exit 0` line is the last line.

3. Reboot to take effect: `sudo reboot`
