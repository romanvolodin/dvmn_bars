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
        # I think SeatsCount == 0 means "no data"
        # so I ignore such bars
        [
            bar for bar in json_data
            if int(bar['properties']['Attributes']['SeatsCount']) > 0
        ],
        key=lambda bar: bar['properties']['Attributes']['SeatsCount']
    )


def get_closest_bar(json_data, long, lat):
    # The geo coordinates in the json data seem to be mixed up.
    # For example:
    # the first bar coordinates are [37.621587946152012, 55.765366956608361],
    # but Yandex says it should be [55.765366956608361, 37.621587946152012].

    geo = 'geometry'
    coords = 'coordinates'
    return min(
        json_data,
        key=lambda bar: math.sqrt(
            (bar[geo][coords][1] - long)**2 + (bar[geo][coords][0] - lat)**2
        )
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

    while True:
        user_input = input().strip()
        try:
            user_long, user_lat = user_input.split(', ')
            user_long = float(user_long)
            user_lat = float(user_lat)
            break
        except ValueError:
            print('Координаты должны быть в формате: XX.XXX, YY.YYY')

    closest = get_closest_bar(json_data, user_long, user_lat)
    biggest = get_biggest_bar(json_data)
    smallest = get_smallest_bar(json_data)

    print_bar(closest, 'близкий')
    print_bar(biggest, 'большой')
    print_bar(smallest, 'маленький')

