# System Monitor

## Overview
A lightweight command-line system monitoring tool written in Python using the psutil library. It displays CPU usage, memory usage, disk usage, and network speed with ASCII bar visualizations.

## Project Structure
```
.
├── main.py           # Main application entry point
├── requirements.txt  # Python dependencies (psutil)
├── README.md         # User documentation
└── LICENSE           # Project license
```

## How to Run
The application runs as a console application with various command-line arguments:

```bash
python main.py           # Show all system stats once
python main.py -c        # Show CPU usage only
python main.py -m        # Show memory usage only
python main.py -d        # Show disk usage only
python main.py -n        # Show network speed only
python main.py -w        # Watch mode (refresh every 2 seconds)
python main.py -w 5      # Watch mode with custom interval (5 seconds)
```

## Dependencies
- Python 3.11
- psutil - Cross-platform library for system monitoring

## Features
- CPU usage (total and per-core)
- Memory usage (total, used, available)
- Disk usage (total, used, free)
- Network speed (upload/download bytes and packets)
- Watch mode for continuous monitoring
- ASCII bar visualizations

## Online Demo
To try this online, you need follow a few steps
1. Click the Replit link below to open this project in view mode:
https://replit.com/@weibolin322/System-Monitor
2. Click **Remix** to create your own copy
3. Press **Run** to try!!!

## Why I build this
I built this project because I'm very interested in how computer hardware
and operating systems work.

It's also because I want to build my own CLI tools with the argument parsing and terminal output.

This project is a starting point, and I plan to build more CLI tools in
the future.