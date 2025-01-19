import time
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
        time.sleep(6)
        self.find_element_with_wait(FeedPageLocators.quantity_of_orders)
        return self.get_text_on_element(FeedPageLocators.quantity_of_orders)

    @allure.step('Получить количество заказов, выполненных за сегодня')
    def get_daily_quantity_of_orders(self):
        self.find_element_with_wait(FeedPageLocators.daily_quantity_of_orders)
        return self.get_text_on_element(FeedPageLocators.daily_quantity_of_orders)

    @allure.step('Получить номер последнего заказа в разделе "В работе"')
    def get_order_number_in_feed_progress_section(self):
        return self.get_text_on_element(FeedPageLocators.number_of_order_in_progress)

    @allure.step('Поиск номера созданного заказа в ленте')
    def find_order_number(self, order_number):
        order_elements = self.driver.find_elements(By.CSS_SELECTOR, 'p.text.text_type_digits-default')
        for element in order_elements:
            if order_number in element.text:
                return element
        return None