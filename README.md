# litexOnColorlightLab004

Demonstration on using a Soft Core (**VexRiscv**)
built with **LiTex** in a **Colorlight 5A-75B** or **Colorlight I5** (ECP5).
This demo is based on
[lab004][lab004] of [fpga_101][fpga_101] repository.

- push button is used as reset
- led is used for *led* demo in firmware

## Colorlight 5A-75B

UART use (arbitrary) J1 pins 1 & 2

| name      | Pin | note        |
|-----------|-----|-------------|
| clk25     | P6  | 25MHz clock |
| cpu_reset | P11 | button J28  |
| user_led  | P11 | button J28  |
| Uart TX   | F3  | J1.1        |
| Uart RX   | F1  | J1.2        |

## Colorlight I5

UART is directly available through CMSIS-DAP ACM interface

| name        | Pin | note        |
|-------------|-----|-------------|
| clk25       | P3  | 25MHz clock |
| cpu_reset_n | K18 | button J28  |
| user_led    | U16 | button J28  |
| Uart TX     | J17 | CMSIS-DAP   |
| Uart RX     | H18 | CMSIS-DAP   |

## Prerequisite

### software

- [openFPGALoader][openFPGALoader]
- [LiteX and Migen tools]() (see [fpga_101][fpga_101] README for install
  everything).
- yosys, nextpnr and prjtrellis

### hardware (Colorlight 5A-75B only)

- **ColorLight 5A-75B** has no on-board JTAG adapter, so user must solder a pinheader
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
./base.py --version 5A-75B --build
```
or
```bash
./base.py --version I5 --build
```
### firmware
```bash
cd firmware && make
```
see [lab004] for more details.

## load bitstream
```bash
./base.py --version 5A-75B --load [--cable yourCable] # change 5A-75B by I5
```
where *yourCable* depends on your JTAG probe. If `--cable` is not provided
*openFPGALoader* will uses `ft2232` generic interface. Not required for I5.

## load firmware
```bash
lxterm /dev/ttyYYYX --kernel firmware/firmware.bin
```
where *ttyYYYX* is your USB <-> UART converter device (usually ttyUSB0 (5A-75B)
or ttyACM0 (I5)).

## boot
```bash
serialboot
```

## test
To start the blink led use command
```bash
led
```


[fpga_101]: https://github.com/litex-hub/fpga_101
[lab004]: https://github.com/litex-hub/fpga_101/tree/master/lab004
[openFPGALoader]: https://github.com/trabucayre/openFPGALoader
