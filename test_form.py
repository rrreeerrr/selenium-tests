import pytest
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
                #Selenium Manager will auto-download the appropriate driver
    options = webdriver.EdgeOptions()
    options.add_argument("--headless")  # run without UI
    options.add_argument("--no-sandbox")  # required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # overcome limited /dev/shm size on Linux
 
    driver = webdriver.Edge(options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


def test_successful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    username_input = driver.find_element(By.NAME, "username")
    username_input.clear()
    username_input.send_keys("tomsmith")

    password_input = driver.find_element(By.NAME, "password")
    password_input.clear()
    password_input.send_keys("SuperSecretPassword!")

    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    successful_message = driver.find_element(By.CSS_SELECTOR, ".flash.success").text
    assert "You logged into a secure area!" in successful_message


def test_unsuccessful_login(driver):
    driver.get("https://the-internet.herokuapp.com/login")

    wrong_username_input = driver.find_element(By.NAME, "username")
    wrong_username_input.clear()
    wrong_username_input.send_keys("sam")
    
    wrong_password_input = driver.find_element(By.NAME, "password")
    wrong_password_input.clear()
    wrong_password_input.send_keys("notthatpassword")
    
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    unsuccessful_message = driver.find_element(By.CSS_SELECTOR, ".flash.error").text
    assert "Your username is invalid!" in unsuccessful_message