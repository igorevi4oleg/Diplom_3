from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage
from locators.for_feed_page import FeedPageLocators
import allure


class FeedPage(BasePage):
    @allure.step('Кликнуть по первому (последнему) заказу в ленте')
    def click_on_order_card(self):
        self.wait_visibility_of_element(FeedPageLocators.order_in_feed)
        self.click_on_element(FeedPageLocators.order_in_feed)

    @allure.step('Получить текст заголовка окна с деталями заказа')
    def get_text_on_title_of_modal_order(self):
        return self.get_text_on_element(FeedPageLocators.title_of_modal_order)

    @allure.step('Получить количество заказов, выполненных за все время')
    def get_quantity_of_orders(self):
        self.find_element_with_wait(FeedPageLocators.quantity_of_orders)
        return self.get_text_on_element(FeedPageLocators.quantity_of_orders)

    @allure.step('Получить количество заказов, выполненных за сегодня')
    def get_daily_quantity_of_orders(self):
        self.find_element_with_wait(FeedPageLocators.daily_quantity_of_orders)
        return self.get_text_on_element(FeedPageLocators.daily_quantity_of_orders)

    @allure.step("Дождаться появления заказа в работе")
    def wait_for_visibility_order_number_in_work(self, order_id, timeout=10):
        order_locator = (By.XPATH, f'//p[@class="text text_type_digits-default" and text()="#0{order_id}"]')
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(order_locator)
        )

    @allure.step("Проверить, что заказ отображается в работе")
    def check_for_visibility_order_number_in_work(self, order_id):
        order_locator = (By.XPATH, f'//p[@class="text text_type_digits-default" and text()="#0{order_id}"]')
        return self.check_displaying_of_element(order_locator)

    @allure.step("Дождаться появления заказа в ленте")
    def wait_for_visibility_order_number(self, order_id, timeout=10):
        order_locator = (By.XPATH, f'//p[@class="text text_type_digits-default" and text()="#{order_id}"]')
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(order_locator)
        )

    @allure.step("Проверить, что заказ отображается в ленте")
    def check_for_visibility_order_number(self, order_id):
        order_locator = (By.XPATH, f'//p[@class="text text_type_digits-default" and text()="#{order_id}"]')
        return self.check_displaying_of_element(order_locator)

