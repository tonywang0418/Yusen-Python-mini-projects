#!/usr/bin/python3
# This script has 4 mode, update hash, check file integrity, add IP or DNS to database, delete IP or DNS from database 
# YW-20240218
import os
import sys
import pymysql
from datetime import datetime
import hashlib
import csv
import time
from pinglib import pingthis
import psutil
#import subprocess
#server connection
def database_connection():
    mydb = pymysql.connect(host='localhost', user='cmdb', password='sec444bc', database='cmdb') 
    mycursor = mydb.cursor() #creates cursor object used for CREATE, RETRIEVE, UPDATE AND DELETE.
    return mycursor, mydb
def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb')as file:
        while True:
            chunk = file.read(4096) #read only 4096 each time to save memory space
            if not chunk:
                break
            hash_md5.update(chunk) #update the hash everytime it reads a chunk
        return hash_md5.hexdigest()

def zulu_timestamp():
    utc_time = datetime.utcnow()
    format_time = utc_time.strftime("%Y-%m-%dT%H:%M")
    return format_time
def insert_update_mysql_mode(md5_hash,time_stamp,file_path): 
    mycursor, mydb = database_connection()
    query =  "SELECT * FROM `files` WHERE `path`= %s"  #find the row that contains the path
    mycursor.execute(query,(file_path))
    result = mycursor.fetchone() #fetch one row
    if result: #if result exist
        query = "UPDATE `files` SET `timestamp` = %s, `hash` = %s WHERE `files`.`path` = %s"
        cursor = mycursor.execute(query,(time_stamp, md5_hash, file_path))
        mydb.commit()

    else:
        query =  "INSERT INTO `files` (`timestamp`, `path`, `hash`) VALUES (%s,%s,%s)"
        cursor = mycursor.execute(query,(time_stamp,file_path,md5_hash))
        mydb.commit()
    mydb.close()
def check_mode(seconds_between_runs):
    try:
        while True:
            mycursor,mydb = database_connection()  #database connection

            query = "SELECT `path` FROM `files`"
            mycursor.execute(query)
            file_paths = mycursor.fetchall()
            
            checks = []
            for path in file_paths:
                file_path = path[0]

                if os.path.exists(file_path):
                    old_time_query = "SELECT `timestamp` FROM `files` WHERE `path` = %s"
                    mycursor.execute(old_time_query, (file_path,))
                    old_time = mycursor.fetchone()[0]

                    status = 'OK'
                    query = "SELECT `hash` FROM `files` WHERE `path` = %s"
                    mycursor.execute(query, (file_path,))
                    old_hash = mycursor.fetchone()[0]

                    md5_hash = calculate_md5(file_path)
                    time_stamp = zulu_timestamp()
                    #insert_update_mysql_mode(md5_hash, time_stamp, file_path)

                    if old_hash != md5_hash:
                        status = 'FAIL'
            
                    message = f"FILE={file_path}, OLD_HASH={old_hash}, OLD_HASH_DATE= {old_time}, CURRENT_HASH={md5_hash}"
                    checks.append({'check date': time_stamp, 'check type': 'filehash', 'status': status, 'message': message})
                    
            
            query = "SELECT `DNSorIP` FROM `servers`"
            mycursor.execute(query)
            dns_and_ips = mycursor.fetchall()

            for dnsip in dns_and_ips:
                server_for_ping = dnsip[0]
                result = pingthis(server_for_ping)
                if result[1] == 'Not found':
                    status= 'FAIL'
                else:
                    status = 'OK'
                
                message = f"TIME(MS)={result[1]}"
                checks.append({'check date': time_stamp, 'check type': 'pingcheck', 'status': status, 'message': f"SERVER={server_for_ping},{message}"})
            
            cpu_load = psutil.getloadavg()[0]      # check cpu_load 
            round_cpu = round(cpu_load,2)
            if cpu_load > 2.0:
                status = 'FAIL'
            else:
                status = 'OK'
            message = f"CPU_LOAD={round_cpu}"
            checks.append({'check date': time_stamp, 'check type': 'host-cpu', 'status': status, 'message': message})
            
            disk_usage = psutil.disk_usage('/')       #check disk_usage
            disk_percentage = int(round((disk_usage.used / disk_usage.total) * 100))
            if disk_percentage >= 85:
                status = 'FAIL'
            else:
                status = 'OK'
            message = f"DISK_USED={disk_percentage}%"  
            checks.append({'check date': time_stamp, 'check type': 'host-disk', 'status': status, 'message': message})
            
            mem = psutil.virtual_memory()          #check free memory
            mem_percentage = int(round((mem.available / mem.total) * 100))
            if mem_percentage <= 25:
                status = 'FAIL'
            else:
                status = 'OK'
            message = f"FREE_MEM={mem_percentage}%"
            checks.append({'check date': time_stamp, 'check type': 'host-mem', 'status': status, 'message': message})
            
            write_csv(checks)
            time.sleep(seconds_between_runs)
    except KeyboardInterrupt:
        print("Script interrupted. Closing database connection.")
        mydb.close() # Close the database connection at the end of the check_mode function

