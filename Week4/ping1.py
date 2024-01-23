#!/usr/bin/python3
# Script takes one arguments on the command line like so: ping1.py <filename>
# YW-20240123
from pinglib import pingthis
import sys 

def main():
    """ open the file in read mode and .read and return as a list. Finally print output """
    if len(sys.argv) != 2:
        print("Usage: ping1.py <filename>")
        sys.exit()

    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            addresses = file.read().splitlines() # .read the file as a string and use splitlines to split the string at '\n' line break and made a list [].

            print("IP, TimeToPing (ms)")
            for line in addresses:
                result = pingthis(line)     #apply ip address to my pinglib
                print(f'{result[0]}, {result[1]}') #display in this format
    except FileNotFoundError:
        print(f'File not found')

if __name__ == "__main__":
    main()
