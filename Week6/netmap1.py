#!/usr/bin/python3
# The script will do a syn scan only of 152.157.64.0/24
# YW-20240201
#import nmap3 
import nmap3
import csv
def syn_scan(target):
    """syn nmap and write as a csv file """
    nmap = nmap3.NmapScanTechniques()
    result = nmap.nmap_syn_scan(target)

    with open('netmap1.csv', 'w')as fout:
        csv_writer = csv.writer(fout, quoting=csv.QUOTE_NONE)
        csv_writer.writerow(['IP', 'Open Ports']) 
        for key, value in result.items():              
            if 'ports' in value and value['ports']:   #check if the key ports exist and value not empty  
                open_ports = [port_info['portid'] for port_info in value['ports'] if port_info['state'] == 'open']
                csv_writer.writerow([key, ' '.join(open_ports)])


def main():
    target = "152.157.64.0/24"
    syn_scan(target)

if __name__ == "__main__":
    main()
