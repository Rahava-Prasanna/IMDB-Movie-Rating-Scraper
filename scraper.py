from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

URL = "https://www.imdb.com/chart/top/"
CSV_FILE = r"C:\IMDB Movie Rating Scraper\imdb_top250.csv"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--ignore-certificate-errors")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

driver.get(URL)

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "ul.ipc-metadata-list"))
)

time.sleep(3)

for _ in range(8):
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(0.8)

time.sleep(2)

cards = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

movies = []
rank = 1

for card in cards:
    try:
        title = card.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text.strip()
    except:
        title = ""

    try:
        year = card.find_element(By.CSS_SELECTOR, "div.cli-title-metadata span").text.strip()
    except:
        year = ""

    try:
        rating = card.find_element(By.CSS_SELECTOR, "span.ipc-rating-star--rating").text.strip()
    except:
        rating = ""

    if title:
        movies.append({
            "Rank": rank,
            "Title": title,
            "Year": year,
            "Rating": rating
        })
        rank += 1

df = pd.DataFrame(movies)
df.to_csv(CSV_FILE, index=False)

print("Movies scraped:", len(df))
print("CSV saved at:", CSV_FILE)

driver.quit()