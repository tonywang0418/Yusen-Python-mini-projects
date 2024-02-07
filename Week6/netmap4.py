#!/usr/bin/python3
# The script will create an output file called netmap4.csv that is the same as netmap3.csv with location data added
# YW-20240206
import sys
import csv
import requests
import json
def dns_brute(filename):
    """read the file and use API to find geo info and write out as a csv file """ 
    with open(filename, 'r') as file:
        next(file)
        reader = csv.reader(file)

        with open('netmap4.csv', 'w')as fout:
            csv_writer = csv.writer(fout)
            csv_writer.writerow(['DNS', 'IP', 'Services', 'Country', 'RegionName', 'City', 'Zipcode', 'ISP'])
            for row in reader:

                ip_address = row[1]
                geo_API = f'http://ip-api.com/json/{ip_address}?fields=country,regionName,city,zip,timezone,isp'
                response = requests.get(geo_API)
                results = response.text.strip()
                data_dict = json.loads(results) #Parse json and write a dictionary 
                
                country = data_dict.get('country')
                region_name = data_dict.get('regionName')
                city = data_dict.get('city')
                Zipcode = data_dict.get('zip')
                timezone = data_dict.get('timezone')
                isp = data_dict.get('isp')
                row.extend((country, region_name,city,Zipcode,timezone,isp))
                csv_writer.writerow(row)
                       

def main():
    if len(sys.argv) != 2:
        print("Usage: netmap4.py <input file name>")
        sys.exit()
    filename = sys.argv[1]
    dns_brute(filename)

if __name__ == "__main__":
    main()
