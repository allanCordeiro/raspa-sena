from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.support.expected_conditions import presence_of_element_located

def date_prize_no(data):
    return_info = {}
    info = data.split(" ")
    return_info["prize_number"] = info[1]
    return_info["date"] = info[2][1:][:-1]
    return return_info

def next_prize(data):
    return_info = {}
    info = data.split("\n")
    next_award = info[0].split("R$")
    nye_award = info[2].split("R$")
    return_info["next_award"] = next_award[1][1:]
    return_info["nye_award"] = nye_award[1][1:]
    return return_info

def hits(text):
    info = text.split("\n")
    result = {}
    #6-hits
    if info[2] == "Não houve ganhadores":
        award = 0.0
        player = 0
    else:
        splitted = info[2].split(" ")
        award = splitted[4]
        player = splitted[0]
    result["6-hits"] = {"winners": player, "award": award}
    #5-hits
    if info[4] == "Não houve ganhadores":
        award = 0.0
        player = 0
    else:
        splitted = info[4].split(" ")
        award = splitted[4]
        player = splitted[0]
    result["5-hits"] = {"winners": player, "award": award}
    #4-hits
    if info[6] == "Não houve ganhadores":
        award = 0.0
        player = 0
    else:
        splitted = info[6].split(" ")
        award = splitted[4]
        player = splitted[0]
    result["4-hits"] = {"winners": player, "award": award}

    return result

def collection(text):
    info = text.split("Arrecadação total\n")
    data = info[1].split(" ")
    return data[1]

def lucky_numbers(numbers):
    number_set = []
    for number in numbers:
        number_set.append(number.get_attribute("innerHTML"))

    return number_set

def consolida(header, collection, hits, forecast, lucky_numbers):
    retorna = {}
    retorna[header['prize_number']] = {
        "date": header['date'],
        "collection": collection,
        "award": hits,
        "next_award": forecast['next_award'],
        "nye_award": forecast['nye_award'],
        "lucky_numbers": lucky_numbers
    }
    return retorna


base_geral = []
with webdriver.Firefox(executable_path=r'geckodriver/geckodriver') as driver:
    wait = WebDriverWait(driver, 30)
    driver.get('http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/')
    driver.find_element(By.ID, "buscaConcurso").send_keys("2300" + Keys.ENTER)
    while True:
        try:
            # dados
            time.sleep(2)
            numbers_set = driver.find_element_by_id("ulDezenas")
            prize_numbers = lucky_numbers(numbers_set.find_elements_by_tag_name("li"))


            data_concurso = driver.find_element_by_class_name("title-bar.clearfix").find_element_by_tag_name("span")
            # print(data_concurso.text)
            info_inicial = date_prize_no(data_concurso.text)

            faixa_direita = driver.find_element_by_class_name("related-box.gray-text.no-margin")
            ganhadores = hits(faixa_direita.text)
            col = collection(faixa_direita.text)


            faixa_esquerda = driver.find_element_by_class_name("totals")
            previsao = next_prize(faixa_esquerda.text)



            base_geral.append(consolida(info_inicial, col, ganhadores, previsao, prize_numbers))
            driver.find_element_by_css_selector("a[ng-click='carregaProximoConcurso()']").click()
            time.sleep(1)
            if info_inicial["prize_number"] == '2357':
                break
        except UnexpectedAlertPresentException as e:
            break

    print(base_geral)
