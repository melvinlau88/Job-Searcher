# C:\Users\melvi\Downloads\VS_Code\Python\Car_Search

import requests
from bs4 import BeautifulSoup

url = 'https://www.ebay.com.au/b/Cars/29690/bn_1843284',
  

minimum_price = int(input("Enter the minimum price: ").strip())
maximum_price = int(input("Enter the maximum price: ").strip())
maximum_range = int(input("Enter the maximum range: ").strip())
type = input("Enter the type of car (e.g., SUV, Sedan, Hatchback): ").strip()
mode = input("Enter the mode (Auto, Manual): ").strip()
year = int(input("Enter the year of the car: ").strip())

for i in range(1, 10): 
    current_url = f"https://www.gumtree.com.au/s-cars-vans-utes/page-{i}/c18320?view=gallery"
    
    reponse = requests.get(current_url)
    soup = BeautifulSoup(reponse.content, "html.parser")

    cars = soup.find_all("a", class_="user-ad-square-new-design")
    cars = soup.find_all("div", class_="user-ad-square-new-design__content")

    # Tags are duplicates so loop using indexing
    attributes = car.find_all('li', class_="user-ad-attributes_attribute user-ad-square-new-design__attribute")
    for car in cars:
        price = soup.find("span", class_="user-ad-price-new-design__price").text.strip()
        year = soup.find("span", class_="user-ad-price-new-design__title").text.strip()   # index later.....
        mileage = attributes[0].text.strip()
        type = attributes[1].text.strip()
        mode = attributes[2].text.strip()




        
        

    