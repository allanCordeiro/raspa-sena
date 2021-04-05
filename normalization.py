class Normalize:
    def __init__(self, data_to_normalize):
        self._header = data_to_normalize[0]
        self._lucky_numbers = data_to_normalize[1]
        self._award = data_to_normalize[2]
        self._forecast = data_to_normalize[3]
        self._data = {}

    def normalize_data(self):
        header = self._get_header(self._header)
        collection = self._get_collection(self._award)
        hits = self._get_award(self._award)
        forecast = self._get_forecast(self._forecast)

        self._data[header['prize_number']] = {
            "date": header['date'],
            "collection": collection,
            "award": hits,
            "next_award": forecast['next_award'],
            "nye_award": forecast['nye_award'],
            "lucky_numbers": self._lucky_numbers
        }
        return self._data

    @staticmethod
    def _get_header(data):
        f_format = {}
        info = data.split(" ")
        f_format["prize_number"] = info[1]
        f_format["date"] = info[2][1:][:-1]
        return f_format

    @staticmethod
    def _get_forecast(data):
        f_format = {}
        info = data.split("\n")
        next_award = info[0].split("R$")
        nye_award = info[2].split("R$")
        f_format["next_award"] = next_award[1][1:]
        f_format["nye_award"] = nye_award[1][1:]
        return f_format

    @staticmethod
    def _get_award(data):
        info = data.split("\n")
        result = {}
        # 6-hits
        if info[2] == "Não houve ganhadores":
            award = 0.0
            player = 0
        else:
            splitted = info[2].split(" ")
            award = splitted[4]
            player = splitted[0]
        result["6-hits"] = {"winners": player, "award": award}
        # 5-hits
        if info[4] == "Não houve ganhadores":
            award = 0.0
            player = 0
        else:
            splitted = info[4].split(" ")
            award = splitted[4]
            player = splitted[0]
        result["5-hits"] = {"winners": player, "award": award}
        # 4-hits
        if info[6] == "Não houve ganhadores":
            award = 0.0
            player = 0
        else:
            splitted = info[6].split(" ")
            award = splitted[4]
            player = splitted[0]
        result["4-hits"] = {"winners": player, "award": award}

        return result

    @staticmethod
    def _get_collection(data):
        info = data.split("Arrecadação total\n")
        f_format = info[1].split(" ")
        return f_format[1]

