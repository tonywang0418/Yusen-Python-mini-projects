#!/usr/bin/python3
# the script will create an output file called netmap3.csv that will have the DNS names it finds in the first column and the IPs in a second column
# YW-20240206
import nmap3
import sys
import csv
def dns_brute(domain_name):
    """run a dns brute scan to guess DNS names and write out as a csv file """
    list = [] 
    nmap = nmap3.Nmap()
    results = nmap.nmap_dns_brute_script(domain_name)
    for item in results:
        age = item ['address']
        hostname = item['hostname']
        if ':' not in age:
            list.append((hostname, age))

    with open('netmap3.csv', 'w')as fout:
        csv_writer = csv.writer(fout)
        csv_writer.writerow(['DNS', 'IP','Services'])
        for DNS, IP in list:
            csv_writer.writerow([DNS,IP])



def main():
    if len(sys.argv) != 2:
        print("Usage: netmap3.py <domain name>")
        sys.exit()
    domain_name = sys.argv[1]
    dns_brute(domain_name)

if __name__ == "__main__":
    main()


