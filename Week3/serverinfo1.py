#!/usr/bin/python3
# This script returns information about the machine it is running on to the screen
# YW-20240116
# Set up initial variables and imports
import subprocess #input command 
import psutil    #to view RAM, Disk, IP
import platform  #to viwq system, OS, version

def commands(command):
    """run subprocess command """
    proc = subprocess.run(command, shell=True, universal_newlines=True, capture_output=True, text=True)
    return proc.stdout.strip()

hostname = commands(['hostname'])

cpu_count = commands(['nproc'])

ram_gb = round(psutil.virtual_memory().total / 1024 / 1024 /1024 ,2)

os_type = platform.system()

os_version = platform.platform()

disk_count = len(psutil.disk_partitions())

ip_eth0 = psutil.net_if_addrs()

mac_eth0 = psutil.net_if_addrs() 
print(f'Hostname: {hostname}')
print(f'CPU(count): {cpu_count}')
print(f'RAM(GB): {ram_gb}')
print(f'OSType: {os_type}')
print(f'OSVersion: {os_version}')
print(f'Disk(Count): {disk_count}')
print(f"ip of eth0: {ip_eth0['eth0'][0][1]}")
print(f"mac of eth0: {ip_eth0['eth0'][2][1]}")
