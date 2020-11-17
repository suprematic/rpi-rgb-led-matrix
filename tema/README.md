# TeMa 0.1.0

## Install OS & dev tools

- Install [DietPI](https://dietpi.com/docs/user-guide_installation/)
- Log in with default login: `root`:`dietpi`
  - (initial setup takes a couple of minutes, then a series of dialogs starts)
  - Opt-out from sending usage statistics in DietPI-Survey dialog
  - Change the login passwords for "root" and "dietpi" to e.g., `tema`
  - Disable the serial console in the dialog
  - `dietpi-software` dialog starts, search and install (same can be done with `apt`):
    - `git`    
    - `vim`
    - `build-essentials`
  - reboot
  - in `dietpi-config`:
    - set "Advanced Options" => "Time sync mode" to "0 - Custom"
    - set "Network Options: Misc" => "Boot Net Wait" to "0 - Disabled" (Off)
    - set "AutoStart Options" => "Automatic login" to `root` user (the rpi-rgb-led-matrix SDK requires `root` user!)
  - reboot    
    
    
## Install SDK

```bash
cd ~
mkdir tema
cd tema/
git clone https://github.com/suprematic/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix/
git checkout tema-p10
make
```


## Build
```bash
cd ~/tema/rpi-rgb-led-matrix/tema/
make tema
```


### Smoke-test
```bash
cd ~/tema/rpi-rgb-led-matrix/tema/
./test_green.sh 644
```


### Autostart Smoke-test
```bash
echo './tema/rpi-rgb-led-matrix/tema/test_green.sh 644' >> ~/.bashrc
```

