#!/usr/bin/python3
# The script will create an output file called logs3.csv that will have columns for IP, Mac address, and vendor associated with the mac address
# YW-20240128
import sys
import csv 
import re
import requests
import time

def analyze_logs(filename_ips, dhcp_logfile):
    """Read the log file and write log3.csv"""
    ipmac_dict= {}  #Create a dictionary with ipaddress and macaddress followed with vendor
    ip_searchlist = []      #create ip searchlist
    
    with open(filename_ips, 'r') as ipfile:
        ips =  ipfile.read().splitlines()
        ip_searchlist= ips           #read the ip list and put it into ip_searchlist
    try:
        with open(dhcp_logfile, 'r') as file:                   
            for line in file:
                for ip in ip_searchlist:
                    find = re.search(f"{ip} (\S*) (\S*)", line)
                    if find:
                        ip_address = ip
                        mac_address = find.group(2)
                        key = ip_address
                        if key not in ipmac_dict:        #To avoid repeat
                            vendor_url = f'https://api.macvendors.com/{mac_address}'
                            response = requests.get(vendor_url)
                            time.sleep(1)         #API request can't be too fast..
                            vendor = response.text.strip() #ouput vendor result
                        

                            ipmac_dict[key]= [ip_address, mac_address, vendor] #add them to dictioanry 
                         
    except FileNotFoundError:
        print(f"Log file not found, usage:logs3.py <filename of IPs> <dhcpd log file>")
        sys.exit()

    
    with open('log3.csv', 'w') as fout:
        csv_writer = csv.DictWriter(fout, fieldnames=['IP', 'MacAddress', 'Vendor'], delimiter=' ')
        csv_writer.writeheader()
        
        for ip_address, mac_address,vendor in ipmac_dict.values(): 
            csv_writer.writerow({'IP': ip_address, 'MacAddress': mac_address, 'Vendor': vendor})

def main():
    if len(sys.argv) != 3:
        print("Usage: logs3.py <filename of IPs> <dhcpd log file>")
        sys.exit()
    filename_ips = sys.argv[1]
    dhcp_logfile = sys.argv[2]
    
    analyze_logs(filename_ips, dhcp_logfile) 

if __name__ == "__main__":
    main()
