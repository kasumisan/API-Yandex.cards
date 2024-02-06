import pygame
import requests
import sys
import os


class MapParams(object):
    def __init__(self):
        self.lat = 61.665279
        self.lon = 50.813492
        self.zoom = 16
        self.type = "map"

    def ll(self):
        return str(self.lon) + "," + str(self.lat)

    def increase_zoom(self):
        if self.zoom < 23:  # ограничение верхней границы масштаба
            self.zoom += 1

    def decrease_zoom(self):
        if self.zoom > 1:  # ограничение нижней границы масштаба
            self.zoom -= 1


def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)
    response = requests.get(map_request)

    if not response.ok:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"

    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    return map_file

