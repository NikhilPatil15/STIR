import requests
from selenium import webdriver
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from database import save_trending_data
import uuid
import os
import time
from dotenv import load_dotenv
import json


load_dotenv()


def setup_driver():
    
    firefox_options = Options()
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("dom.webdriver.enabled", False)
    firefox_profile.set_preference("useAutomationExtension", False)

    # Get proxy from environment
    PROXY = os.getenv("PROXYMESH_URL")
    if PROXY:
        firefox_options.add_argument(f"--proxy-server={PROXY}")

    firefox_options.binary_location = "C:/Program Files/Firefox Developer Edition/firefox.exe"
    service = Service(executable_path="E:/WebDriver/geckodriver.exe")
    return webdriver.Firefox(service=service, options=firefox_options)


def handle_login(driver, username, password):
    """ login process with error handling"""
    try:
        x_username = urllib.parse.quote_plus(username)
        time.sleep(5)

        # Find and fill username
        inputs = driver.find_elements(By.TAG_NAME, "input")
        for input_field in inputs:
            if input_field.is_displayed():
                input_field.send_keys(x_username)
                break

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
        )
        next_button.click()
        time.sleep(2)

        # Handle password
        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )
        password_input.send_keys(password)
        login_button = driver.find_element(By.XPATH, "//span[text()='Log in']")
        login_button.click()
        time.sleep(5)
        return True
    except Exception as e:
        print(f"Login error: {str(e)}")
        return False


def get_trending_topics(driver):
    """Extracting trending topics from Twitter homepage"""
    try:
        time.sleep(10)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.TAG_NAME, "section"))
        )
        headings = driver.find_elements(By.TAG_NAME, "section")

        if len(headings) < 2:
            return {"error": "Required sections not found"}

        whats_happening_text = headings[1].text
        lines = whats_happening_text.split("\n")
        trending_topics = []
     
        
        for i in range(len(lines) - 1):
            current_line = lines[i].strip()
            next_line = lines[i + 1].strip() if i + 1 < len(lines) else ""

            if any(skip in current_line for skip in [
                "Trending now"  , "What's happening", "Show more", "Trending in", "· Trending"
            ]):
                continue

            if (not current_line.endswith("posts") and next_line.endswith("posts") and current_line or current_line.startswith("#")):
                trending_topics.append(current_line)

        if trending_topics:
            return {"trends": trending_topics}
        else:
            return {"error": "No trending topics found"}
    except Exception as e:
        print(f"Error getting trends: {str(e)}")
        return {"error": str(e)}


def get_current_ip(driver):
    """Get the current IP address by checking the IP detection service"""
    try:
        driver.get('https://api.ipify.org')
        time.sleep(2)
        current_ip = driver.find_element(By.TAG_NAME, "body").text.strip()
        return current_ip
    except Exception as e:
        return {"error": "Error getting IP address"}


def scrape_twitter():
    """Main function to scrape Twitter trends"""
    x_username = os.getenv("X_USERNAME")
    x_password = os.getenv("X_PASSWORD")
    proxy = os.getenv("PROXYMESH_URL")

    if not all([x_username, x_password, proxy]):
        return {"error": "Missing environment variables. Please check your .env file."}

    driver = None
    try:
        driver = setup_driver()

        current_ip = get_current_ip(driver)
        
        if not current_ip:
            current_ip = "unknown"

        driver.get("https://twitter.com/i/flow/login")
        
       
        if not handle_login(driver, x_username, x_password):
            return {"error": "Login failed"}

        
        trends_response = get_trending_topics(driver)
        if "error" in trends_response:
            return trends_response
        
        trends = trends_response.get("trends", [])
        
        
        if len(trends) == 4:
            record = {
                "_id": str(uuid.uuid4()),
                "trend1": trends[0],
                "trend2": trends[1],
                "trend3": trends[2],
                "trend4": trends[3],
                "timestamp": datetime.now(),
                "ip_address": current_ip,
            }
            response = save_trending_data(record)
            response["timestamp"] = response["timestamp"].isoformat()
            return {"trends": trends,"response":response}
        else:
            return {"error": "Not enough trending topics found"}

    except Exception as e:
        return {"error": f"Main error occurred: {str(e)}"}
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    result = scrape_twitter()
    
    
    print(json.dumps(result))  
