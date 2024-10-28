import pytest
from playwright.sync_api import sync_playwright
import allure


@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@allure.feature("Поиск салонов МТС")
@allure.story("Проверка отображения информации о салоне")
def test_mts_salon_search(browser):
    page = browser.new_page()

    with allure.step("Открыть веб-браузер и перейти на сайт mts.ru"):
        page.goto("https://www.mts.ru/")

    with allure.step("Нажать на кнопку 'Тарифы'"):
        page.click("text=Тарифы")

    with allure.step("Нажать на кнопку 'Дополнительные услуги'"):
        page.click("text=Дополнительные услуги")

    with allure.step("Нажать на кнопку 'Подключить'"):
        page.click("text=Подключить")

    with allure.step("Нажать на кнопку 'В салонах экосистемы МТС'"):
        page.click("text=В салонах экосистемы МТС")

    with allure.step("Ввести адрес салона МТС"):
        search_input = page.locator("input[placeholder='Поиск']")
        search_input.fill("Рязань, ул. Циолковского, д.2/6")
        search_input.press("Enter")

    with allure.step("Выбрать адрес из результатов поиска"):
        page.click("text=Рязань, ул. Циолковского, д.2/6")

    with allure.step("Проверить, что информация о салоне появилась на карте"):
        page.wait_for_selector(".offices-map__balloon", timeout=1000)
        assert page.is_visible(".offices-map__balloon")
        assert page.is_visible("text=Рязань, ул. Циолковского, д.2/6")

    page.close()
