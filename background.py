from classes import *


def set_background(window, sort: sorts.Sort, sort_info, plus: VariationButton, minus: VariationButton,
                   theme_text, theme_color):
    pg.draw.line(window, cs.CYAN, (cs.WIDTH, 0), (cs.WIDTH, cs.HEIGHT), width=2)
    for i, rect in enumerate(sort.blocks):
        pg.draw.rect(window, sort.colors[i], rect)
    for i, word in enumerate(sort_info):
        window.blit(word, (cs.WIDTH + center_text(word, cs.CONTROLS), i * cs.HEIGHT // 20))

    plus.draw(window)
    minus.draw(window)
    h = 0
    pg.draw.rect(window, theme_color, theme_text[1])
    for word in theme_text[0]:
        window.blit(word, (theme_text[1].x + center_text(word, theme_text[1].w), theme_text[1].y + h))
        h += word.get_height()
    pg.display.update()


def set_change_theme(window, themes: list[Theme], sort: sorts.Sort, back):

    for theme in themes:
        theme.draw(window)

    window.blit(back[0], back[1])

    for i, rect in enumerate(sort.blocks):
        pg.draw.rect(window, sort.colors[i], rect)

    pg.display.update()