from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class Helper():

    def __init__(self, driver, test_logger):
        self.driver = driver
        self.test_logger = test_logger

    def go_to_page(self, url):
        try:
            self.driver.get(url)
            self.test_logger.info(f"Successfully navigated to: {url}")
            return True
        except Exception as e:
            self.test_logger.error(f"Failed to navigate to {url}: {str(e)}")
            raise

    def find_element(self, loc, sec=60):
        try:
            elem = WebDriverWait(self.driver, sec).until(
                EC.visibility_of_element_located(loc))
            return elem
        except Exception as e:
            self.test_logger.error(f"Unexpected error finding element: {str(e)}")
            raise

    def find_elements(self, loc, sec=60):
        try:
            elem = WebDriverWait(self.driver, sec).until(
                EC.visibility_of_all_elements_located(loc))
            return elem
        except Exception as e:
            self.test_logger.error(f"Unexpected error finding element: {str(e)}")
            raise

    def find_elem_dom(self, loc, sec=60):
        try:
            elem = WebDriverWait(self.driver, sec).until(
                EC.presence_of_element_located(loc))
            return elem
        except Exception as e:
            self.test_logger.error(f"Unexpected error finding element: {str(e)}")
            raise

    def find_and_click(self, loc, sec=60):
        try:
            elem = WebDriverWait(self.driver, sec).until(EC.element_to_be_clickable(loc))
            elem.click()
        except Exception as e:
            self.test_logger.error(f"Unexpected error: {str(e)}")

    def find_and_send_keys(self, loc, inp_text, sec=60):
        elem = self.find_element(loc, sec)
        elem.send_keys(inp_text)

    def hover_to_element(self, by_locator, sec=60):

        element = WebDriverWait(self.driver, sec).until(
            EC.presence_of_element_located(by_locator)
        )
        ActionChains(self.driver).move_to_element(element).perform()
