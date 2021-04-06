from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
import logging
from conf import Config

class Scraping:
    def __init__(self, uri, award_number=""):
        self._uri = uri
        self._award_number = award_number
        self._data = []
        self._control_number = 0
        logging.basicConfig(filename='logs/scrapping.log', level=logging.INFO)

    def scrap_award(self):
        # with webdriver.Firefox() as driver:
        with webdriver.Firefox(executable_path=r'geckodriver/geckodriver') as driver:
            wait = WebDriverWait(driver, 10)
            driver.get(self._uri)
            driver.find_element(By.ID, 'buscaConcurso').send_keys(self._award_number + Keys.ENTER)
            while True:
                try:
                    time.sleep(2)
                    award_data = driver.find_element_by_class_name("title-bar.clearfix").\
                        find_element_by_tag_name("span").text
                    logging.info(f'{time.strftime("%m/%d/%Y %I:%M:%S %p")}: Raspando dados do {award_data}')
                    lucky_numbers = self._get_lucky_numbers(driver.find_element_by_id("ulDezenas").find_elements_by_tag_name("li"))
                    winners_data = driver.find_element_by_class_name("related-box.gray-text.no-margin").text
                    forecast_data = driver.find_element_by_class_name("totals").text
                    consolidated = [award_data, lucky_numbers, winners_data, forecast_data]
                    self._data.append(consolidated)
                    current_award = self._loop_control(award_data)
                    print(f"controle {self._control_number} | atual {current_award}")
                    if current_award != self._control_number:
                        self._control_number = current_award
                    else:
                        logging.info(f'{time.strftime("%m/%d/%Y %I:%M:%S %p")}: Fim da execução')
                        Config.set_last_prize(str(self._control_number + 1))
                        break
                    time.sleep(10)
                    driver.find_element_by_css_selector("a[ng-click='carregaProximoConcurso()']").click()
                except UnexpectedAlertPresentException as AlertE:
                    logging.info(f'{time.strftime("%m/%d/%Y %I:%M:%S %p")}: Chegamos no fim da página')
                    logging.error(f'{AlertE.msg} | {AlertE.alert_text}')
                    break
                except Exception as e:
                    logging.error(f'{time.strftime("%m/%d/%Y %I:%M:%S %p")}: Ocorreu um erro não esperado')
                    logging.error(f'-->{e.args}')
                    logging.error(f'--> {award_data}')
                    break
        return self._data

    @staticmethod
    def _loop_control(award_data):
        info = award_data.split(" ")
        return int(info[1])

    @staticmethod
    def _get_lucky_numbers(data):
        number_set = []
        for number in data:
            number_set.append(number.get_attribute("innerHTML"))
        return number_set