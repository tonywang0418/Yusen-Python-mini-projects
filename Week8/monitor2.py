#!/usr/bin/python3
#
# YW-20240218
import os
import sys
import pymysql
from datetime import datetime
import hashlib
import csv
import time
#server connection
mydb = pymysql.connect(host='localhost', user='cmdb', password='sec444bc', database='cmdb') #Another database connection function is in main()
mycursor = mydb.cursor() #creates cursor object used for CREATE, RETRIEVE, UPDATE AND DELETE.
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
    return datetime.utcnow()
def insert_update_mysql(md5_hash,time_stamp,file_path):
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
    
def write_csv(checks):
    with open('monitor2.csv', 'a', newline='')as csvfile:
        fieldnames = ['check date', 'check type', 'status', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        for check in checks:
            writer.writerow(check)
def main():
    if len(sys.argv) != 3 or (sys.argv[1] != 'updatehash' and sys.argv[1] != 'run'):
        print("Usage: ./monitor <cmd> <options> \n<cmd> is 'updatehash' and  <options> is the full path to the file (e.g. /etc/hosts)\n<cmd> is 'run' and <options> is number of seconds between runs")
        sys.exit()
    if sys.argv[1] == 'updatehash':
        file_path = sys.argv[2]
        if not os.path.exists(file_path):
            print('File not found')
            sys.exit()

        md5_hash = calculate_md5(file_path)
        time_stamp = zulu_timestamp()
        insert_update_mysql(md5_hash,time_stamp,file_path)
        
    
    elif sys.argv[1] == 'run':
        while True:
            seconds_between_runs = int(sys.argv[2])
            mydb = pymysql.connect(host='localhost', user='cmdb', password='sec444bc', database='cmdb')#Database info
            mycursor = mydb.cursor()
            
            query = "SELECT `path` FROM `files`"    #This chunk is for selecting all path in database
            mycursor.execute(query)
            file_paths = mycursor.fetchall() #fetch them into a tuple 
            
            checks = []  #Create a list for csv 
            for path in file_paths: #loop over each file path
                file_path = path[0]
                
                if os.path.exists(file_path):
                    old_time_query="SELECT `timestamp` FROM `files` WHERE `path` = %s"  #This chunk is for old timestamp
                    mycursor.execute(old_time_query, (file_path))
                    old_time=mycursor.fetchone()[0]
                    
                    status = 'OK'
                    query = "SELECT `hash` FROM `files` WHERE `path` = %s"  #This chunk is for old hash
                    mycursor.execute(query, (file_path))
                    old_hash = mycursor.fetchone()[0]

                    md5_hash = calculate_md5(file_path)   #New hash 
                    time_stamp = zulu_timestamp()         #New Timestamp
                    insert_update_mysql(md5_hash,time_stamp,file_path) #update or insert file
                    
                    if old_hash != md5_hash: 
                        status = 'FAIL'
                    
                    message = f"FILE={file_path}, OLD_HASH={old_hash}, OLD_HASH_DATE= {old_time}, CURRENT_HASH={md5_hash}"
                    checks.append({'check date': time_stamp, 'check type': 'filehash', 'status': status, 'message': message})
            mydb.close() #close connection for 'run' mode
            write_csv(checks)
            time.sleep(seconds_between_runs)
        mydb.close() #close connection for 'updatehash' mode

        
if __name__ == "__main__":
    main()
