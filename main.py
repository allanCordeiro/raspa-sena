import json
from scraping import Scraping
from normalization import Normalize
from conf import Config


def get_data():
    empty_data = []
    try:
        with open('data/megasena.json', 'r') as outfile:
            data = json.load(outfile)
            return data['data']
    except FileNotFoundError:
        return empty_data


def main():
    uri = Config.get_config('uri')
    prize = Config.get_config('last_prize_scraped')
    structure = {}
    final_json = get_data()
    scraping = Scraping(
        uri,
        prize
    )
    data = scraping.scrap_award()
    for line in data:
        normalize = Normalize(line)
        final_json.append(normalize.normalize_data())

    structure['data'] = final_json

    with open('data/megasena.json', 'w') as outfile:
        # json.dump(final_json, outfile)
        json.dump(structure, outfile)


if __name__ == '__main__':
    main()
