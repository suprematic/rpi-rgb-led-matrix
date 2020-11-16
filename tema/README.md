# Ver. 0.0.0

## Install OS & dev tools

- [DietPI](https://dietpi.com/docs/user-guide_installation/)
- With `dietpi-software` install addtionally:
  - git
  - vim
  - make => `apt install build-essential`


## Install SDK
```bash
cd ~
mkdir tema
cd tema
git clone https://github.com/suprematic/rpi-rgb-led-matrix.git
cd rpi-rgb-led-matrix
git checkout tema-p10
make
```

## Build
```bash
cd ~/tema/rpi-rgb-led-matrix/tema
make tema
```

### Smoke-test
```bash
cd ~/tema/rpi-rgb-led-matrix/tema
./test_green.sh 644
```

### Smoke-test autostart
```bash
echo './tema/rpi-rgb-led-matrix/tema/test_green.sh 644' >> ~/.bashrc
```