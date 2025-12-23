import psutil
import argparse
import time

def main():
    args = parse_args()
    cores, cpu_usage = get_cpu_usage()
    mem_usage = get_memory_usage()
    disk_usage = get_disk_usage()
    net_speed = get_net_speed()
    if args.cpu:
        print_cpu_usage(cores, cpu_usage)
    if args.mem:
        print_mem_usage(mem_usage)
    if args.disk:
        print_disk_usage(disk_usage)
    if not (args.cpu or args.mem or args.disk):
        print_all(cpu_usage, mem_usage.percent, disk_usage.percent, net_speed)

def get_cpu_usage():
    cores = psutil.cpu_percent(interval=0.1, percpu=True)
    usage = psutil.cpu_percent(interval=0.1)
    return cores, usage


def get_memory_usage():
    usage = psutil.virtual_memory()
    return usage

def get_disk_usage():
    usage = psutil.disk_usage("/")
    return usage

def get_net_speed():
    old_value = psutil.net_io_counters()
    time.sleep(1)
    new_value = psutil.net_io_counters()

    bytes_sent = (new_value.bytes_sent - old_value.bytes_sent) / 1
    bytes_recv = (new_value.bytes_recv - old_value.bytes_recv) / 1
    packets_sent = (new_value.packets_sent - old_value.packets_sent) / 1
    packets_recv = (new_value.packets_recv - old_value.packets_recv) / 1
    return [bytes_sent, bytes_recv, packets_sent, packets_recv]

def print_all(cpu_usage, mem_usage, disk_usage, net_speed):
    print(f"CPU usage: {cpu_usage}%")
    print(f"Memory Usage: {mem_usage}%")
    print(f"Disk Usage: {disk_usage}%")
    print(f"Download Speed: {net_speed[1] / 1024:.2f} KB\n")

def print_cpu_usage(cores, usage):
    print(f"CPU usage:")
    print (f"Total: {usage}%")
    for i,core in enumerate(cores):
        print(f"Core {i+1}: {core}%")
    print()

def print_mem_usage(usage):
    print(f"Memory Usage:")
    print(f"Total: {usage.total / 1024 ** 3:.2f} GB")
    print(f"Used: {usage.used / 1024 ** 3:.2f} GB")
    print(f"Available: {usage.available / 1024 ** 3:.2f} GB")
    print(f"Usage: {usage.percent}%\n")

def print_disk_usage(usage):
    print("Disk Usage:")
    print(f"Total: {usage.total / 1024 ** 3:.2f} GB")
    print(f"Used: {usage.used / 1024 ** 3:.2f} GB")
    print(f"Free: {usage.free / 1024 ** 3:.2f} GB")
    print(f"Usage: {usage.percent}%\n")

def print_net_speed(net_speed):
    print(f"Network speed:")
    print(f"Upload Speed: {net_speed[0] / 1024:.2f:.2f} KB/s")
    print(f"Download Speed: {net_speed[1] / 1024:.2f:.2f} KB/s")
    print(f"Packets Upload: {int(net_speed[2])} Packets/s")
    print(f"Packets Download: {int(net_speed[3])} Packets/s\n")

def parse_args():
    parser = argparse.ArgumentParser(description="The system monitor")
    parser.add_argument("-c", "--cpu", action="store_true", help="check the CPU")
    parser.add_argument("-m", "--mem", action="store_true", help="check the Memory")
    parser.add_argument("-d", "--disk", action="store_true", help="check the Disk")
    parser.add_argument("-n", "--net", action="store_true", help="check the Network")
    return parser.parse_args()

if __name__ == "__main__":
    main()