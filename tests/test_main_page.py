import pytest
import allure
from page_objects.main_page import MainPage
from page_objects.base_page import BasePage
from page_objects.feed_page import FeedPage
from page_objects.account_page import AccountPage
from locators.for_main_page import MainPageLocators
from locators.for_feed_page import FeedPageLocators
from locators.for_reset_password import ResetPasswordLocators


@pytest.mark.usefixtures("driver")
class TestMainFunctionality:
    @allure.description("Переход по клику на 'Конструктор'")
    def test_click_on_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_button_constructor()
        base_page = BasePage(driver)
        assert base_page.find_element_with_wait(MainPageLocators.selected_button), "Элемент не найден"

    @allure.description("Переход по клику на 'Лента заказов'")
    def test_click_on_feed(self, driver):
        main_page = MainPage(driver)
        main_page.click_header_feed_button()
        feed_page = FeedPage(driver)
        assert feed_page.find_element_with_wait(FeedPageLocators.section_orders_list), "Элемент не найден"


    @allure.description("Получение деталей об ингридиенте")
    def test_get_ingridient_details(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_button_constructor()
        main_page.click_on_ingredient()
        assert main_page.check_displaying_of_modal_details(), "окно отображается"


    @allure.description("Получение деталей об ингридиенте и закрытие окна")
    def test_get_ingridient_details_and_close_window(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_button_constructor()
        main_page.click_on_ingredient()
        main_page.check_displaying_of_modal_details()
        main_page.close_modal()
        assert main_page.check_not_displaying_of_modal_details(), "окно не отображается"


    @allure.description("Увеличение каунтера ингридиента")
    def test_increase_counter(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_button_constructor()
        before_drop = main_page.get_count_of_ingredients()
        main_page.add_ingredient_to_order_with_js()
        after_drop = main_page.get_count_of_ingredients()
        assert after_drop > before_drop


    @allure.description("Залогиненный юзер может оформить заказ")
    def test_click_on_order_history(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page = AccountPage(driver)
        account_page.send_keys_to_input(ResetPasswordLocators.input_email, user_data['email'])
        account_page.send_keys_to_input(ResetPasswordLocators.input_password, user_data['password'])
        account_page.click_on_element(MainPageLocators.enter_button)
        main_page.add_ingredient_to_order_with_js()
        main_page.click_on_button_make_order()
        main_page.check_displaying_of_confirmation_modal_of_order()
        main_page.get_number_of_order_in_modal_confirmation()
        main_page.click_on_button_close_confirmation_modal()
        base_page = BasePage(driver)
        assert base_page.get_current_url() == "https://stellarburgers.nomoreparties.site/"


