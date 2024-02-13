#!/usr/bin/python3
# A script that connects to the database and prints out the data in the devices table to either csv and json formatted files depending on the script argument
# YW-202402013
import pymysql
import csv
import json
import sys
#server connection
mydb = pymysql.connect(host='localhost', user='cmdb', password='sec444bc', database='cmdb')
mycursor = mydb.cursor() #creates cursor object used for CREATE, RETRIEVE, UPDATE AND DELETE.
mycursor.execute('SELECT * FROM device')
rows = mycursor.fetchall() #fetches all rows of a query result set and returns a list of tuples
mycursor.close()
def export_json():
    json_list=[]
    for row in rows:
        json_list.append({'name':row[0], 'macaddress':row[1],
            'ip':row[2], 'cpucount':row[3],'disks':row[4],
            'ram':row[5], 'ostype':row[6], 'osversion':row[7]})
    with open('database2.json', 'w') as jfile:
        json.dump(json_list, jfile)
    
def export_csv():    
    with open('database2.csv', 'w') as csvfile:
        csv_writer= csv.writer(csvfile)
        csv_writer.writerow(['name', 'macaddress', 'ip', 'cpucount', 'disks', 'ram', 'ostype', 'osversion'])
        csv_writer.writerows(rows)

    

def main():
    if len(sys.argv) != 2:
        print("Usage: ./database2.py <json|csv>")
        sys.exit()
    file_format = sys.argv[1]
    if file_format == 'json':
        export_json()
    else:
        export_csv()
if __name__ == "__main__":
    main()
