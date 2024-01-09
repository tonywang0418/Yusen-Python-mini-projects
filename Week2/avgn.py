#!/usr/bin/python3
# This script is use to calculate average of three numbers
# YW-20240108
import sys  # sys is built-in module use to make interation with command-line aruguments

def calculate_average(numbers):
    """This function is use for average calculation and quit if input is empty"""
    if not numbers:
        print("empty input, usage: <number> <numer> ... Must be positive numbers.")
        return sys.exit()
    
    return sum(numbers) / len(numbers)

def main():
    """ print the average or exit if numbers are not float or postive"""
    
    try:
        numbers = [float(arg) for arg in sys.argv[1:]]
    except ValueError:
        print("invalid input, usage: <number>, <number>, ... Must be positive numbers")
        return sys.exit()
    
    
    for num in numbers:
        if num < 0:
            print("please enter postive number. usage: <number>, <number>, ...  Must be positive numbers")
            return sys.exit()
    
    average= calculate_average(numbers)
    print("average: ", round(average, 2))
if __name__ == "__main__":
    main()
