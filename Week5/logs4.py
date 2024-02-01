#!/usr/bin/python3
#  Take the name of the file on the command line, find all the servers that connected to this email server, and write out a csv file named 'servers.csv'
# YW-20240201
import sys 
import csv
import re

def analyze_logs(mail_log):
    """Read mail logfile and find serverename and corresponding IPs """
    server_ip = {}
    try:
        with open(mail_log, "r") as logfile:
            for line in logfile:
                match = re.search("client=(\S+)\[(.*)]", line)
                if match:
                    server_name = match.group(1)
                    ip_address = match.group(2)
                    key = server_name
                    if server_name not in server_ip:
                        server_ip[key] = [ip_address]
    except FileNotFoundError:
        print(f"Log file not found, usage: logs4.py <mail log file>")
        sys.exit()
    
    with open('log4.csv', 'w')as fout:
        csv_writer = csv.DictWriter(fout, fieldnames=['ServerName','IP'], delimiter =' ')
        csv_writer.writeheader()
        for key, value in server_ip.items():
            csv_writer.writerow({'ServerName': f"{key}," , 'IP': value[0]})
    print(server_ip)

def main():
    mail_log = sys.argv[1]
    if len(sys.argv) != 2:
        print("Usage: logs4.py <mail log file>")
        sys.exit()

    analyze_logs(mail_log)

if __name__ == "__main__":
    main()
