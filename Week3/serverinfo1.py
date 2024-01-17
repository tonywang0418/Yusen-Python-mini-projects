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
disk_list=set()  #I made a list to count disk, set() will prevent duplicate
disk_count = psutil.disk_partitions()     
for part in disk_count:            #these functions will exclude any device that contains string "loop" and only letter 
    if 'loop' not in part.device:                                            
        disk_num = ''.join(char for char in part.device if char.isalpha()) #some disk have mutiple partitions with same name but different number for example (dev/xvda1 and dev/xvda15) I use .isalpha to only accept letter and join each name as a string a way to package every name.
        disk_list.add(disk_num)
disks=len(disk_list) 

ip_eth0 = psutil.net_if_addrs()

mac_eth0 = psutil.net_if_addrs() 
print(f'Hostname: {hostname}')
print(f'CPU(count): {cpu_count}')
print(f'RAM(GB): {ram_gb}')
print(f'OSType: {os_type}')
print(f'OSVersion: {os_version}')
print(f'Disk(Count): {disks}')
print(f"ip of eth0: {ip_eth0['eth0'][0][1]}")
print(f"mac of eth0: {ip_eth0['eth0'][2][1]}")
