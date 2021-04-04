from scraping import Scraping

def main():
    data = []
    scraping = Scraping(
        'http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/',
        '2300'
    )
    data = scraping.scrap_award()
    print(data)

if __name__ == '__main__':
    main()