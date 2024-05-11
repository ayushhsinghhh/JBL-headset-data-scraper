import csv
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.2420.81",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0"
]

chosen_user_agent = random.choice(user_agents)
s = Service("E:\\chromedriver\\chromedriver.exe")


def get_driver():
    options = webdriver.ChromeOptions()
    chosen_user_agent = random.choice(user_agents)
    options.add_argument(f"user-agent={chosen_user_agent}")
    return webdriver.Chrome(service=s, options=options)


driver = get_driver()
urls = ["https://in.jbl.com", "https://uk.jbl.com"]
for base_url in urls:
    driver.get(base_url)
    time.sleep(10)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    headphone_type = ""
    headphones_dropdown = soup.find_all('li', {'data-cgid': 'headphones'})

    for link in headphones_dropdown:
        category = link.find('span', class_="category-decoration").text
        a_tag_class = category.replace(" ", "-")
        category_link = base_url + link.find('a', class_=a_tag_class)
        driver = get_driver()
        driver.get(category_link)
        category_html = driver.page_source
        category_soup = BeautifulSoup(category_html, "html.parser")
        headphones = category_soup.find_all('div', class_='product-tile')
        product_link = "https://in.jbl.com/" + headphones[0].find('a', class_='link')[
            'href']

        driver = get_driver()
        driver.get(product_link)
        time.sleep(10)
        product_page_content = driver.page_source
        product_soup = BeautifulSoup(product_page_content, 'html.parser')

        # Extract specification headers
        spec_divs = product_soup.find_all('div', class_='spec-body')
        column_names = ['Name', 'Price']
        for spec_div in spec_divs:
            dt_tags = spec_div.find_all('dt')
            column_names += [dt.text.strip() for dt in dt_tags]

        product_data = []

        for headphone in headphones:
            name = headphone.find('a', class_='link').text.strip()
            anchor_tag = headphone.find('a', class_='link')
            price = headphone.find('span', class_='value').text.strip()
            product_link = "https://in.jbl.com/" + anchor_tag['href']  # url of each product

            # Load Product page to extract specs
            driver = get_driver()
            driver.get(product_link)
            wait_time = random.uniform(8, 18)
            time.sleep(wait_time)
            product_page_content = driver.page_source
            product_soup = BeautifulSoup(product_page_content, 'html.parser')

            # Extracting specs
            spec_divs = product_soup.find_all('div', class_='spec-body')
            specs = {}
            for spec_div in spec_divs:
                dd_tags = spec_div.find_all('dd')
                dt_tags = spec_div.find_all('dt')
                specs.update({dt.text.strip(): dd.text.strip() for dt, dd in zip(dt_tags, dd_tags)})
            product_data.append({
                'Name': name,
                'Price': price,
                **specs
            })
        driver.quit()

        # Writing data to a CSV file
        if "in" in base_url:
            country = "In"
        else:
            country = "UK"
        csv_filename = f'{country}_{category}_data.csv'
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=column_names)
            writer.writeheader()
            for product in product_data:
                writer.writerow(product)
        print("Data has been successfully saved to", csv_filename)
