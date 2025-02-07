from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Function to initialize WebDriver (useful for scraping orders)
def initialize_driver():
    """Initializes the WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless to avoid opening the browser window
    driver = webdriver.Chrome(options=options)
    return driver

def login(driver):
    """Logs in to the Edusson platform"""
    driver.get("https://edusson.com/writer/orders/available")
    
    # Enter login details
    username = driver.find_element(By.NAME, "email")  
    password = driver.find_element(By.NAME, "password")
    
    username.send_keys("your_email_here")  # Replace with actual email
    password.send_keys("your_password_here")  # Replace with actual password
    driver.find_element(By.CLASS_NAME, "btn-login").click()

    time.sleep(5)  # Wait for the page to load

def fetch_orders():
    """Scrapes available orders from Edusson"""
    driver = initialize_driver()  # Start WebDriver
    login(driver)  # Login to the platform

    orders = driver.find_elements(By.CLASS_NAME, "order-card")  # Adjust based on HTML structure
    available_orders = []

    for order in orders:
        order_id = order.find_element(By.CLASS_NAME, "order-id").text
        subject = order.find_element(By.CLASS_NAME, "order-subject").text
        deadline = order.find_element(By.CLASS_NAME, "order-deadline").text
        bids = order.find_element(By.CLASS_NAME, "order-bids").text
        
        available_orders.append({
            "Order ID": order_id, 
            "Subject": subject, 
            "Deadline": deadline, 
            "Bids": int(bids)
        })

    driver.quit()  # Quit the browser session
    return available_orders
