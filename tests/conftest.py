import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from helpers import *
import requests
from urls import Urls
import allure


@pytest.fixture(params=[webdriver.Firefox, webdriver.Chrome], ids=['firefox', 'chrome'], scope="function")
def driver(request):
    driver_class = request.param
    if driver_class == webdriver.Chrome:
        options = Options()
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--incognito')
        driver = webdriver.Chrome(options=options)
    elif driver_class == webdriver.Firefox:
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--width=1920')
        firefox_options.add_argument('--height=1080')
        profile = FirefoxProfile()
        profile.set_preference("browser.privatebrowsing.autostart", True)
        firefox_options.profile = profile
        driver = webdriver.Firefox(options=firefox_options)
    driver.get(Urls.base_url)
    yield driver
    driver.quit()

@pytest.fixture
@allure.title('Фикстура создает пользователя с рандомными кредами и удаляет его из базы после теста')
def create_new_user_and_delete():
    payload_cred = {
        'email': create_random_email(),
        'password': create_random_password(),
        'name': create_random_name()
    }
    response = requests.post(Urls.user_register, data=payload_cred)
    response_body = response.json()

    yield payload_cred, response_body

    access_token = response_body['accessToken']
    requests.delete(Urls.user_delete, headers={'Authorization': access_token})
