# litexOnColorlightLab004

Demonstration on using a Soft Core (**VexRiscv**)
built with **LiTex** in a **Colorlight 5A-7B** (ECP5).
This demo is based on
[lab004][lab004] of [fpga_101][fpga_101] repository.

- push button is used as reset
- led is used for *led* demo in firmware
- UART use (arbitrary) J1 pins 1 & 2

| name      | Pin | note        |
|-----------|-----|-------------|
| clk25     | P6  | 25MHz clock |
| cpu_reset | P11 | button J28  |
| user_led  | P11 | button J28  |
| Uart TX   | F3  | J1.1        |
| Uart RX   | F1  | J1.2        |


## Prerequisite

### software

- [openFPGALoader][openFPGALoader]
- [LiteX and Migen tools]() (see [fpga_101][fpga_101] README for install
  everything).
- yosys, nextpnr and prjtrellis

### hardware

- **ColorLight** has no on-board JTAG adapter, so user must solder a pinheader
  (**J27** for JTAG signals, **J33** for VCC and **J34** for GND) and connect an external probe (see.
  [chubby75](https://github.com/q3k/chubby75/tree/master/5a-75b));
- level shifter *74HC245T* are used between FPGA and Jx connectors. To be able
  to use corresponding pins in bidirectional mode and in 3.3V instead 5V, buffer
  must be desoldered, and replace or just bypass. To have, a partial, access to
  J1, buffer U28 must be dropped (see next figure);
- an USB <-> serial converter must be used to have access to serial interface

![JX direct connection](http://kmf2.trabucayre.com/colorLight5A-75b.jpg)

**U28 without buffer and with direct connection between input and output.**

## Build

### gateware
Just:
```bash
./base.py --build
```
### firmware
```bash
cd firmware && make
```
see [lab004] for more details.

## load bitstream
```bash
./base.py --load [--cable yourCable]
```
where *yourCable* depends on your JTAG probe. If `--cable` is not provided
*openFPGALoader* will uses ft2232` generic interface.

## load firmware
```bash
lxterm /dev/ttyUSBX --kernel firmware/firmware.bin
```
where *ttyUSBX* is your USB <-> UART converter device.

[fpga_101]: https://github.com/litex-hub/fpga_101
[lab004]: https://github.com/litex-hub/fpga_101/tree/master/lab004
[openFPGALoader]: https://github.com/trabucayre/openFPGALoader
