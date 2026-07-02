# C:\Users\melvi\Downloads\VS_Code\Python\Car_Search

import requests
from bs4 import BeautifulSoup

URLs = [
    'https://www.gumtree.com.au/s-cars-vans-utes/page-1/c18320?view=gallery'
    'https://www.ebay.com.au/b/Cars/29690/bn_1843284',
    'https://www.carsales.com.au/cars/victoria-state/'
    ]

minimum_price = int(input("Enter the minimum price: ").strip())
maximum_price = int(input("Enter the maximum price: ").strip())
maximum_range = int(input("Enter the maximum range: ").strip())
type = input("Enter the type of car (e.g., SUV, Sedan, Hatchback): ").strip()
mode = input("Enter the mode (Auto, Manual): ").strip()
year = int(input("Enter the year of the car: ").strip())

