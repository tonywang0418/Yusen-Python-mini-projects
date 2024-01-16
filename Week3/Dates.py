#!/usr/bin/python3
# Script takes arguments on the command line for the birthdate and the number of days to add to it.
# YW-20240115
# Set up initial variables and imports

import sys   # sys is built-in module use to make interation with command-line aruguments
from datetime import datetime, timedelta   #dateime is a built-in module for getting time, timedelta is used to make time calculatioin.

def calculate_days(birthdate_dt, days):
    """This function is used to calculate birthdate + the days you want to be added"""
    adding = birthdate_dt + timedelta(days=days) #timedelta allows date calcuation, seconds,hours, days...
    return adding

def main(): 
    """Exceptions and run the script """
    if len(sys.argv) != 3:      #Check to make sure user input 3 arugments
        print("LUsage: Date.py mm-dd-yyyy days  Must be postive integer ")
        return sys.exit()
    birthdate, days = sys.argv[1], sys.argv[2]     #define each arugments
    
    try:
       birthdate_dt = datetime.strptime(birthdate, "%m-%d-%Y")  #convert birthdate string into datetime, so it check format and month, day and years based on the datetie(datetime module can handle leap year possiblity)  
    except ValueError:
        print("BFUsage: Date.py mm-dd-yyyy days  Must be postive integer ")
        return sys.exit()

    try:    #Check if days is integer
        days= int(days)
    except ValueError:
        print("DFUsage: Date.py mm-dd-yyyy days  Must be postive integer ")
        return sys.exit()
    
    if days <= 0:    #Check if days is postive
        print("DNUsage: Date.py mm-dd-yyyy days  Must be postive integer")
        return sys.exit()

    print(f"Person born on {birthdate} will have their {days} birthday on {calculate_days(birthdate_dt, days).strftime('%m-%d-%Y')}.")

if __name__ == "__main__":
    main()

