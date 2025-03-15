The aim of the project is to extract the data from the stock websites and store it in an excel sheet using web scrapping  to give an overview of the stock prices to the investors.

Step  1: Import required libraries
- requests: Fetches web pages from the internet.  
- BeautifulSoup: Parses the HTML content of the web pages.  
- pandas: Stores the extracted data in a structured format (DataFrame).  
- time: Adds delays between requests to avoid being blocked.  
- certifi: Provides SSL certificates to ensure secure requests.
  
Step 2: Define Headers 
- The headers dictionary is created to simulate a real web browser request by providing a *User-Agent string*.  
- This helps bypass basic anti-scraping measures used by websites.  

python:

headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...'}

Step 3: Define URLs of Stocks
- A list of URLs of different *US stocks* on the Groww website is stored in the urls list.  

python:

urls = [
    'https://groww.in/us-stocks/nke',
    'https://groww.in/us-stocks/ko', 
    ...
]

Step 4: Initialize an Empty List
- all_data = [] is created to store extracted stock information.  


Step 5: Loop Through Each URL 
For each stock URL:  
1. *Send an HTTP GET Request*  
   - Uses requests.get(url, headers=headers, verify=certifi.where()) to fetch the webpage.  
   - verify=certifi.where() ensures SSL verification.  

2. *Check for Errors*  
   - page.raise_for_status() stops execution if there’s an HTTP error (e.g., 404, 500).  

python:

try:
    page = requests.get(url, headers=headers, verify=certifi.where())
    page.raise_for_status()

Step 6: Parse the Webpage HTML 
- BeautifulSoup is used to parse the page content.  

python:

soup = BeautifulSoup(page.text, 'html.parser')



Step 7: Extract Required Data
1. *Extract Company Name*  
   - Looks for an  element with class 'usph14Head displaySmall'.  
   - If not found, assigns "N/A".  

python:

company = soup.find('h1', {'class': 'usph14Head displaySmall'}).text.strip()


2. *Extract Stock Price* 
   - Finds all <td> elements with class 'col l3 bodyLargeHeavy'.  
   - The first element ([0]) contains the stock price
  python:

price_elements = soup.find_all('td', class_='col l3 bodyLargeHeavy')
if len(price_elements) >= 3:
    price = price_elements[0].text.strip()


3. *Extract Price Change (1-Day Change)*  
   - Searches for a <div> containing either 'contentNegative' or 'contentPositive' (depending on whether the stock is down or up).  
   - Removes "1D" from the text.  

python:

change_element = soup.find('div', {'class': 'uht141Day bodyBaseHeavy contentNegative'})
if change_element is None:
    change_element = soup.find('div', {'class': 'uht141Day bodyBaseHeavy contentPositive'})
change = change_element.text.strip().replace("1D", "").strip() if change_element else 'N/A'

4. *Extract Trading Volume*  
   - Uses the same <td> elements as the price.  
   - The **third element ([2])** represents the stock’s trading volume.  

python:

elements = soup.find_all('td', class_='col l3 bodyLargeHeavy')
if len(elements) >= 3:
    volume = elements[2].text.strip()



Step 8: Store the Extracted Data
- The extracted company, price, change, volume is appended to the all_data list.  

python:

all_data.append([company, price, change, volume])


Step 9: Pause to Avoid Rate Limiting 
- Waits *5 seconds* before scraping the next URL to prevent blocking.  

python:

time.sleep(5)



Step 10: Handle Request Errors
- If any error occurs (network issue, invalid URL, website blocking), it prints an error message and moves to the next URL.  

python:

except requests.exceptions.RequestException as e:
    print(f"Error fetching {url}: {e}")

 Step 11: Store Data in an Excel File 
- Creates a *Pandas DataFrame* with column names "Company", "Price", "Change", "Volume".  
- Saves the data to *stocks.xlsx*.  

python:

column_names = ["Company", "Price", "Change", "Volume"]
df = pd.DataFrame(all_data, columns=column_names)
df.to_excel('stocks.xlsx', index=False)



Step 12: Display the Data 
- Prints "Data has been successfully scraped and saved to stocks.xlsx" and displays the DataFrame.  

python:

print("Data has been successfully scraped and saved to stocks.xlsx")
df

Final Outcome: 
- Extracts stock data (Company Name, Price, Change, Volume) from Groww.  
- Saves it to an *Excel file* (stocks.xlsx).  
- Displays the collected data in the terminal.  










