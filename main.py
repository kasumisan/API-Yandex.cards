import pygame
import requests
import sys
import os


class MapParams:
    def __init__(self):
        self.lat = 51.765334
        self.lon = 55.124111
        self.zoom = 16
        self.type = "map"

    def ll(self):
        return f"{self.lon},{self.lat}"

    def increase_zoom(self):
        if self.zoom < 23:
            self.zoom += 1

    def decrease_zoom(self):
        if self.zoom > 1:
            self.zoom -= 1

    def move_up(self, step):
        if self.lat < 85 - step / 2 ** self.zoom:
            self.lat += step

    def move_down(self, step):
        if self.lat > -85 + step / 2 ** self.zoom:
            self.lat -= step

    def move_right(self, step):
        self.lon += step

    def move_left(self, step):
        self.lon -= step

        def set_map_type(self, map_type):
            if map_type in self.layers:            self.type = self.layers[map_type]


def draw_buttons(screen):
    font = pygame.font.Font('MP Manga.ttf', 36)

    map_button = font.render("Map", True, (255, 151, 187))
    screen.blit(map_button, (10, 10))

    satellite_button = font.render("Satellite", True, (255, 151, 187))
    screen.blit(satellite_button, (10, 50))

    hybrid_button = font.render("Hybrid", True, (255, 151, 187))
    screen.blit(hybrid_button, (10, 90))


def load_map(mp):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={mp.ll()}&z={mp.zoom}&l={mp.type}"
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


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapParams()
    step = 0.0001

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    mp.decrease_zoom()
                elif event.key == pygame.K_PAGEUP:
                    mp.increase_zoom()
                elif event.key == pygame.K_UP:
                    mp.move_up(step)
                elif event.key == pygame.K_DOWN:
                    mp.move_down(step)
                elif event.key == pygame.K_RIGHT:
                    mp.move_right(step)
                elif event.key == pygame.K_LEFT:
                    mp.move_left(step)

        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()

    pygame.quit()
    os.remove(map_file)


if __name__ == "__main__":
    main()
