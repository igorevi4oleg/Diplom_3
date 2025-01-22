from page_objects.base_page import BasePage
from locators.for_account import AccountLocators
from locators.for_reset_password import ResetPasswordLocators
from locators.for_main_page import MainPageLocators
import allure


class AccountPage(BasePage):
    @allure.step('Кликнуть по кнопке "История заказов"')
    def click_on_order_history_button(self):
        self.wait_visibility_of_element(AccountLocators.order_history)
        self.click_on_element(AccountLocators.order_history)

    @allure.step('Кликнуть по кнопке "Выйти"')
    def click_on_logout_button(self):
        self.wait_visibility_of_element(AccountLocators.button_logout)
        self.click_on_element(AccountLocators.button_logout)

    @allure.step('Подождать прогрузки текста описания раздела')
    def wait_visibility_of_description(self):
        self.wait_visibility_of_element(AccountLocators.description_of_section)

    @allure.step('Подождать прогрузки кнопки "Зарегистрироваться"')
    def wait_visibility_of_button_register(self):
        self.wait_visibility_of_element(AccountLocators.button_register)

    @allure.step('Проверить отображение кнопки "Зарегистрироваться"')
    def check_displaying_of_button_register(self):
        return self.check_displaying_of_element(AccountLocators.button_register)

    @allure.step('Авторизоваться в личном кабинете')
    def login_user(self, email, password):
        self.send_keys_to_input(ResetPasswordLocators.input_email, email)
        self.send_keys_to_input(ResetPasswordLocators.input_password, password)
        self.click_on_element(MainPageLocators.enter_button)