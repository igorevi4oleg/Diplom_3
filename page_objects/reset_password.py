from page_objects.base_page import BasePage
from locators.for_reset_password import ResetPasswordLocators
from helpers import *
import allure


class ResetPassword(BasePage):
    @allure.step('Открыть страницу восстановления пароля')
    def navigate_to_reset_password_page(self):
        self.wait_visibility_of_element(ResetPasswordLocators.button_forgot_password)
        self.check_element_is_clickable(ResetPasswordLocators.button_forgot_password)
        self.click_on_element(ResetPasswordLocators.button_forgot_password)

    @allure.step('Проверить отображение поля email')
    def check_displaying_of_input_email(self):
        return self.check_displaying_of_element(ResetPasswordLocators.input_email)


    @allure.step('Кликнуть на кнопку "Восстановить"')
    def click_on_recovery_button(self):
        self.wait_visibility_of_element(ResetPasswordLocators.button_recover)
        self.check_element_is_clickable(ResetPasswordLocators.button_recover)
        self.click_on_element(ResetPasswordLocators.button_recover)

    @allure.step('Проверить отображение поля password')
    def check_displaying_of_input_password(self):
        self.wait_visibility_of_element(ResetPasswordLocators.input_password)
        return self.check_displaying_of_element(ResetPasswordLocators.input_password)

    @allure.step('Ввести password')
    def send_password(self):
        self.wait_visibility_of_element(ResetPasswordLocators.input_password)
        self.check_element_is_clickable(ResetPasswordLocators.input_password)
        passwd = create_random_password()
        self.send_keys_to_input(ResetPasswordLocators.input_password, passwd)

    @allure.step('Кликнуть на иконку глаза в поле ввода пароля')
    def click_on_eye_icon(self):
        self.wait_visibility_of_element(ResetPasswordLocators.eye_icon)
        self.check_element_is_clickable(ResetPasswordLocators.eye_icon)
        self.click_on_element(ResetPasswordLocators.eye_icon)

    @allure.step('Проверить, что значение поля password отображается')
    def check_displaying_password_value(self):
        return self.check_displaying_of_element(ResetPasswordLocators.value_password_is_visible)
