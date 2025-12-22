import psutil
import argparse

def main():
    args = parse_args()

    if args.cpu:
        cpu_usage = get_cpu_usage()
        print(f"CPU usage: {cpu_usage}%")
    if args.mem:
        mem_usage = get_memory_usage()
        print(f"Memory Usage: {mem_usage.percent}%")
    if args.disk:
        disk_usage = get_disk_usage()
        print(f"Disk Usage: {disk_usage.percent}%")
    
    if not (args.cpu or args.mem or args.disk):
        cpu_usage = get_cpu_usage()
        mem_usage = get_memory_usage()
        disk_usage = get_disk_usage()
        print(f"CPU usage: {cpu_usage}%")
        print(f"Memory Usage: {mem_usage.percent}%")
        print(f"Disk Usage: {disk_usage.percent}%")

def get_cpu_usage():
    usage = psutil.cpu_percent(interval=1)
    return usage

def get_memory_usage():
    usage = psutil.virtual_memory()
    return usage

def get_disk_usage():
    usage = psutil.disk_usage("/")
    return usage

def parse_args():
    parser = argparse.ArgumentParser(description="The system monitor")
    parser.add_argument("-c", "--cpu", action="store_true", help="check the CPU")
    parser.add_argument("-m", "--mem", action="store_true", help="check the Memory")
    parser.add_argument("-d", "--disk", action="store_true", help="check the Disk")
    return parser.parse_args()

if __name__ == "__main__":
    main()