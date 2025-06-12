from selenium import webdriver
import pytest
import logging
import os
from datetime import datetime
# import allure


@pytest.fixture()
def test_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture()
def test_logger(request):
    today_date = datetime.today().date()
    os.makedirs(f"logs_{today_date}", exist_ok=True)
    test_name = request.node.name
    log_path = os.path.join(f"logs_{today_date}", test_name)

    # Configure logger
    logger = logging.getLogger(test_name)
    file_handler = logging.FileHandler(log_path, mode='a')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    logger.info(f'{test_name} is started')
    yield logger 
    logger.info(f'{test_name} is finished')
