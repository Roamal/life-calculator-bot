import requests

class getLiveByCountrySex:
    def __init__(self, user_country, user_sex):
        self.user_sex = user_sex.lower()
        self.user_country = user_country.lower()
        

        sex_codes = {
            "m": 'SEX_MLE',    # Мужчины
            "f": 'SEX_FMLE'    # Женщины
        }


        country_codes = {
            'россия': 'RUS',
            'рф': 'RUS',
            'russia': 'RUS',
            'сша': 'USA',
            'америка': 'USA',
            'usa': 'USA',
            'united states': 'USA',
            'китай': 'CHN',
            'china': 'CHN',
            'германия': 'DEU',
            'germany': 'DEU',
            'франция': 'FRA',
            'france': 'FRA',
            'великобритания': 'GBR',
            'great britain': 'GBR',
            'united kingdom': 'GBR',
            'англия': 'GBR',
            'япония': 'JPN',
            'japan': 'JPN',
            'канада': 'CAN',
            'canada': 'CAN',
            'австралия': 'AUS',
            'australia': 'AUS',
            'бразилия': 'BRA',
            'brazil': 'BRA',
            'индия': 'IND',
            'india': 'IND',
            'италия': 'ITA',
            'italy': 'ITA',
            'испания': 'ESP',
            'spain': 'ESP',
            'украина': 'UKR',
            'ukraine': 'UKR',
            'казахстан': 'KAZ',
            'kazakhstan': 'KAZ',
            'беларусь': 'BLR',
            'belarus': 'BLR',
            'польша': 'POL',
            'poland': 'POL',
            'турция': 'TUR',
            'turkey': 'TUR',
            'южная корея': 'KOR',
            'south korea': 'KOR',
            'korea': 'KOR',
            'мексика': 'MEX',
            'mexico': 'MEX'
        }

        # Проверяем, есть ли страна в словаре
        if self.user_country not in country_codes:
            available_countries = ", ".join(sorted(country_codes.keys()))
            raise ValueError(f"Страна '{user_country}' не найдена. Доступные страны: {available_countries}")

        # Проверяем пол
        if self.user_sex not in sex_codes:
            raise ValueError(f"Пол '{user_sex}' не поддерживается. Используйте 'm' или 'f'")

        try:
            url = "https://ghoapi.azureedge.net/api/WHOSIS_000001"
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус ответа
            data = response.json()

            # Ищем записи по стране и полу
            records = [
                record for record in data['value'] 
                if record.get('SpatialDim') == country_codes[self.user_country] 
                and record.get('Dim1') == sex_codes[self.user_sex]
            ]

            if not records:
                raise ValueError(f"Данные для страны '{user_country}' и пола '{user_sex}' не найдены")

            # Находим самую свежую запись
            latest_record = max(records, key=lambda x: x['TimeDim'])
            self.life_mean = float(latest_record['NumericValue'])

        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API: {e}")
        except KeyError as e:
            raise ValueError(f"Некорректный формат данных от API: отсутствует ключ {e}")
        except Exception as e:
            raise RuntimeError(f"Ошибка при получении данных: {e}")

    def HowMuchRemained(self):
        """Возвращает среднюю продолжительность жизни в годах"""
        return self.life_mean

    def __str__(self):
        return f"Средняя продолжительность жизни: {self.life_mean} лет"

    def __repr__(self):
        return f"getLiveByCountrySex(country='{self.user_country}', sex='{self.user_sex}', life_expectancy={self.life_mean})"