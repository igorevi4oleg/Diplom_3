import pytest
import allure
from page_objects.account_page import AccountPage
from page_objects.feed_page import FeedPage
from page_objects.main_page import MainPage

@pytest.mark.usefixtures("driver")
class TestOrderFeed:
    @allure.title("Получение деталей окна заказа")
    def test_order_details_popup(self, driver):
        main_page = MainPage(driver)
        main_page.click_header_feed_button()
        feed_page = FeedPage(driver)
        feed_page.click_on_order_card()
        assert feed_page.get_text_on_title_of_modal_order(), 'Окно не открыто'

    @allure.title("Заказ есть в ленте всех заказов")
    def test_new_order_found_in_feed(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page = AccountPage(driver)
        account_page.login_user(user_data['email'], user_data['password'])
        main_page.add_ingredient_to_order_with_js()
        main_page.click_on_button_make_order()
        main_page.check_displaying_of_confirmation_modal_of_order()
        number_order = f'0{main_page.get_number_of_order_in_modal_confirmation()}'
        main_page.click_on_button_close_confirmation_modal()
        main_page.click_header_feed_button()
        feed_page = FeedPage(driver)
        feed_page.wait_for_visibility_order_number(number_order)
        assert feed_page.check_for_visibility_order_number(number_order), f"Заказ {number_order} не найден в ленте заказов"

    @allure.title("Заказ увеличивает каунтер заказов за все время")
    def test_new_order_increases_counter_all_orders(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)
        main_page.click_header_feed_button()
        count_order_before = feed_page.get_quantity_of_orders()
        account_page = AccountPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page.login_user(user_data['email'], user_data['password'])
        main_page.add_ingredient_to_order_with_js()
        main_page.click_on_button_make_order()
        main_page.check_displaying_of_confirmation_modal_of_order()
        main_page.get_number_of_order_in_modal_confirmation()
        main_page.click_on_button_close_confirmation_modal()
        main_page.click_header_feed_button()
        count_order_after = feed_page.get_quantity_of_orders()
        assert count_order_after > count_order_before, "Каунтер не увеличился"

    @allure.title("Заказ увеличивает каунтер заказов за весь день")
    def test_new_order_increases_counter_daily_orders(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)
        main_page.click_header_feed_button()
        count_order_before = feed_page.get_daily_quantity_of_orders()
        account_page = AccountPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page.login_user(user_data['email'], user_data['password'])
        main_page.add_ingredient_to_order_with_js()
        main_page.click_on_button_make_order()
        main_page.check_displaying_of_confirmation_modal_of_order()
        main_page.get_number_of_order_in_modal_confirmation()
        main_page.click_on_button_close_confirmation_modal()
        main_page.click_header_feed_button()
        count_order_after = feed_page.get_daily_quantity_of_orders()
        assert count_order_after > count_order_before, "Каунтер не увеличился"

    @allure.title("Заказ есть в ленте в работе")
    def test_new_order_found_in_work(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)
        account_page = AccountPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page.login_user(user_data['email'], user_data['password'])
        main_page.add_ingredient_to_order_with_js()
        main_page.click_on_button_make_order()
        main_page.check_displaying_of_confirmation_modal_of_order()
        order_number = main_page.get_number_of_order_in_modal_confirmation()
        main_page.click_on_button_close_confirmation_modal()
        main_page.click_header_feed_button()
        feed_page.wait_for_visibility_order_number_in_work(order_number)
        assert feed_page.check_for_visibility_order_number_in_work(order_number), f"Заказ {order_number} не найден в ленте заказов"




