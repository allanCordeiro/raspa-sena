import json
from scraping import Scraping
from normalization import Normalize
from conf import Config

def main():
    data = []
    final_json = []
    scraping = Scraping(
        'http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/',
        '1250'
    )
    data = scraping.scrap_award()
    for line in data:
        normalize = Normalize(line)
        final_json.append(normalize.normalize_data())

    with open('data/megasena.json', 'w') as outfile:
        json.dump(final_json, outfile)

if __name__ == '__main__':
    # main()
    print(Config.get_config('last_prize_scraped'))
    Config.set_last_prize('1500')