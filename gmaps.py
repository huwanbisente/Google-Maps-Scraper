from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

class WebDriver:
    location_data = {}

    def __init__(self):
        self.PATH = r"C:\Users\jvchi\Documents\GoogleMapsScraper\chromedriver-win64\chromedriver.exe"  # Full path to the driver
        self.options = Options()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(self.PATH, options=self.options)

        self.location_data["rating"] = "NA"
        self.location_data["reviews_count"] = "NA"
        self.location_data["location"] = "NA"
        self.location_data["contact"] = "NA"
        self.location_data["website"] = "NA"
        self.location_data["Time"] = {
            "Monday": "NA", "Tuesday": "NA", "Wednesday": "NA", 
            "Thursday": "NA", "Friday": "NA", "Saturday": "NA", 
            "Sunday": "NA"
        }
        self.location_data["Reviews"] = []
        self.location_data["Popular Times"] = {
            "Monday": [], "Tuesday": [], "Wednesday": [], 
            "Thursday": [], "Friday": [], "Saturday": [], 
            "Sunday": []
        }

    def click_open_close_time(self):
        try:
            element = self.driver.find_element(By.CLASS_NAME, "cX2WmPgCkHi__section-info-hour-text")
            ActionChains(self.driver).move_to_element(element).click(element).perform()
        except Exception:
            pass

    def click_all_reviews_button(self):
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "allxGeDnJMl__button"))
            )
            element.click()
            return True
        except Exception:
            return False

    def get_location_data(self):
        try:
            avg_rating = self.driver.find_element(By.CLASS_NAME, "section-star-display")
            total_reviews = self.driver.find_element(By.CLASS_NAME, "section-rating-term")
            address = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id='address']")
            phone_number = self.driver.find_element(By.CSS_SELECTOR, "[data-tooltip='Copy phone number']")
            website = self.driver.find_element(By.CSS_SELECTOR, "[data-item-id='authority']")

            self.location_data["rating"] = avg_rating.text
            self.location_data["reviews_count"] = total_reviews.text[1:-1]
            self.location_data["location"] = address.text
            self.location_data["contact"] = phone_number.text
            self.location_data["website"] = website.text
        except Exception:
            pass

    def get_location_open_close_time(self):
        try:
            days = self.driver.find_elements(By.CLASS_NAME, "lo7U087hsMA__row-header")
            times = self.driver.find_elements(By.CLASS_NAME, "lo7U087hsMA__row-interval")

            day = [a.text for a in days]
            open_close_time = [a.text for a in times]

            for i, j in zip(day, open_close_time):
                self.location_data["Time"][i] = j
        except Exception:
            pass

    def get_popular_times(self):
        try:
            popular_times = self.driver.find_elements(By.CLASS_NAME, "section-popular-times-graph")
            dic = {0: "Sunday", 1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday"}
            l = {day: [] for day in dic.values()}

            for count, graph in enumerate(popular_times):
                bars = graph.find_elements(By.CLASS_NAME, "section-popular-times-bar")
                for bar in bars:
                    x = bar.get_attribute("aria-label")
                    l[dic[count]].append(x)

            self.location_data["Popular Times"] = l
        except Exception:
            pass

    def scroll_the_page(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root")))
            pause_time = 2
            max_count = 5

            for _ in range(max_count):
                scrollable_div = self.driver.find_element(By.CSS_SELECTOR, 'div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                time.sleep(pause_time)
        except Exception:
            pass

    def expand_all_reviews(self):
        try:
            elements = self.driver.find_elements(By.CLASS_NAME, "section-expand-review")
            for element in elements:
                element.click()
        except Exception:
            pass

    def get_reviews_data(self):
        try:
            review_names = self.driver.find_elements(By.CLASS_NAME, "section-review-title")
            review_texts = self.driver.find_elements(By.CLASS_NAME, "section-review-review-content")
            review_dates = self.driver.find_elements(By.CSS_SELECTOR, "[class='section-review-publish-date']")
            review_stars = self.driver.find_elements(By.CSS_SELECTOR, "[class='section-review-stars']")

            review_stars_final = [i.get_attribute("aria-label") for i in review_stars]
            review_names_list = [a.text for a in review_names]
            review_texts_list = [a.text for a in review_texts]
            review_dates_list = [a.text for a in review_dates]

            for name, text, date, rating in zip(review_names_list, review_texts_list, review_dates_list, review_stars_final):
                self.location_data["Reviews"].append({"name": name, "review": text, "date": date, "rating": rating})
        except Exception:
            pass

    def scrape(self, url):
        try:
            self.driver.get(url)
            time.sleep(10)

            self.click_open_close_time()
            self.get_location_data()
            self.get_location_open_close_time()
            self.get_popular_times()
            if not self.click_all_reviews_button():
                return self.location_data  # Stop if unable to click reviews button

            time.sleep(5)
            self.scroll_the_page()
            self.expand_all_reviews()
            self.get_reviews_data()
        finally:
            self.driver.quit()

        return self.location_data

# Replace with your actual location URL
url = "your_location_url"
x = WebDriver()
print(x.scrape(url))
