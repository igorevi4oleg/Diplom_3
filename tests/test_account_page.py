import pytest
import allure
from tests.conftest import driver
from page_objects.account_page import AccountPage
from page_objects.main_page import MainPage
from page_objects.base_page import BasePage
from locators.for_reset_password import ResetPasswordLocators
from locators.for_main_page import MainPageLocators
from urls import Urls


@pytest.mark.usefixtures("driver")
class TestPersonalAccount:
    @allure.description("Переход по клику на 'личный кабинет'")
    def test_navigate_to_personal_account(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        account_page = AccountPage(driver)
        account_page.wait_visibility_of_button_register()
        assert account_page.check_displaying_of_button_register(), "Не удалось перейти в личный кабинет"

    @allure.description("Переход по клику на 'историю заказов'")
    def test_click_on_order_history(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page = AccountPage(driver)
        account_page.send_keys_to_input(ResetPasswordLocators.input_email, user_data['email'])
        account_page.send_keys_to_input(ResetPasswordLocators.input_password, user_data['password'])
        account_page.click_on_element(MainPageLocators.enter_button)
        main_page.click_on_personal_account_in_header()
        account_page.wait_visibility_of_description()
        account_page.click_on_order_history_button()
        account_page.wait_visibility_of_description()
        base_page = BasePage(driver)
        assert  base_page.get_current_url() == f"{Urls.order_history}", "Не удалось перейти в историю заказов"

    @allure.description("Выход из аккаунта")
    def test_exit_from_account(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page = AccountPage(driver)
        account_page.send_keys_to_input(ResetPasswordLocators.input_email, user_data['email'])
        account_page.send_keys_to_input(ResetPasswordLocators.input_password, user_data['password'])
        account_page.click_on_element(MainPageLocators.enter_button)
        main_page.click_on_personal_account_in_header()
        account_page.click_on_logout_button()
        base_page = BasePage(driver)
        assert base_page.get_current_url() == f"{Urls.login_page}", "Не удалось выйти"
