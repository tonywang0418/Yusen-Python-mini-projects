#!/usr/bin/python3
# This script is use to calculate average of three numbers
# YW-20240108
# Set up initial variables and imports

import sys    # sys is built-in module use to make interation with command-line aruguments

def calculate_average(num1, num2, num3):
    """This function is use for average calculation"""
    return (num1 + num2 + num3) / 3

# This is called when script is run
def main():
    if len(sys.argv) != 4:   # Exception: if user input exceed the limit of 3 numbers it will exit and prompt the usage 
        print("invalid input, usage: <number>, <number>, <number>  Must have three positive numbers")
        return sys.exit()
    try:                     # Exception: if user input not float it will exit and prompt the usage
        num1 = float(sys.argv[1])
        num2 = float(sys.argv[2])
        num3 = float(sys.argv[3])
    except ValueError:
        print("invalid input, usage: <number>, <number>, <number>  Must have three positive numbers")
        return sys.exit()
    
    if num1 <= 0 or num2 <= 0 or num3 <= 0:   # Exception:: if user input small or equal to 0 it will exit and prompt the usage
        print("usage: <number>, <number>, <number>  Must have three positive numbers")
        return sys.exit()
    
    average= calculate_average(num1, num2, num3)
    print("average: ", round(average, 2))     # Print the output rounded with 2 decimal

if __name__ == "__main__":
    main()              # run main()
    
        
    
