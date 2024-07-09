import datetime
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
import os
from tqdm import tqdm
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def get_purchase(driver, url):
  
  driver.get(url)

  item_info = {}

  for _ in range(2):
    # Wait for the JavaScript to load the content
    time.sleep(5)  # Adjust the sleep time as necessary

    # Get the page source after JavaScript has loaded the content
    html_content = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    purchase_info = soup.find_all('div', class_='index-mod__order-container___1ur4- js-order-container')
    for info in tqdm(purchase_info):
      table_info = info.find('table')
      success = '成功' in table_info.find_all('span', 'text-mod__link___1rXmw')[-1].text
      if success:
        name = table_info.find_all('tbody')[-1].find_all('span')[2].text
        purchase_date = table_info.find('span', 'bought-wrapper-mod__create-time___yNWVS').text
        all_imgs = table_info.find_all('tbody')[-1].find_all('img')
        
        for i in range(0, len(all_imgs), 6):
          item_info[name + '_' + str(i // 6)] = {'purchase_date': purchase_date, 'img': "https:" + all_imgs[i].get('src')}
        

    # Find and click the "Next" button
    try:
      button = driver.find_element(By.XPATH, '//button[contains(@class, "button-mod__button___2HDif") and contains(@class, "button-mod__default___2pRKd") and contains(@class, "button-mod__small___1a8rc") and text()="下一页"]')
      button.click()
      
      # Wait for the next page to load
      time.sleep(5)  # Adjust the sleep time as necessary
    except Exception as e:
      print("No more pages or an error occurred:", e)
      break

  
  return item_info

def get_purchase_main(url): 
  """
  Find all purchase item of the given url user.
  In the future may take in date concern.
  """ 

  # Set up options for the Chrome driver
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')

  # Set the executable path for the driver
  driver = webdriver.Chrome(options=chrome_options)
  # Navigate to the Taobao login page
  driver.get('https://login.taobao.com/member/login.jhtml')

  # Wait for the page to load
  time.sleep(5)
  pruchase_item = get_purchase(driver, url)

  # get today's time
  now = datetime.datetime.now()
  purchase_csv = 'purchase_' + now.strftime('%Y-%m-%d') + '.csv'
  if os.path.exists(purchase_csv):
    os.remove(purchase_csv)
  with open(purchase_csv, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['商品名', '购买日期', '图片']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for name, info in pruchase_item.items():
      writer.writerow({'商品名': name, '购买日期': info['purchase_date'], '图片': info['img']})


  # Close the browser window
  driver.quit()

if __name__ == "__main__":
  get_purchase_main('123')