def write_csv(checks):
    with open('monitor4.csv', 'a', newline='')as csvfile:
        fieldnames = ['check date', 'check type', 'status', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        for check in checks:
            writer.writerow(check)

def insert_ipordns(ipordns): 
    mycursor, mydb = database_connection()
    query =  "SELECT * FROM `servers` WHERE `DNSorIP`= %s"
    mycursor.execute(query, (ipordns))
    result = mycursor.fetchone()
    if result:
        print("The IP address or dns you entered already exist")
        mydb.close()
    else:
        query = "INSERT INTO `servers` (`DNSorIP`) VALUES (%s)"
        mycursor.execute(query, (ipordns))
        mydb.commit()
        mydb.close()
def delete_ipordns(ipordns):
    mycursor, mydb = database_connection()
    query =  "SELECT * FROM `servers` WHERE `DNSorIP`= %s"
    mycursor.execute(query, (ipordns))
    result = mycursor.fetchone()
    if result:
        query = "DELETE FROM `servers` WHERE `DNSorIP`= %s"
        mycursor.execute(query, (ipordns))
        mydb.commit()
        mydb.close()
    else:
        print("The IP address or DNS you entered does not exist")
        mydb.close()


def main():
    if len(sys.argv) != 3 or (sys.argv[1] != 'updatehash' and sys.argv[1] != 'run' and sys.argv[1] != 'addserver' and sys.argv[1] != 'deleteserver'):
        print("Usage: ./monitor <cmd> <options> \nupdate hash mode: <cmd> is 'updatehash' and  <options> is the full path to the file (e.g. /etc/hosts)\nAuto check integrity mode: <cmd> is 'run' and <options> is number of seconds between runs\nadd server mode: <cmd> is 'addserver' and <options>  will be the server name or IP to add to the servers database table\ndeleteserver mode: <cmd> is 'deleteserver' and <options> will be the server name or IP to delete from the servers database table")
        sys.exit()
    if sys.argv[1] == 'updatehash':        #updatehash mode
        file_path = sys.argv[2]
        if not os.path.exists(file_path):
            print('File not found')
            sys.exit()

        md5_hash = calculate_md5(file_path)
        time_stamp = zulu_timestamp()
        insert_update_mysql_mode(md5_hash,time_stamp,file_path)
        
    elif sys.argv[1] == 'run':         #check mode
        seconds_between_runs = int(sys.argv[2])
        check_mode(seconds_between_runs)            
    elif sys.argv[1] == 'addserver':   #addserver mode
        ipordns = sys.argv[2]
        insert_ipordns(ipordns)
    elif sys.argv[1] == 'deleteserver':#deleteserver mode
        ipordns = sys.argv[2]
        delete_ipordns(ipordns)
        
if __name__ == "__main__":
    main()
