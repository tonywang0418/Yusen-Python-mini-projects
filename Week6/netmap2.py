#!/usr/bin/python3
# The script will read netmap1.csv and detect OS
# YW-20240201 
import nmap3
import csv
import sys
def os_detect(filename):
    """Read the file and do a nmap os detection for each IP in the file """
    ip_list = [] #After read, store Ip and open ports inside the list
    with open(filename, 'r') as file:
        next(file)
        for line in file:
            ip_address =  line.split(',')[0].strip()
            open_ports = line.split(',')[1].strip()
            ip_list.append((ip_address,open_ports))
    

    with open ('netmap2.csv', 'w') as fout: 
        csv_writer = csv.writer(fout, quoting=csv.QUOTE_NONE)
        csv_writer.writerow(['IP', 'Open Ports', 'OS'])
        for ip, open_ports in (ip_list):
            nmap = nmap3.Nmap()
            os_results = nmap.nmap_os_detection(ip) #nmap os detection 
            for key,value in os_results.items():
                if 'osmatch' in value and value['osmatch']:
                    first_osmatch = value['osmatch'][0]['name']  #best guess as to the OS of the server
                    csv_writer.writerow([ip, open_ports, first_osmatch])
    

def main():
    filename = sys.argv[1]
    if len(sys.argv) != 2:
        print("Usage: netmap2.py <input file name>")
        sys.exit()

    os_detect(filename)

if __name__ == "__main__":
    main()
