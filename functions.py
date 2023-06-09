import pygame as pg
import sorts
import constants as cs
import time


def wrap_text(text: str, font: pg.font.Font, width: int, color: tuple[int, int, int], background=None):
    words = text.split()
    current = ''
    current_size = 0
    surfaces = []
    for i, word in enumerate(words):
        size = font.size(word)[0]
        if i < len(words) - 1: size += font.size(' ')[0]
        if current_size + size > width:
            surfaces.append(font.render(current, True, color, background))
            current = word + ' '
            current_size = size
        else:
            current_size += size
            current += word + ' '
    surfaces.append(font.render(current, True, color, background))
    return surfaces


def check_mouse_hover(x, y, rect):
    return 0 <= x - rect.x <= rect.w and 0 <= y - rect.y <= rect.h


def center_text(text: pg.Surface, width: int):
    return (width - text.get_width()) // 2


def divisors(n):
    div = []
    for i in range(1, n + 1):
        if n % i == 0:
            div.append(i)
    return div

def show_sorted(sort: sorts.Sort):
    for i in range(sort.size):
        sort.colors[i] = cs.RED
        time.sleep(0.001 * cs.WIDTH / sort.size)
        sort.colors[i] = cs.GREEN
    sort.set_colors()
