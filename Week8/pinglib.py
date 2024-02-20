#!/usr/bin/python3
# A python library for pinging an IP or domain name
# YW-20240220

import subprocess #This is used to run linux command" 
import sys #This is used to allow user interact with comand line"
import re #regular expression is used to extract ping time from dataset"
def pingthis(ipordns):
    """run ping command and return ip and ping time """
    try:
        result = subprocess.run(['ping', '-c', '1', ipordns], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            ping_time_search = re.search('time=(.*)ms', result.stdout)  #use re.search to find ping time match and extract as a standard output
            ping_time = round(float(ping_time_search.group(1)),2)  #After found the match, we need to define group(number) which is ping time. Also rounded 
            return [ipordns, ping_time]
        else:
            return [ipordns, f'Not found'] #if unreachable
    except Exception as a: 
        return [ipordns, f'Error Message: {str(a)}']

def main():
    """print IP and ping time. """
    if len(sys.argv) != 2:
        print("Usage: pinglib.py <IP|Domain name>")
        sys.exit()

    ipordns = sys.argv[1]
    result = pingthis(ipordns)
    print("IP, TimeToPing(ms)")
    print(f'{result[0]},{result[1]}')

if __name__ == "__main__":       #use to run script itself. When called by other script as lib, main() will not execute.
    main()
