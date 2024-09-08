import allure
import pytest
import allure_commons
from appium.options.android import UiAutomator2Options
from selene import browser, support
import os
from dotenv import load_dotenv
from utils import attach

@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    login = os.getenv('LOGIN')
    access_key = os.getenv('PASSWORD')
    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        # "platformName": "android"
        'platformVersion': '9.0',
        'deviceName': 'Google Pixel 3',
        # Set URL of the application under test
        'app': os.getenv('APP_URL'),

        # Set other BrowserStack capabilities
        'bstack:options': {
            'projectName': 'First Python project',
            'buildName': 'browserstack-build-1',
            'sessionName': 'BStack first_test',
        # Set your access credentials
            'userName': login,
            'accessKey': access_key
        }
    })

    with allure.step('Инициализировать сеанс приложения'):
        browser.config.driver_remote_url = 'http://hub.browserstack.com/wd/hub'
        browser.config.driver_options = options

        browser.config.timeout = float(os.getenv('timeout', '10.0'))
        browser.config._wait_decorator = support._logging.wait_with(context=allure_commons._allure.StepContext)

    yield

    attach.add_screenshot(browser)
    attach.add_xml(browser)

    session_id = browser.driver.session_id

    attach.add_video(session_id, login, access_key)

    with allure.step('Закрыть сессию приложения'):
        browser.quit()