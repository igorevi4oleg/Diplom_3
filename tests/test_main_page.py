import pytest
import allure
from urls import Urls
from page_objects.main_page import MainPage
from page_objects.feed_page import FeedPage
from page_objects.account_page import AccountPage


@pytest.mark.usefixtures("driver")
class TestMainFunctionality:
    @allure.title("Переход по клику на 'Конструктор'")
    def test_click_on_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_button_constructor()
        assert main_page.check_displaying_of_selected_button, "Элемент не найден"

    @allure.title("Переход по клику на 'Лента заказов'")
    def test_click_on_feed(self, driver):
        main_page = MainPage(driver)
        main_page.click_header_feed_button()
        feed_page = FeedPage(driver)
        assert feed_page.check_displaying_section_order_list, "Элемент не найден"

    @allure.title("Получение деталей об ингридиенте")
    def test_get_ingridient_details(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_button_constructor()
        main_page.click_on_ingredient()
        assert main_page.check_displaying_of_modal_details(), "Окно отображается"


    @allure.title("Получение деталей об ингридиенте и закрытие окна")
    def test_get_ingridient_details_and_close_window(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_button_constructor()
        main_page.click_on_ingredient()
        main_page.check_displaying_of_modal_details()
        main_page.close_modal()
        assert main_page.check_not_displaying_of_modal_details(), "Окно не отображается"


    @allure.title("Увеличение каунтера ингридиента")
    def test_increase_counter(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_button_constructor()
        before_drop = main_page.get_count_of_ingredients()
        main_page.add_ingredient_to_order_with_js()
        after_drop = main_page.get_count_of_ingredients()
        assert after_drop > before_drop, "Каунтер не увеличился"


    @allure.title("Залогиненный юзер может оформить заказ")
    def test_click_on_order_history(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page = AccountPage(driver)
        account_page.login_user(user_data['email'], user_data['password'])
        main_page.add_ingredient_to_order_with_js()
        main_page.click_on_button_make_order()
        main_page.check_displaying_of_confirmation_modal_of_order()
        main_page.get_number_of_order_in_modal_confirmation()
        main_page.click_on_button_close_confirmation_modal()
        assert main_page.get_current_url() == Urls.base_url, "Ошибка подтверждения заказа"


