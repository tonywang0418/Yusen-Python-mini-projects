#!/usr/bin/python3
# Script takes one argument and an optional CSV output file on the command line like so: ping1.py <filename> <output.csv>
# YW-20240124
from pinglib import pingthis
import sys
import csv

def main():
    """ open the file in read mode and .read and return as a list. Finally print output """
    if len(sys.argv) < 2 or len(sys.argv) > 3:  #optional argument     
        print("Usage: ping1.py <filename | IP | Domainname> <output.csv>")
        print("Output.csv is optional")
        sys.exit()

    target = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else None  

    try:
        """if enter a ping file """
        with open(target, 'r') as file:
            addresses = file.read().splitlines() # .read the file as a string and use splitlines to split the string at '\n' line break and made a list [].
        print("IP, TimeToPing (ms)")
        for line in addresses:
            result = pingthis(line)     #apply ip address to my pinglib
            print(f'{result[0]}, {result[1]}') #display in this format
        if output_file:       #if csv argument exist
            with open(output_file, 'w', newline='') as fout:
                csv_writer = csv.writer(fout) #write on this file
                csv_writer.writerow(['IP, TimeToPing (ms)']) 
                for line in addresses:
                    result = pingthis(line)     #apply ip address to my pinglib
                    csv_writer.writerow(result)
    
                
    except FileNotFoundError:
        """if enter ip or dns  """
        result = pingthis(target)
        print("IP, TimeToPing (ms)")
        print(f'{result[0]}, {result[1]}') # if file not found, treat it as IP or domain name.
        
        if output_file:
            result = pingthis(target)
            with open(output_file, 'w', newline='') as fout:
                csv_writer = csv.writer(fout)
                csv_writer.writerow(['IP, TimeToPing (ms)'])
                csv_writer.writerow(result)
                

if __name__ == "__main__":
    main()
