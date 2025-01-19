import pytest
from page_objects.reset_password import ResetPassword
from page_objects.main_page import MainPage
import allure


@pytest.mark.usefixtures("driver")
class TestPasswordRecovery:
    @allure.description("Переход на страницу восстановления пароля по кнопке «Восстановить пароль»")
    def test_navigate_to_password_recovery(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        reset_page = ResetPassword(driver)
        reset_page.navigate_to_reset_password_page()
        assert reset_page.check_displaying_of_input_email(), "Страница восстановления пароля не открылась"

    @allure.description("ввод почты и клик по кнопке «Восстановить»")
    def test_password_recovery_email_input(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        reset_page = ResetPassword(driver)
        reset_page.navigate_to_reset_password_page()
        reset_page.click_on_recovery_button()
        assert reset_page.check_displaying_of_input_password(), "Форма для ввода кода не появилась"

    @allure.description("работет включение видимости пароля")
    def test_toggle_password_visibility(self, driver):
        main_page = MainPage(driver)
        main_page.click_on_personal_account_in_header()
        reset_page = ResetPassword(driver)
        reset_page.navigate_to_reset_password_page()
        reset_page.click_on_recovery_button()
        reset_page.send_password()
        reset_page.click_on_eye_icon()
        assert reset_page.check_displaying_password_value(), "Поле пароля не подсветилось"