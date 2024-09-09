import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from selene import browser, support
import os
from dotenv import load_dotenv
from appium import webdriver
from utils import attach

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    login = os.getenv('LOGIN')
    access_key = os.getenv('PASSWORD')
    options = UiAutomator2Options().load_capabilities({
        'platformVersion': '9.0',
        'deviceName': 'Google Pixel 3',

        'app': os.getenv('APP_URL'),

        'bstack:options': {
            'projectName': 'First Python project',
            'buildName': 'browserstack-build-1',
            'sessionName': 'BStack first_test',

            'userName': login,
            'accessKey': access_key
        }
    })
    with allure.step('Инициализировать сеанс приложения'):
        browser.config.driver = webdriver.Remote('http://hub.browserstack.com/wd/hub', options=options)
        browser.config.driver_options = options

        browser.config.timeout = float(os.getenv('timeout', '15.0'))

        browser.config._wait_decorator = support._logging.wait_with(context=allure_commons._allure.StepContext)

    yield

    attach.add_screenshot(browser)
    attach.add_xml(browser)

    session_id = browser.driver.session_id

    attach.add_video(session_id, login, access_key)

    with allure.step('Закрыть сессию приложения'):
        browser.quit()