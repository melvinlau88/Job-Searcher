# C:\Users\melvi\Downloads\VS_Code\Python\Car_Search

import requests
from bs4 import BeautifulSoup

url = 'https://www.gumtree.com.au/s-cars-vans-utes/page-2/c18320?view=gallery'
  

minimum_price = int(input("Enter the minimum price: ").strip())
maximum_price = int(input("Enter the maximum price: ").strip())
maximum_range = int(input("Enter the maximum range: ").strip())
type = input("Enter the type of car (e.g., SUV, Sedan, Hatchback): ").strip()
mode = input("Enter the mode (Auto, Manual): ").strip()



for i in range(1, 2): 
    current_url = f"https://www.gumtree.com.au/s-cars-vans-utes/page-{i}/c18320?view=gallery"
    
    reponse = requests.get(current_url)
    soup = BeautifulSoup(reponse.content, "html.parser")

    cars = soup.find_all("div", class_="user-ad-square-new-design__content")

    # Tags are duplicates so loop using indexing

        
    for car in cars:
        attr_container = car.find('ul', class_="user-ad-attributes")
        if not attr_container:
            continue

        attributes = attr_container.find_all('li', class_="user-ad-attributes__attribute")  


        price = car.find("span", class_="user-ad-price-new-design__price") # index later.....
        char_price = price.text.strip()
        mileage = attributes[0].text.strip()
        type = attributes[1].text.strip()
        mode = attributes[2].text.strip()

        print(f"Price: {price}, Mileage: {mileage}, Type: {type}, Mode: {mode}")