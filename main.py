# # C:\Users\melvi\Downloads\VS_Code\Python\Car_Search

# import requests
# from bs4 import BeautifulSoup

# url = 'https://www.gumtree.com.au/s-cars-vans-utes/page-2/c18320?view=gallery'
  

# minimum_price = int(input("Enter the minimum price: ").strip())
# maximum_price = int(input("Enter the maximum price: ").strip())
# maximum_range = int(input("Enter the maximum range: ").strip())
# type = input("Enter the type of car (e.g., SUV, Sedan, Hatchback): ").strip()
# mode = input("Enter the mode (Auto, Manual): ").strip()

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# }

# for i in range(1, 2): 
#     current_url = f"https://www.gumtree.com.au/s-cars-vans-utes/page-{i}/c18320?view=gallery"
    
#     reponse = requests.get(current_url, headers=headers)
#     soup = BeautifulSoup(reponse.content, "html.parser")

#     cars = soup.find_all("div", class_="user-ad-square-new-design__content")

#     # Tags are duplicates so loop using indexing

        
#     for car in cars:
#         attr_container = car.find('ul', class_="user-ad-attributes")
#         if not attr_container:
#             continue

#         attributes = attr_container.find_all('li', class_="user-ad-attributes__attribute")  


#         price = car.find("span", class_="user-ad-price-new-design__price") # index later.....
#         char_price = price.text.strip()
#         mileage = attributes[0].text.strip()
#         type = attributes[1].text.strip()
#         mode = attributes[2].text.strip()

#         print(f"Price: {price}, Mileage: {mileage}, Type: {type}, Mode: {mode}")


from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time

# User Inputs
minimum_price = int(input("Enter the minimum price: ").strip())
maximum_price = int(input("Enter the maximum price: ").strip())
maximum_range = int(input("Enter the maximum range: ").strip())
target_type = input("Enter the type of car (e.g., SUV, Sedan, Hatchback): ").strip().lower()
target_mode = input("Enter the mode (Auto, Manual): ").strip().lower()

# Start Playwright automated browser context
with sync_playwright() as p:
    # Set headless=True to hide the window, or headless=False to watch it work!
    browser = p.chromium.launch(headless=False) 
    
    # Create a browser page that perfectly mimics a normal human window size
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    for i in range(1, 2): 
        current_url = f"https://www.gumtree.com.au/s-cars-vans-utes/page-{i}/c18320?view=gallery"
        
        print(f"\nOpening browser to fetch page {i}...")
        page.goto(current_url)
        
        # Give the page 4 seconds to fully load all elements and bypass security handshakes
        time.sleep(4)
        
        # Grab the raw HTML code directly from the live browser window
        html_content = page.content()
        soup = BeautifulSoup(html_content, "html.parser")

        # Flexible Target: Look for containers containing the ad layout classes
        cars = soup.find_all("div", class_=lambda x: x and 'user-ad-square-new-design__content' in x)
        
        print(f"--- Found {len(cars)} total car ads on page {i} ---")

        for car in cars:
            attr_container = car.find('ul', class_=lambda x: x and 'user-ad-attributes' in x)
            if not attr_container:
                continue

            attributes = attr_container.find_all('li', class_=lambda x: x and 'attribute' in x)  

            price_element = car.find("span", class_=lambda x: x and 'price' in x)
            if not price_element:
                continue
                
            char_price = price_element.text.strip()
            
            if len(attributes) >= 3:
                scraped_mileage = attributes[0].text.strip()
                scraped_type = attributes[1].text.strip()
                scraped_mode = attributes[2].text.strip()

                # --- DATA CLEAN-UP ---
                try:
                    clean_price = int(char_price.replace("$", "").replace(",", "").replace("Drive Away", "").replace("Negotiable", "").strip())
                    clean_mileage = int(scraped_mileage.lower().replace("km", "").replace(",", "").strip())
                except ValueError:
                    continue

                # --- FILTER EVALUATION ---
                if (minimum_price <= clean_price <= maximum_price and 
                    clean_mileage <= maximum_range and 
                    target_type in scraped_type.lower() and 
                    target_mode in scraped_mode.lower()):
                    
                    print(f"MATCH FOUND -> Price: {char_price}, Mileage: {scraped_mileage}, Type: {scraped_type}, Mode: {scraped_mode}")
                    
    # Clean up and close the browser instance down
    browser.close()