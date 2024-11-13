from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Comment this line if you want to see the browser

# Specify the path to the ChromeDriver
driver_path = r"C:\Users\jvchi\Documents\GoogleMapsScraper\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)

# Create a WebDriver instance
driver = webdriver.Chrome(service=service, options=options)

try:
    # Open Google
    driver.get("https://www.google.com")

    # Wait for the page to load
    time.sleep(2)

    # Find the search box using its name attribute value
    search_box = driver.find_element("name", "q")

    # Type a search query
    search_box.send_keys("Hello, world!")

    # Submit the search form
    search_box.submit()

    # Wait for the results to load
    time.sleep(2)

    # Print the title of the current page
    print(driver.title)

finally:
    # Close the browser
    driver.quit()
