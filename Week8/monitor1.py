#!/usr/bin/python3
# This script needs to create a MD5 hash of the file and add the timestamp in zulu time, the file path, and the hash to a database table in the mysql server# YW-20240218
import os
import sys 
import pymysql
from datetime import datetime
import hashlib
#server connection
mydb = pymysql.connect(host='localhost', user='cmdb', password='sec444bc', database='cmdb')
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
    mydb.close()

def main():
    if len(sys.argv) != 3 or sys.argv[1] != 'updatehash':
        print("Usage: ./monitor <cmd> <options> \n<cmd> is 'updatehash' and  <options> is the full path to the file (e.g. /etc/hosts)")
        sys.exit()
    file_path = sys.argv[2]

    if not os.path.exists(file_path):
       print('File not found')
       sys.exit()
    
    md5_hash = calculate_md5(file_path)
    time_stamp = zulu_timestamp()
    insert_update_mysql(md5_hash,time_stamp,file_path)

if __name__ == "__main__":
    main()
