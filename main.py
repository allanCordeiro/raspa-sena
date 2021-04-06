import json
from scraping import Scraping
from normalization import Normalize
from conf import Config

def main():
    uri = Config.get_config('uri')
    prize = Config.get_config('last_prize_scraped')
    final_json = []
    scraping = Scraping(
        uri,
        prize
    )
    data = scraping.scrap_award()
    for line in data:
        normalize = Normalize(line)
        final_json.append(normalize.normalize_data())

    with open('data/megasena.json', 'w') as outfile:
        json.dump(final_json, outfile)

if __name__ == '__main__':
    main()