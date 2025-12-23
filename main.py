"""
Author: Weibo Lin

This program allows users to check their system status or monitor the system continuously.
Without the arguments, the system will automatically give all the parts of system that this program could check in once.
There are also some arguments that the users could add to the end of the command:
"-c, --cpu" is the argument that allows the users to check the current usage of cpu and each core of the cpu.
"-m, --mem" is the argument that allows the users to check the current usage of memory.
"-d, --disk" is the argument that allows the users to check the current usage of disk.
"n, --net" is the argument that allows the users to check the current network speed.
"--watch" is the argument that allows the users to monite the system continuously.
"""

import psutil
import argparse
import time
import sys

def main():
    args = parse_args()
    if args.watch:
        run_daemon(args)
    else:
        run_once(args)

def run_daemon(args):
    """
    This function runs the daemon that checks the current usage of the parts that the users want.
    This function uses a while loop to keep calling the function run_once to check the whole system again and again.
    :param args: The arguments that the users give.
    """

    # args.watch is one of the argument that users could add when they want to use the watch mode.
    interval = args.watch
    try:
        while True:
            # clear the terminal
            print("\033c", end="")
            print("System Monitor (Daemon Mode)")
            # call the function that run all the checks
            run_once(args)
            # wait for the interval
            time.sleep(interval)
    except KeyboardInterrupt:
        sys.exit("\nUser interrupt")

def run_once(args):
    """
    This function runs once to check the parts that the users want.
    This function could be called by run_daemon to run the watch mode.
    :param args: the arguments that the users give.
    """

    # If there are any parts that users don't want to check, it won't run the check so the user could save some memory.
    show_all = not (args.cpu or args.mem or args.disk or args.net)
    if args.cpu or show_all:
        cores, cpu_usage = get_cpu_usage()
        print_cpu_usage(cores, cpu_usage)
    if args.mem or show_all:
        mem_usage = get_memory_usage()
        print_mem_usage(mem_usage)
    if args.disk or show_all:
        disk_usage = get_disk_usage()
        print_disk_usage(disk_usage)
    if args.net or show_all:
        net_speed = get_net_speed()
        print_net_speed(net_speed)


def get_cpu_usage():
    """
    This function returns the cpu usage of the system.
    :return: usage of the cpu and each core of it
    """

    # interval=0.1 means measure CPU usage over 0.1 second
    cores = psutil.cpu_percent(interval=0.1, percpu=True)
    usage = sum(cores) / len(cores)
    return cores, usage


def get_memory_usage():
    """
    This function returns the memory usage of the system.
    :return: usage of the memory
    """

    usage = psutil.virtual_memory()
    return usage

def get_disk_usage():
    """
    This function returns the disk usage of the system.
    :return: usage of the disk
    """

    usage = psutil.disk_usage("/")
    return usage

def get_net_speed():
    """
    This function returns the network speed of the system.
    :return: The bytes that received and sent and the packets that received and sent of the system.
    """

    old_value = psutil.net_io_counters()
    time.sleep(1)
    new_value = psutil.net_io_counters()

    bytes_sent = (new_value.bytes_sent - old_value.bytes_sent)
    bytes_recv = (new_value.bytes_recv - old_value.bytes_recv)
    packets_sent = (new_value.packets_sent - old_value.packets_sent)
    packets_recv = (new_value.packets_recv - old_value.packets_recv)
    return [bytes_sent, bytes_recv, packets_sent, packets_recv]

def print_cpu_usage(cores, usage):
    """
    This function prints the cpu usage and each core of it of the system.
    :param cores: the usage of each core of the cpu
    :param usage: the usage of cpu
    """

    print(f"CPU usage:")
    print(f"Total: {usage:.1f}%")
    print(f"{ascii_bar(usage)}")
    for i,core in enumerate(cores):
        print(f"Core {i+1}: {ascii_bar(core)}")
    print()

def print_mem_usage(usage):
    """
    This function prints the memory usage of the system.
    :param usage: the usage of memory
    """

    print(f"Memory Usage:")
    # Convert the bytes to the GBs
    print(f"Total: {usage.total / 1024 ** 3:.2f} GB")
    print(f"Used: {usage.used / 1024 ** 3:.2f} GB")
    print(f"Available: {usage.available / 1024 ** 3:.2f} GB")
    print(f"Usage: {usage.percent}%")
    print(f"{ascii_bar(usage.percent)}\n")

def print_disk_usage(usage):
    """
    This function prints the disk usage of the system.
    :param usage: usage of disk
    """

    print("Disk Usage:")
    # Convert the bytes to the GBs
    print(f"Total: {usage.total / 1024 ** 3:.2f} GB")
    print(f"Used: {usage.used / 1024 ** 3:.2f} GB")
    print(f"Free: {usage.free / 1024 ** 3:.2f} GB")
    print(f"Usage: {usage.percent}%")
    print(f"{ascii_bar(usage.percent)}\n")

def print_net_speed(net_speed):
    """
    This function prints the network speed of the system.
    :param net_speed: network speed of the system
    """

    print(f"Network speed:")
    # Convert the bytes to the KBs
    print(f"Upload Speed: {net_speed[0] / 1024:.2f} KB/s")
    print(f"Download Speed: {net_speed[1] / 1024:.2f} KB/s")
    print(f"Packets Upload: {int(net_speed[2])} Packets/s")
    print(f"Packets Download: {int(net_speed[3])} Packets/s\n")

def parse_args():
    """
    This function parses the command line arguments.
    """
    parser = argparse.ArgumentParser(description="The system monitor")
    parser.add_argument("-c", "--cpu", action="store_true", help="check the CPU")
    parser.add_argument("-m", "--mem", action="store_true", help="check the Memory")
    parser.add_argument("-d", "--disk", action="store_true", help="check the Disk")
    parser.add_argument("-n", "--net", action="store_true", help="check the Network")
    parser.add_argument("-w", "--watch", type=int, nargs="?", const=2, help="Keep watching")
    return parser.parse_args()

def ascii_bar(percent, width=20):
    """
    This function returns the ascii art of the system usage percentage.
    :param percent: the percentage of the system usage
    :param width: the width of the ascii art
    """
    filled = int(width * percent / 100)
    return "[" + "#" * filled + "." * (width - filled) + f"] {percent:.1f}%"

if __name__ == "__main__":
    main()