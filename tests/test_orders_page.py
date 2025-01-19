import pytest
import allure
from page_objects.account_page import AccountPage
from page_objects.feed_page import FeedPage
from page_objects.main_page import MainPage
from locators.for_reset_password import ResetPasswordLocators
from locators.for_main_page import MainPageLocators

@pytest.mark.usefixtures("driver")
class TestOrderFeed:
    @allure.description("Получение деталей окна заказа")
    def test_order_details_popup(self, driver):
        main_page = MainPage(driver)
        main_page.click_header_feed_button()
        feed_page = FeedPage(driver)
        feed_page.click_on_order_card()
        assert feed_page.get_text_on_title_of_modal_order(), 'Окно не открыто'

    @allure.description("Заказ есть в ленте в работе")
    def test_order_from_history_absent_in_work(self, driver, create_new_user_and_delete):
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
        number_order = f'0{main_page.get_number_of_order_in_modal_confirmation()}'
        main_page.click_on_button_close_confirmation_modal()
        main_page.click_header_feed_button()
        feed_page = FeedPage(driver)
        main_page.wait_for_page_load()
        last_order_in_work = feed_page.get_order_number_in_feed_progress_section()
        assert number_order == last_order_in_work

    @allure.description("Заказ увеличивает каунтер заказов за все время")
    def test_new_order_increases_counter_all_orders(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)
        main_page.click_header_feed_button()
        count_order_before = feed_page.get_quantity_of_orders()
        account_page = AccountPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page.send_keys_to_input(ResetPasswordLocators.input_email, user_data['email'])
        account_page.send_keys_to_input(ResetPasswordLocators.input_password, user_data['password'])
        account_page.click_on_element(MainPageLocators.enter_button)
        main_page.add_ingredient_to_order_with_js()
        main_page.click_on_button_make_order()
        main_page.check_displaying_of_confirmation_modal_of_order()
        main_page.click_on_button_close_confirmation_modal()
        main_page.click_header_feed_button()
        count_order_after = feed_page.get_quantity_of_orders()
        assert count_order_after > count_order_before

    @allure.description("Заказ увеличивает каунтер заказов за все день")
    def test_new_order_increases_counter_daily_orders(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)
        main_page.click_header_feed_button()
        count_order_before = feed_page.get_daily_quantity_of_orders()
        account_page = AccountPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page.send_keys_to_input(ResetPasswordLocators.input_email, user_data['email'])
        account_page.send_keys_to_input(ResetPasswordLocators.input_password, user_data['password'])
        account_page.click_on_element(MainPageLocators.enter_button)
        main_page.add_ingredient_to_order_with_js()
        main_page.click_on_button_make_order()
        main_page.check_displaying_of_confirmation_modal_of_order()
        main_page.click_on_button_close_confirmation_modal()
        main_page.click_header_feed_button()
        count_order_after = feed_page.get_daily_quantity_of_orders()
        assert count_order_after > count_order_before

    @allure.description("Заказ есть в ленте всех заказов")
    def test_new_order_found_in_feed(self, driver, create_new_user_and_delete):
        main_page = MainPage(driver)
        feed_page = FeedPage(driver)
        account_page = AccountPage(driver)
        main_page.click_on_personal_account_in_header()
        user_data = create_new_user_and_delete[0]
        account_page.send_keys_to_input(ResetPasswordLocators.input_email, user_data['email'])
        account_page.send_keys_to_input(ResetPasswordLocators.input_password, user_data['password'])
        account_page.click_on_element(MainPageLocators.enter_button)
        main_page.add_ingredient_to_order_with_js()
        main_page.click_on_button_make_order()
        main_page.check_displaying_of_confirmation_modal_of_order()
        order_number = main_page.get_number_of_order_in_modal_confirmation()
        main_page.click_on_button_close_confirmation_modal()
        main_page.click_header_feed_button()
        main_page.wait_for_page_load()
        found_order = feed_page.find_order_number(order_number)
        assert found_order is not None, f"Заказ {order_number} не найден в ленте заказов"




