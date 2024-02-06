from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os

def get_high_res_url(thumbnail_url):
    return thumbnail_url.replace("80x80.jpg_", "")

def download_images(urls, save_dir, image_name_prefixes):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for url, image_name_prefix in zip(urls, image_name_prefixes):
            driver.get(url)

            thumbnails = driver.find_elements(By.CSS_SELECTOR, 'div.slider--img--D7MJNPZ img')
            image_urls = set()

            for thumbnail in thumbnails:
                thumbnail_url = thumbnail.get_attribute('src')
                if thumbnail_url:
                    high_res_url = get_high_res_url(thumbnail_url)
                    image_urls.add(high_res_url)

            for i, img_url in enumerate(image_urls):
                response = requests.get(img_url)
                if response.status_code == 200:
                    image_path = os.path.join(save_dir, f'{image_name_prefix}_{i}.jpg')
                    with open(image_path, 'wb') as f:
                        f.write(response.content)
                    print(f'Downloaded image to {image_path}')
                else:
                    print(f'Failed to download image {i+1}')

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

urls = []
image_name_prefixes = []

while True:
    user_url = input("Enter the URL of the product page (or press Enter to finish): ")
    if not user_url:
        break

    user_image_name = input("Enter the image name prefix: ")
    if not user_image_name:
        break

    urls.append(user_url)
    image_name_prefixes.append(user_image_name)

if urls:
    user_save_dir = 'ADD/YOUR/PATH'
    download_images(urls, user_save_dir, image_name_prefixes)
    print("Operation completed. Images downloaded.")
else:
    print("No URLs provided. Exiting.")
