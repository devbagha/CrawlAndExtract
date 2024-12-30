from selenium import webdriver

def initialize_driver():
    """Initialize and return a Chrome WebDriver instance."""
    return webdriver.Chrome()
