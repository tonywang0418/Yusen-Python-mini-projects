#!/usr/bin/python3
# Copy your serverinfo1.py script to database3.py and update it to write the server information into the existing device table in the cmdb database.
# YW-20240214
# Set up initial variables and imports
import subprocess #input command 
import psutil    #to view RAM, Disk, IP
import platform  #to view system, OS, version
import pymysql
#server connection
mydb = pymysql.connect(host='localhost', user='cmdb', password='sec444bc', database='cmdb')
mycursor = mydb.cursor() #creates cursor object used for CREATE, RETRIEVE, UPDATE AND DELETE.

def commands(command):
    """run subprocess command """
    proc = subprocess.run(command, shell=True, universal_newlines=True, capture_output=True, text=True)
    return proc.stdout.strip()

hostname = commands(['hostname'])
cpu_count = commands(['nproc'])
ram_gb = round(psutil.virtual_memory().total / 1024 / 1024 /1024 ,2)
os_type = platform.system()
os_version = platform.platform()[:40]
disk_list=set()  #I made a set{} to count disk, set() will prevent duplicate
disk_count = psutil.disk_partitions()     
for part in disk_count:            #these functions will exclude any device that contains string "loop" and only letter 
    if 'loop' not in part.device:                                            
        disk_num = ''.join(char for char in part.device if char.isalpha()) #some disk have mutiple partitions with same name but different number for example (dev/xvda1 and dev/xvda15) I use .isalpha to only accept letter and join each name as a string a way to package every name.
        disk_list.add(disk_num)
disks=len(disk_list) 
ip_eth0 = psutil.net_if_addrs()
mac_eth0 = psutil.net_if_addrs() 

def insert_data():
    query = "INSERT INTO `device` (`name`, `macaddress`, `ip`, `cpucount`, `disks`, `ram`, `ostype`, `osversion`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    mycursor.execute(query, (hostname, ip_eth0['eth0'][2][1], ip_eth0['eth0'][0][1], cpu_count, disks, ram_gb, os_type, os_version))
    mydb.commit()
    mydb.close()
def main():
    insert_data()
if __name__ == "__main__":
    main()

