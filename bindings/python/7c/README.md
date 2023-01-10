# 7C-M1 set-up

## Pre-requisites

1) Define PANEL_NAME (e.g. `7C-M1-R2`)

2) Use SUPREMATIC_INTERNAL WiFi for initial set-up


## Install firmware

### OS & dev tools

- Install [DietPI](https://dietpi.com/docs/install/)

- Copy (overwrite) the prepared `dietpi/dietpi.txt` to the SD card
    - change `AUTO_SETUP_NET_HOSTNAME` to PANEL_NAME
- Setup WiFi credentials in `dietpi-wifi.txt`

- Insert the SD card to Raspi and boot

- Find out the IP address of the Raspi
    - For SUPREMATIC Mikrotik router: http://192.168.114.1/webfig/#IP:DHCP_Server.Leases
    - Or use any IP scanner available

- Log in with `ssh root@<ip-address>`
    - (The first boot will take some time)
    - Leave `dietpi` software password    
    - Disable the UART serial console in the dialog
    - `dietpi-software` dialog starts, search and install (same can be done with `apt`):
      - `git`
      - `vim`
      - `build-essential`
      
### Install and make rpi-rgb-led-matrix SDK

```shell
mkdir /opt/7c
cd /opt/7c
git clone https://github.com/suprematic/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix/
git checkout 7c/m1/dev
make
```

### Install and make python3 bindings

```shell
sudo apt-get update --allow-releaseinfo-change && sudo apt-get install python3-dev python3-pillow -y
make build-python PYTHON=$(command -v python3)
sudo make install-python PYTHON=$(command -v python3)
```


### Run smoke-test

```shell
cd /opt/7c/rpi-rgb-led-matrix/bindings/python/7c
./m1.sh
```

The panel should display current time.

## Set up 7c systemd service

```shell
cp etc/systemd/system/7c.service /etc/systemd/system/7c.service
```

Service start:
```shell
systemctl start 7c.service
```

Service auto-start:
```shell
systemctl enable 7c.service
```


### Final test

```shell
reboot
```

The panel should display current time.


## Change WiFi to customer network

- Get WiFi SSID and key
- In `dietpi-config`:
    - Go to "7: Network Options: Adapters"
    - Go to "WiFi"
    - Go to "Scan"
    - Select "SUPREMATIC_INTERNAL" and remove it
    - Select the 0th slot
    - Select "Manual"
        - Enter SSID
        - Enter key
    - done, back, back, exit, ok

    


## Install development environment

### RGBMatrixEmulator

- Install [Python 3.10.9](https://www.python.org/downloads/release/python-3109/)
- Install Pillow with `pip install Pillow`
- Install RGBMatrixEmulator with `pip install RGBMatrixEmulator`
- Clone [RGBMatrixEmulator](https://github.com/ty-porter/RGBMatrixEmulator)

Smoke-test with:
```
cd RGBMatrixEmulator/samples
python runtext.py
```

Open `http://localhost:8888` in browser, "Hello world!" is to be displayed.
