#!/usr/bin/python3
# script will create an output file called logs1.txt that will have only the iPhone mac addresses in it and at the bottom, a count of the total number of unique addresses
# YW-20240128
import sys
import csv 
import re

def findiphonemac(filename):
    """Read the log file and find iphone mac adddresses"""
    macs=[]

    with open(filename, 'r') as file:
        for line in file:
            find = re.search("from (\S*) \(iPhone", line)
            if find:
                mac_address = find.group(1)
                if mac_address not in macs:  #Make sure there are no repeat mac addresses
                    macs.append(mac_address)
    return macs


def main():
    """Write the file into csv format and print"""
    log_file = sys.argv[1]
    iphone_macs = findiphonemac(log_file)
    
    if len(sys.argv) != 2:
        print("Usage: logs1.py <filename>")
        sys.exit()


    with open('log1.csv', 'w') as fout:
        csv_writer = csv.writer(fout)
        for mac_address in iphone_macs:
            print(mac_address)
            csv_writer.writerow([mac_address])
        csv_writer.writerow(['Count = ' + str(len(iphone_macs))])
        print(f'Count = ', len(iphone_macs))

if __name__ == "__main__":
    main()


