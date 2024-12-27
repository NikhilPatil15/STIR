# import requests
# from selenium import webdriver
# import urllib.parse
# from selenium.webdriver.common.by import By
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.keys import Keys
# from datetime import datetime
# from database import save_trending_data
# import uuid
# import os
# import time
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()


# def setup_driver():
#     """Setup and return Firefox driver with appropriate options"""
#     # Firefox WebDriver setup
#     firefox_options = Options()
#     firefox_profile = webdriver.FirefoxProfile()
#     firefox_profile.set_preference("dom.webdriver.enabled", False)
#     firefox_profile.set_preference("useAutomationExtension", False)

#     # Get proxy from environment
#     PROXY = os.getenv("PROXYMESH_URL")

#     if PROXY:

#         # print(PROXY)
#         # Set the proxy argument
#         firefox_options.add_argument(f"--proxy-server={PROXY}")

#     firefox_options.binary_location = (
#         "C:/Program Files/Firefox Developer Edition/firefox.exe"
#     )
#     service = Service(executable_path="E:/WebDriver/geckodriver.exe")

#     return webdriver.Firefox(service=service, options=firefox_options)


# def handle_login(driver, username, password):
#     """Handle the login process with error handling"""
#     try:
#         # URL encode the username and password
#         x_username = urllib.parse.quote_plus(username)

#         # Wait for page load
#         time.sleep(5)

#         # Find and fill username using JavaScript
#         inputs = driver.find_elements(By.TAG_NAME, "input")
#         for input_field in inputs:
#             if input_field.is_displayed():
#                 input_field.send_keys(x_username)
#                 break

#         # Click Next
#         next_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
#         )
#         next_button.click()
#         time.sleep(2)

#         # Handle password
#         password_input = WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
#         )
#         print(password)
#         password_input.send_keys(password)

#         # Click Login
#         login_button = driver.find_element(By.XPATH, "//span[text()='Log in']")
#         login_button.click()
#         time.sleep(5)

#         return True
#     except Exception as e:
#         print(f"Login error: {str(e)}")
#         driver.save_screenshot("login_error.png")
#         return False


# # def get_trending_topics(driver):
# #     """Extract trending topics from Twitter homepage's 'What's happening' section."""
# #     try:
# #         # Make sure we're on the homepage and give it time to load
# #         time.sleep(3)

# #         WebDriverWait(driver, 60).until(
# #             EC.presence_of_element_located((By.TAG_NAME,'section'))
# #         )
# #         text = "What's happening"
# #         # Extract all span elements inside the section
# #         headings = driver.find_elements(By.TAG_NAME,"section")

# #         print(type(headings))

# #         print("headings: ",headings,"length: ", len(headings))

# #         # # Segregate based on criteria (example: trends vs descriptions)
# #         # trending_topics = [text for text in headings if text.startswith("#")]  # Hashtags
# #         # other_content = [text for text in headings if not text.startswith("#")]  # Non-hashtag content

# #         # print("Trending Topics:", trending_topics)
# #         # print("Other Content:", other_content)
# #         # Filter out spans that look like headings (non-empty and bold/prominent text)
# #         trends = [heading.text.strip() for heading in headings if heading.text.strip()]

# #         if trends:
# #             print("Trending topics:",type(trends),"Length: ", len(trends),"")

# #             print("Trending: ", trends[1])
# #             # for trend in trends:
# #             #     print(f"- {trend}")
# #             return trends
# #         else:
# #             print("No trending topics found.")
# #             return []


# #     except Exception as e:
# #         print(f"Error getting trends: {str(e)}")
# #         print("Current URL:", driver.current_url)
# #         driver.save_screenshot("trends_error.png")
# #         return []
# # def get_trending_topics(driver):
# #     """Extract trending topics from Twitter homepage's 'What's happening' section."""
# #     try:
# #         # Make sure we're on the homepage and give it time to load
# #         time.sleep(3)

# #         WebDriverWait(driver, 60).until(
# #             EC.presence_of_element_located((By.TAG_NAME, "section"))
# #         )

# #         # Extract all sections
# #         headings = driver.find_elements(By.TAG_NAME, "section")

# #         if len(headings) < 2:
# #             print("Required sections not found")
# #             return []

# #         # Get text from What's happening section (second element)
# #         whats_happening_text = headings[1].text

# #         # Split into lines and process
# #         lines = whats_happening_text.split("\n")
# #         trending_topics = []

# #         # Debug print
# #         print("Processing 'What's happening' section content:")
# #         print(whats_happening_text)

# #         skip_next = False
# #         for line in lines:
# #             # Skip the header and empty lines
# #             if line == "What's happening" or not line.strip():
# #                 continue

# #             # Skip lines that indicate metadata
# #             if (
# #                 line.replace("K", "").replace("M", "").isdigit()
# #                 or line == "Trending"
# #                 or line.endswith("Tweets")
# #                 or line.startswith("·")
# #                 or "· Trending" in line
# #             ):
# #                 skip_next = False
# #                 continue

# #             # If not a metadata line and not marked for skipping, it's a trend heading
# #             if not skip_next:
# #                 trending_topics.append(line.strip())
# #                 skip_next = True  # Skip the next line as it's usually the description

