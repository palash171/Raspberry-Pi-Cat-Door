# Camera Preview C++

This folder has only 3 files:

- `main.cpp` = the C++ program
- `Makefile` = lets you build with `make`
- `README.md` = these notes

## What the program does

It only tries to open the Raspberry Pi camera preview.

First it tries:

```bash
rpicam-hello --timeout 0
```

If that fails, it tries:

```bash
libcamera-hello --timeout 0
```

`--timeout 0` means keep the camera preview open until you stop it.

## Build

```bash
make
```

## Run

```bash
./camera_preview
```

Stop it with:

```bash
Ctrl+C
```
