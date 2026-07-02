# # C:\Users\melvi\Downloads\VS_Code\Python\Car_Search

# import requests
# from bs4 import BeautifulSoup

# URLs = [
#     'https://www.gumtree.com.au/s-cars-vans-utes/page-1/c18320?view=gallery'
#     'https://www.ebay.com.au/b/Cars/29690/bn_1843284',
#     'https://www.carsales.com.au/cars/victoria-state/'
#     ]

# minimum_price = int(input("Enter the minimum price: ").strip())
# maximum_price = int(input("Enter the maximum price: ").strip())
# maximum_range = int(input("Enter the maximum range: ").strip())
# type = input("Enter the type of car (e.g., SUV, Sedan, Hatchback): ").strip()
# mode = input("Enter the mode (Auto, Manual): ").strip()
# year = int(input("Enter the year of the car: ").strip())

# for url in URLs:
#     for i in range(1, 10): 
#         current_url = f"https://www.gumtree.com.au/s-cars-vans-utes/page-{i}/c18320?view=gallery"
        
#         reponse = requests.get(current_url)
#         soup = BeautifulSoup(reponse.content, "html.parser")

#         cars = soup.find_all("a", class_="user-ad-square-new-design")

#         for car in cars:
#             cars = soup.find_all("div", class_="user-ad-square-new-design__content")

#             price = soup.find_all("span", class_="user-ad-price-new-design__price")
            
#             title = soup.find_all('span', class_="user-ad-square-new-design__title")


            

from bs4 import BeautifulSoup
import requests

# Paste your copied Gumtree search URL here
url = "https://www.gumtree.com.au/web/listing/cars-vans-utes/1343171989"

# Storage for your chart coordinates (X, Y points)
graph_data = []

# Headers mimic a real browser request to ensure the site answers smoothly
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
r = requests.get(url, headers=headers)

if r.status_code == 200:
    soup = BeautifulSoup(r.text, "html.parser")

    # 1. Target every single car listing box on the page
    car_listings = soup.find_all("article", attrs={"data-q": "search-result"})

    for car in car_listings:
        try:
            # 2. Extract the raw text elements
            price_element = car.find(attrs={"data-q": "search-result-price"})

            # Note: For odometer, look for the text containing 'km' within the listing details
            details_text = car.get_text()

            # Safe check to make sure the elements aren't empty
            if price_element:
                raw_price = price_element.text  # e.g., "$15,490"

                # Parse the odometer reading directly from the text block
                # (Loops through words to isolate the one ending in 'km')
                raw_mileage = "0"
                for word in details_text.split():
                    if "km" in word.lower() and any(
                        char.isdigit() for char in word
                    ):
                        raw_mileage = word
                        break

                # 3. CONVERT TEXT INTO GRAPH POINTS (The mathematical clean-up)
                cleaned_price = int(
                    raw_price.replace("$", "")
                    .replace(",", "")
                    .replace("Negotiable", "")
                    .strip()
                )
                cleaned_mileage = int(
                    raw_mileage.lower()
                    .replace("km", "")
                    .replace(",", "")
                    .strip()
                )

                # Skip anomalies (like an accidentally typed 0km or a $0 price)
                if cleaned_price > 0 and cleaned_mileage > 0:

                    # 4. SAVE AS GRAPH COORDINATE PAIR: { X: Mileage, Y: Price }
                    point = {"mileage": cleaned_mileage, "price": cleaned_price}
                    graph_data.append(point)

        except Exception as e:
            # Skip any single malformed ad card so the program keeps running
            continue

# Print your gathered dataset points in the terminal
print(f"Successfully collected {len(graph_data)} graph points!")
print("Here are your raw data coordinates ready for the plotting step:")
print(graph_data)