# #         print("\nExtracted Trending Topics:")
# #         for i, topic in enumerate(trending_topics, 1):
# #             print(f"{i}. {topic}")

# #         return trending_topics

# #     except Exception as e:
# #         print(f"Error getting trends: {str(e)}")
# #         print("Current URL:", driver.current_url)
# #         driver.save_screenshot("trends_error.png")
# #         return []

# def get_trending_topics(driver):
#     """Extract trending topics from Twitter homepage's 'What's happening' section."""
#     try:
#         time.sleep(3)
        
#         WebDriverWait(driver, 60).until(
#             EC.presence_of_element_located((By.TAG_NAME,'section'))
#         )
        
#         headings = driver.find_elements(By.TAG_NAME,"section")
        
#         if len(headings) < 2:
#             print("Required sections not found")
#             return []
            
#         # Get text from What's happening section
#         whats_happening_text = headings[1].text
#         lines = whats_happening_text.split('\n')
        
#         trending_topics = []
        
#         # Process lines to extract headings
#         for i in range(len(lines)-1):
#             current_line = lines[i].strip()
#             next_line = lines[i+1].strip() if i+1 < len(lines) else ""
            
#             # Skip specific lines we don't want
#             if any(skip in current_line for skip in [
#                 "Trending now",
#                 "What's happening",
#                 "Show more",
#                 "Trending in",
#                 "· Trending"
#             ]):
#                 continue
                
#             # If current line isn't a post count and next line is, it's a heading
#             if (not current_line.endswith('posts') and 
#                 next_line.endswith('posts') and 
#                 current_line):
#                 trending_topics.append(current_line)
        
#         # print("\nExtracted Trending Topics:")
#         # for i, topic in enumerate(trending_topics, 1):
#         #     print(f"{i}. {topic}")
            
#         return trending_topics

#     except Exception as e:
#         print(f"Error getting trends: {str(e)}")
#         print("Current URL:", driver.current_url)
#         driver.save_screenshot("trends_error.png")
#         return []

# def get_current_ip(driver):
#     """Get the current IP address being used by sending a request to an IP detection service"""
#     try:
#         # Navigate to an IP checking service
#         driver.get('https://api.ipify.org')
#         time.sleep(2)  # Wait for page to load
#         # Get the IP address from the page (ipify returns only the IP address)
#         current_ip = driver.find_element(By.TAG_NAME, "body").text.strip()
#         return current_ip
#     except Exception as e:
#         print(f"Error getting IP address: {str(e)}")
#         # Fallback method using requests
#         try:
#             response = requests.get('https://api.ipify.org')
#             return response.text.strip()
#         except:
#             return None
        
# def scrape_twitter():
#     """Main function to scrape Twitter trends"""
#     # Get environment variables
#     x_username = os.getenv("TWITTER_USERNAME")
#     x_password = os.getenv("TWITTER_PASSWORD")
#     proxy = os.getenv("PROXYMESH_URL")

#     if not all([x_username, x_password, proxy]):
#         print("Missing environment variables. Please check your .env file.")
#         return

#     driver = None
#     try:
#         # Setup and start driver
#         driver = setup_driver()
        
#         current_ip = get_current_ip(driver)
        
#         if not current_ip:
#             print("Warning: Could not determine IP address")
#             current_ip = "unknown"
#         # else:
#         #     print(f"Current IP address: {current_ip}")
        
#         driver.get("https://twitter.com/i/flow/login")

#         # Handle login
#         if not handle_login(driver, x_username, x_password):
#             print("Login failed")
#             return

#         # Get trending topics
#         trends = get_trending_topics(driver)

#         if trends and len(trends) == 4:
#             # Prepare record for MongoDB
#             record = {
#                 "_id": str(uuid.uuid4()),
#                 "trend1": trends[0],
#                 "trend2": trends[1],
#                 "trend3": trends[2],
#                 "trend4": trends[3],
#                 "timestamp": datetime.now(),
#                 "ip_address": current_ip,  # Extract proxy IP
#             }
#             # print(record)
#             # Save to database
#             save_trending_data(record)
#             # print("Successfully saved trends:", record)
#             return trends
#         else:
#             print("Not enough trending topics found")

#     except Exception as e:
#         print(f"Main error occurred: {str(e)}")
#         if driver:
#             driver.save_screenshot("main_error.png")
#     finally:
#         if driver:
#             driver.quit()


# if __name__ == "__main__":
#     scrape_twitter()
    
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

# Load environment variables
load_dotenv()


def setup_driver():
    """Setup and return Firefox driver with appropriate options"""
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
    """Handle the login process with error handling"""
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
    """Extract trending topics from Twitter homepage"""
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
        
        # Handle login
        if not handle_login(driver, x_username, x_password):
            return {"error": "Login failed"}

        # Get trending topics
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


# This condition ensures the script runs only when executed directly (not imported)
if __name__ == "__main__":
    result = scrape_twitter()
    
    
    print(json.dumps(result))  # Print the result to stdout (can be captured in Flask)
