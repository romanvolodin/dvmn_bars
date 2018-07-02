import argparse
import json
import math


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def get_biggest_bar(json_data):
    return max(
        json_data,
        key=lambda bar: bar['properties']['Attributes']['SeatsCount']
    )


def get_smallest_bar(json_data):
    return min(
        json_data,
        key=lambda bar: bar['properties']['Attributes']['SeatsCount']
    )


def get_closest_bar(json_data, user_long, user_lat):

    def get_distance(bar, user_long, user_lat):
        bar_lat, bar_long = bar['geometry']['coordinates']
        return math.sqrt(
            (bar_long - user_long) ** 2 + (bar_lat - user_lat) ** 2
        )

    return min(
        json_data,
        key=lambda bar: get_distance(bar, user_long, user_lat)
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_data',
                        help='path to bars data in json format')
    args = parser.parse_args()

    path = args.input_data
    json_data = load_data(path)['features']

    def print_bar(bar, bar_type):
        bar = bar['properties']['Attributes']
        print(bar_template.format(
            type=bar_type.lower(),
            name=bar['Name'],
            phone=bar['PublicPhone'][0]['PublicPhone'],
            address=bar['Address'],
            seats=bar['SeatsCount'],
        ))


    bar_template = '''
Самый {type} бар:
{name}
Телефон: {phone}
Адрес: {address}
Число мест: {seats}'''

    message = '''
Введите ваши координаты и мы покажем ближайший бар!
Координаты удобно скопировать в картах Гугла или Яндекса.
Например: 55.752631, 37.621418
'''

    print(message, end='')

    user_input = input().strip()
    try:
        user_long, user_lat = user_input.split(', ')
        user_long = float(user_long)
        user_lat = float(user_lat)
    except ValueError:
        print('Ошибка: Координаты должны быть в формате: XX.XXX, YY.YYY')
        exit()

    closest_bar = get_closest_bar(json_data, user_long, user_lat)
    biggest_bar = get_biggest_bar(json_data)
    smallest_bar = get_smallest_bar(json_data)

    print_bar(closest_bar, 'близкий')
    print_bar(biggest_bar, 'большой')
    print_bar(smallest_bar, 'маленький')

