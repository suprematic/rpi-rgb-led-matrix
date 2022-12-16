# TeCa set-up

## Install OS & dev tools

- Install [DietPI](https://dietpi.com/docs/install/)
- Setup WiFi (`dietpi.txt` and `dietpi-wifi.txt`)
- Log in with default login: `root`:`dietpi`
  - (initial setup takes a couple of minutes, then a series of dialogs starts)  
  - Change "global software password" to `tema`
  - Change the login passwords for "root" and "dietpi" to `tema`
  - Disable the serial console in the dialog
  - `dietpi-software` dialog starts, search and install (same can be done with `apt`):
    - `git`    
    - `vim`
    - `build-essentials`
  - Install Open-SSH server in `dietpi-software`
  - Opt-out from sending usage statistics in DietPI-Survey dialog
  - reboot
  - in `dietpi-config`:    
    - set "AutoStart Options" => "Automatic login" to `root` user (the rpi-rgb-led-matrix SDK requires `root` user!)
    - set time zone in "5 : Language/Regional Options"
    - for devices, which do not require Internet (so far, we don't have any):
        - set "Advanced Options" => "Time sync mode" to "0 - Custom"
        - set "Network Options: Misc" => "Boot Net Wait" to "0 - Disabled" (Off)
    -
  - reboot    
    
## Install and make SDK

```bash
cd ~
mkdir /opt/tema
cd /opt/tema
git clone https://github.com/suprematic/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix/
git checkout tema
make
```

## Install python3 bindings

See `rpi-rgb-led-matrix/bindings/python/README.md` => "Python 3"


### Smoke-test

```bash
cd /opt/tema/rpi-rgb-led-matrix/bindings/python/samples
./tennis-midi-p10.sh
```

The panel should display current time.

## Set up tema systemd service

`/etc/systemd/system/tema.service`

```
[Unit]
Description=TeMa Tableau

Requires=local-fs.target
After=local-fs.target
DefaultDependencies=no

[Service]
Type=simple
Restart=on-failure

## Dirs
ProtectSystem=strict
ProtectHome=true
WorkingDirectory=/opt/tema

## Env
#Environment=BLOCKING_MAX_THREADS=16

ExecStart=/bin/sh rpi-rgb-led-matrix/bindings/python/samples/tennis-midi-p10.sh

[Install]
WantedBy=basic.target
```

Service auto-start:
```bash
systemctl enable tema.service
```
