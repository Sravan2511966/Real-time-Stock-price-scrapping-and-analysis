import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import certifi

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}

urls = [
    'https://groww.in/us-stocks/nke',
    'https://groww.in/us-stocks/ko', 
    'https://groww.in/us-stocks/msft',  
    'https://groww.in/us-stocks/axp', 
    'https://groww.in/us-stocks/amgn', 
    'https://groww.in/us-stocks/aapl', 
    'https://groww.in/us-stocks/ba', 
    'https://groww.in/us-stocks/csco', 
    'https://groww.in/us-stocks/gs', 
    'https://groww.in/us-stocks/ibm', 
    'https://groww.in/us-stocks/intc', 
    'https://groww.in/us-stocks/jpm', 
    'https://groww.in/us-stocks/mcd',
    'https://groww.in/us-stocks/crm', 
    'https://groww.in/us-stocks/vz', 
    'https://groww.in/us-stocks/v', 
    'https://groww.in/us-stocks/wmt',  
    'https://groww.in/us-stocks/dis'
]

all_data = []

for url in urls:
    try:
        page = requests.get(url, headers=headers, verify=certifi.where())
        page.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(page.text, 'html.parser')
        
        try:
            company = soup.find('h1', {'class': 'usph14Head displaySmall'}).text.strip()
            print(f"Company: {company}")
        except AttributeError:
            company = 'N/A'
            print("Company not found")
        
        try:
            price_elements = soup.find_all('td', class_='col l3 bodyLargeHeavy')
            if len(price_elements) >= 3:
                price = price_elements[0].text.strip()
            else:
                price = 'N/A'
                print("Price label not found")
            print(f"Price: {price}")
        except AttributeError:
            price = 'N/A'
            print("Price not found")
        
        try:
            change_element = soup.find('div', {'class': 'uht141Day bodyBaseHeavy contentNegative'})
            if change_element is None:
                change_element = soup.find('div', {'class': 'uht141Day bodyBaseHeavy contentPositive'})
            change = change_element.text.strip() if change_element else 'N/A'
            # Remove the trailing "1D" from the change value
            change = change.replace("1D", "").strip()
            print(f"Change: {change}")
        except AttributeError:
            change = 'N/A'
            print("Change not found")
        
        try:
            elements = soup.find_all('td', class_='col l3 bodyLargeHeavy')
            if len(elements) >= 3:
                volume = elements[2].text.strip()
            else:
                volume = 'N/A'
                print("Volume not found")
            print(f"Volume: {volume}")
        except (AttributeError, IndexError):
            volume = 'N/A'
            print("Volume not found")
        
        all_data.append([company, price, change, volume])
        
        # Wait for a short time to avoid rate limiting
        time.sleep(5)
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")

column_names = ["Company", "Price", "Change", "Volume"]
df = pd.DataFrame(all_data, columns=column_names)
df.to_excel('stocks.xlsx', index=False)

print("Data has been successfully scraped and saved to stocks.xlsx")

# Display the DataFrame
df