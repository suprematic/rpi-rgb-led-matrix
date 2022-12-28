# 7c-M1 set-up

## Install OS & dev tools

- Install [DietPI](https://dietpi.com/docs/install/)
    - Setup WiFi (`dietpi.txt` and `dietpi-wifi.txt`)    
- Log in with default login: `root`:`dietpi`
  - (initial setup takes a couple of minutes, then a series of dialogs starts)  
  - Change "global software password" to `7c`
  - Change the login passwords for "root" and "dietpi" to `7c`
  - Disable the serial console in the dialog
  - `dietpi-software` dialog starts, search and install (same can be done with `apt`):
    - `git`
    - `vim`
    - `build-essentials`
  - Install Open-SSH server in `dietpi-software`
  - Opt-out from sending usage statistics in DietPI-Survey dialog
  - reboot
  - in `dietpi-config`:    
    - set time zone in "5 : Language/Regional Options"
    - for devices, which do not require Internet (so far, we don't have any):
        - set "Advanced Options" => "Time sync mode" to "0 - Custom"
        - set "Network Options: Misc" => "Boot Net Wait" to "0 - Disabled" (Off)    
  - reboot    
    
## Install and make SDK

```shell
cd ~
mkdir /opt/7c
cd /opt/7c
git clone https://github.com/suprematic/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix/
git checkout 7c/m1/dev
make
```

## Install python3 bindings

```shell
sudo apt-get update && sudo apt-get install python3-dev python3-pillow -y
make build-python PYTHON=$(command -v python3)
sudo make install-python PYTHON=$(command -v python3)
```


### Smoke-test

```shell
cd /opt/7c/rpi-rgb-led-matrix/bindings/python/7c
./m0.sh
```

The panel should display current time.

## Set up 7c systemd service

```shell
cp etc/7c.service /etc/systemd/system/7c.service
```

Service auto-start:
```shell
systemctl enable 7c.service
```