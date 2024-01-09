#!/usr/bin/python3
# This script will prompt for a user name and then for their favorite color.
# YW-20240108

def main():
    """This function ask for username and color. It will check for letters, it will prompt error message if its not letter"""
    while True:
        name = input(str("Please enter your user name: "))
        if name.isalpha():
            break
        else:
            print("Please enter only letters.")
    while True:
        color = input(str("Please enter your color name: "))
        if color.isalpha():
            break   
        else:
            print("Please enter only letters.")
        
        
    print(f"Your name is {name} and your favorite color is {color}")
main()
