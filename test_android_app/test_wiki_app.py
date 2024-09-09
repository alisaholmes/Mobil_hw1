import allure
from allure_commons.types import Severity
from appium.webdriver.common.appiumby import AppiumBy
from selene import browser, have


@allure.tag('Mobile')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Alisa Holmes')
@allure.feature('Найти статью о «Appium»')
@allure.story('Поиск статьи')
def test_search():
    with allure.step('Ввести в поиск значение "Appium"'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID,'org.wikipedia.alpha:id/search_src_text')).type('Appium')
    with allure.step('Проверить найденное значение'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('Appium'))


@allure.tag('Mobile')
@allure.severity(Severity.NORMAL)
@allure.label('owner', 'Alisa Holmes')
@allure.feature('Найти статью о "HTML"')
@allure.story('Поиск статьи')
def test_search_html():
    with allure.step('Ввести в поиск значение "HTML"'):
        browser.element((AppiumBy.ACCESSIBILITY_ID, 'Search Wikipedia')).click()
        browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text")).type('HTML')
    with allure.step('Проверить найденное значение'):
        results = browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title'))
        results.should(have.size_greater_than(0))
        results.first.should(have.text('HTML'))
    with allure.step('Клик на первый результат'):
        browser.all((AppiumBy.ID, 'org.wikipedia.alpha:id/page_list_item_title')).first.click()
