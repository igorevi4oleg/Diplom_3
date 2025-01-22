import pytest
import allure
from tests.conftest import driver
from page_objects.account_page import AccountPage
from page_objects.main_page import MainPage
from urls import Urls


@pytest.mark.usefixtures("driver")
class TestPersonalAccount:
    @allure.title("Переход по клику на 'личный кабинет'")
    def test_navigate_to_personal_account(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        account_page = AccountPage(driver)
        account_page.wait_visibility_of_button_register()
        assert account_page.check_displaying_of_button_register(), "Не удалось перейти в личный кабинет"

    @allure.title("Переход по клику на 'историю заказов'")
    def test_click_on_order_history(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page = AccountPage(driver)
        account_page.login_user(user_data['email'], user_data['password'])
        main_page.get_current_url_with_wait()
        main_page.check_clickable_on_button_make_order()
        main_page.click_on_personal_account_in_header()
        account_page.wait_visibility_of_description()
        account_page.click_on_order_history_button()
        assert  main_page.get_current_url() == Urls.order_history, "Не удалось перейти в историю заказов"

    @allure.title("Выход из аккаунта")
    def test_exit_from_account(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page = AccountPage(driver)
        account_page.login_user(user_data['email'], user_data['password'])
        main_page.get_current_url_with_wait()
        main_page.check_clickable_on_button_make_order()
        main_page.click_on_personal_account_in_header()
        account_page.wait_visibility_of_description()
        account_page.click_on_logout_button()
        assert main_page.get_current_url_with_wait() == Urls.login_page, "Не удалось выйти"
