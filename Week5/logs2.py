#!/usr/bin/python3
# The script will create an output file called logs2.csv that will have columns for Mac Address, IP, and number of ACKs for that Mac Address at that IP
# YW-20240128
import sys
import csv 
import re
from collections import Counter

def analyze_logs(filename):
    """Read the log file and write log2.csv and problemMACs.csv"""
    ack_count_dict={}  #Create a dictionary 
    try:
        with open(filename, 'r') as file:
            for line in file:
                find = re.search("ACK (\S*) (\S*) to (\S*)", line)
                if find:
                    ip_address = find.group(2)
                    mac_address = find.group(3)
                    
                    key = mac_address + '-' + ip_address 
    
                    ack_count_dict[key]= ack_count_dict.get(key,0) + 1  #if mac and ip address exist, +1, else create this key and +1
    except FileNotFoundError:
        print(f"Log file not found, usage:logs2.py <filename>")
        sys.exit()
    
    with open('log2.csv', 'w') as fout:    #Write log2.csv file 
        csv_writer = csv.DictWriter(fout, fieldnames=['Macs', 'IPs', 'ACKs'], delimiter=' ') #csv.DictWriter is desgined for dictionary
        csv_writer.writeheader() #This will write fieldnames out"
        
        for mac_ip, ack_count in ack_count_dict.items():
            mac_address, ip_address = mac_ip.split('-') #because mac and ip address are in mac_address-ip_address, so i have to use .split('-') to split.
            csv_writer.writerow({'Macs': mac_address, 'IPs': ip_address, 'ACKs': ack_count})
    
    with open('ProblemMacs.csv', 'w') as fout:
        csv_writer = csv.DictWriter(fout, fieldnames=['Macs', 'IPs', 'ACKs'], delimiter=' ')
        csv_writer.writeheader()
        
        top2 = Counter(ack_count_dict).most_common(2) #I use Counter to find top2 ACK IP and MAC
            
        for key, ack_count in top2: 
            mac_address, ip_address = key.split('-')
            csv_writer.writerow({'Macs': mac_address, 'IPs': ip_address, 'ACKs': ack_count})

def main():
    filename = sys.argv[1]
    if len(sys.argv) != 2:
        print("Usage: logs1.py <filename>")
        sys.exit()
    
    analyze_logs(filename)

if __name__ == "__main__":
    main()

