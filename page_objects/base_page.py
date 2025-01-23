from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step('Подождать, пока элемент станет видимым')
    def wait_visibility_of_element(self, locator, timeout=10):

        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Элемент {locator} не стал видимым за {timeout} секунд."
        )

    @allure.step('Найти элемент на странице')
    def find_element_with_wait(self, locator, timeout=10):

        self.wait_visibility_of_element(locator, timeout)
        return self.driver.find_element(*locator)

    @allure.step('Кликнуть на элемент')
    def click_on_element(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator),
                message=f"Элемент {locator} не стал кликабельным в течение {timeout} секунд."
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            ActionChains(self.driver).move_to_element(element).click().perform()

        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="error_screenshot",
                          attachment_type=allure.attachment_type.PNG)
            raise Exception(f"Ошибка при клике на элемент {locator}: {e}")

    @allure.step('Кликнуть на элемент через JavaScript')
    def click_element_with_js(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator),
                message=f"Элемент {locator} не найден за {timeout} секунд."
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="error_screenshot_js",
                          attachment_type=allure.attachment_type.PNG)
            raise Exception(f"Ошибка при клике на элемент через JS {locator}: {e}")

    @allure.step('Ввести значение в поле ввода')
    def send_keys_to_input(self, locator, keys):
        self.driver.find_element(*locator).send_keys(keys)


    @allure.step('Получить текст на элементе')
    def get_text_on_element(self, locator):
        self.wait_visibility_of_element(locator)
        return self.driver.find_element(*locator).text


    @allure.step('Проверить отображение элемента')
    def check_displaying_of_element(self, locator):
        return self.driver.find_element(*locator).is_displayed()

    @allure.step('Подождать, пока элемент закроется')
    def wait_for_closing_of_element(self, locator):
        WebDriverWait(self.driver, 5).until_not(EC.visibility_of_element_located(locator))

    @allure.step('Проверить кликабельность элемента')
    def check_element_is_clickable(self, locator, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент {locator} не стал кликабельным в течение {timeout} секунд."
        )

    @allure.step('Подождать смену текста на элементе')
    def wait_for_element_to_change_text(self, locator, value):
        return WebDriverWait(self.driver, 10).until_not(EC.
                                                        text_to_be_present_in_element(locator, value))


    @allure.step('Вернуть адрес текущей страницы')
    def get_current_url(self):
        return self.driver.current_url


    @allure.step('получить адрес текущей страницы с ожиданием')
    def get_current_url_with_wait(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.url_changes(self.driver.current_url)
        )
        return self.driver.current_url

    @allure.step('Перетаскивание ингридиента')
    def drag_and_drop_with_js(self, source_locator, target_locator):
        source = self.find_element_with_wait(source_locator)
        target = self.find_element_with_wait(target_locator)
        self.driver.execute_script(
            """
            function simulateDragDrop(sourceNode, destinationNode) {
                var EVENT_TYPES = {
                    DRAG_END: 'dragend',
                    DRAG_START: 'dragstart',
                    DROP: 'drop'
                };

                function createCustomEvent(type) {
                    var event = new CustomEvent('CustomEvent');
                    event.initCustomEvent(type, true, true, null);
                    event.dataTransfer = {
                        data: {},
                        setData: function(type, val) {
                            this.data[type] = val;
                        },
                        getData: function(type) {
                            return this.data[type];
                        }
                    };
                    return event;
                }

                function dispatchEvent(node, type, event) {
                    if (node.dispatchEvent) {
                        return node.dispatchEvent(event);
                    }
                    if (node.fireEvent) {
                        return node.fireEvent('on' + type, event);
                    }
                }

                var event = createCustomEvent(EVENT_TYPES.DRAG_START);
                dispatchEvent(sourceNode, EVENT_TYPES.DRAG_START, event);

                var dropEvent = createCustomEvent(EVENT_TYPES.DROP);
                dropEvent.dataTransfer = event.dataTransfer;
                dispatchEvent(destinationNode, EVENT_TYPES.DROP, dropEvent);

                var dragEndEvent = createCustomEvent(EVENT_TYPES.DRAG_END);
                dragEndEvent.dataTransfer = event.dataTransfer;
                dispatchEvent(sourceNode, EVENT_TYPES.DRAG_END, dragEndEvent);
            }

            simulateDragDrop(arguments[0], arguments[1]);
            """,
            source, target
        )

