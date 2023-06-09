from background import *
import threading


def main():
    algorithm = None
    algo_complexity = -1

    window = pg.display.set_mode((cs.WIDTH + cs.CONTROLS, cs.HEIGHT))
    run = True
    start = False

    theme = 0

    sort = sorts.Sort(cs.WIDTH, theme)

    sort_info = [cs.FONT.render("B - bubble sort", True, cs.WHITE),
                 cs.FONT.render("I - insertion sort", True, cs.WHITE),
                 cs.FONT.render("S - selection sort", True, cs.WHITE),
                 cs.FONT.render("Q - quick sort", True, cs.WHITE),
                 cs.FONT.render("M - merge sort", True, cs.WHITE),
                 cs.FONT.render("H - heap sort", True, cs.WHITE),
                 cs.FONT.render("", True, cs.WHITE),
                 cs.FONT.render("SPACE - shuffle", True, cs.WHITE),
                 cs.FONT.render("END - stop sort", True, cs.WHITE),
                 cs.FONT.render("TAB - reverse order", True, cs.WHITE)]

    plus = VariationButton(cs.BUTTON, cs.WIDTH + 2 * cs.PAD, (len(sort_info) + 1) * cs.HEIGHT // 20, True)
    minus = VariationButton(cs.BUTTON, cs.WIDTH + cs.CONTROLS - 2 * cs.PAD - cs.BUTTON,
                            (len(sort_info) + 1) * cs.HEIGHT // 20, False)
    n = wrap_text(cs.TXT, cs.FONT, cs.CONTROLS, cs.WHITE)
    complexities = [[cs.FONT.render("O(n\u00b2) time", True, cs.WHITE), cs.FONT.render("O(1) space",
                                                                                       True, cs.WHITE)] + n,
                    [cs.FONT.render("O(nlog(n)) time", True, cs.WHITE), cs.FONT.render("O(log(n)) space",
                                                                                       True, cs.WHITE)] + n,
                    [cs.FONT.render("O(nlog(n)) time", True, cs.WHITE), cs.FONT.render("O(n) space",
                                                                                       True, cs.WHITE)] + n
                    ]

    back_text = cs.FONT.render("BACK", True, cs.WHITE, cs.RED)
    back_rect = pg.Rect(cs.WIDTH + (cs.CONTROLS - back_text.get_width()) // 2, 0, back_text.get_width(),
                        back_text.get_height())
    back_text = [back_text, (back_rect.x, back_rect.y)]

    theme_count = len(sort.THEMES)
    back_height = back_text[0].get_height() + cs.PAD
    height = cs.HEIGHT - back_height
    themes = [Theme(T, cs.WIDTH + cs.PAD, i * height // theme_count + back_height,
                    cs.CONTROLS, height // theme_count) for i, T in enumerate(sort.THEMES)]

    theme_text = wrap_text("Select theme",  cs.FONT, minus.x - plus.x - 2 * cs.PAD - plus.size, cs.BLUE)
    theme_rect_h = sum([word.get_height() for word in theme_text])
    theme_rect = pg.Rect(plus.x + cs.PAD + plus.size, plus.y + (plus.size - theme_rect_h) // 2,
                         minus.x - plus.x - plus.size - 2 * cs.PAD, theme_rect_h)
    theme_text = [theme_text, theme_rect]
    rect_color = cs.WHITE
    themes[theme].selected = True
    in_rect = False

    while run:
        x, y = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_END:
                sort.flag = True
                start = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    if not start:
                        if check_mouse_hover(x, y, plus.background):
                            sort = plus.use(sort)
                            minus.in_use = plus.in_use
                            threading.Thread(target=lambda: plus.timeout_color(cs.RED, cs.WHITE, 0.1),
                                             daemon=True).start()
                        elif check_mouse_hover(x, y, minus.background):
                            sort = minus.use(sort)
                            plus.in_use = minus.in_use
                            threading.Thread(target=lambda: minus.timeout_color(cs.RED, cs.WHITE, 0.1),
                                             daemon=True).start()
                        elif check_mouse_hover(x, y, theme_rect):
                            theme_setting = True
                            while theme_setting:
                                new_x, new_y = pg.mouse.get_pos()
                                for e in pg.event.get():
                                    if e.type == pg.QUIT:
                                        theme_setting = False
                                        run = False
                                    if e.type == pg.KEYDOWN:
                                        if e.key == pg.K_ESCAPE:
                                            theme_setting = False
                                    if e.type == pg.MOUSEBUTTONDOWN:
                                        if e.button == pg.BUTTON_LEFT:
                                            if check_mouse_hover(new_x, new_y, back_rect):
                                                theme_setting = False
                                                break
                                            for i, val in enumerate(themes):
                                                if not val.selected and check_mouse_hover(new_x, new_y, val.bound):
                                                    themes[theme].selected = False
                                                    themes[i].selected = True
                                                    theme = i
                                                    sort.theme = theme
                                                    sort.set_colors()

                                window.fill(cs.BLACK)

                                if check_mouse_hover(new_x, new_y, back_rect):
                                    back_text[0] = cs.FONT.render("BACK", True, cs.RED, cs.WHITE)
                                else:
                                    back_text[0] = cs.FONT.render("BACK", True, cs.WHITE, cs.RED)

                                for i, val in enumerate(themes):
                                    if not val.selected:
                                        if check_mouse_hover(new_x, new_y, val.bound):
                                            themes[i].hovering = True
                                        else:
                                            themes[i].hovering = False

                                set_change_theme(window, themes, sort, back_text)

            if event.type == pg.KEYDOWN and not start:
                if event.key == pg.K_b:
                    sort.flag = False
                    bubble_sort = threading.Thread(target=sort.bubble_sort, daemon=True)
                    bubble_sort.start()
                    start = True
                    algorithm = wrap_text("Bubble Sort:", cs.FONT, cs.CONTROLS, cs.BLACK, cs.WHITE)
                    algo_complexity = 0
                if event.key == pg.K_SPACE:
                    sort.shuffle()
                if event.key == pg.K_i:
                    sort.flag = False
                    insertion_sort = threading.Thread(target=sort.insertion_sort, daemon=True)
                    insertion_sort.start()
                    start = True
                    algorithm = wrap_text("Insertion Sort:", cs.FONT, cs.CONTROLS, cs.BLACK, cs.WHITE)
                    algo_complexity = 0
                if event.key == pg.K_s:
                    sort.flag = False
                    selection_sort = threading.Thread(target=sort.selection_sort, daemon=True)
                    selection_sort.start()
                    start = True
                    algorithm = wrap_text("Selection Sort:", cs.FONT, cs.CONTROLS, cs.BLACK, cs.WHITE)
                    algo_complexity = 0
                if event.key == pg.K_q:
                    sort.flag = False
                    quick_sort = threading.Thread(target=sort.quick_sort, daemon=True)
                    quick_sort.start()
                    start = True
                    algorithm = wrap_text("Quick Sort:", cs.FONT, cs.CONTROLS, cs.BLACK, cs.WHITE)
                    algo_complexity = 1
                if event.key == pg.K_m:
                    sort.flag = False
                    merge_sort = threading.Thread(target=sort.merge_sort, daemon=True)
                    merge_sort.start()
                    start = True
                    algorithm = wrap_text("Merge Sort:", cs.FONT, cs.CONTROLS, cs.BLACK, cs.WHITE)
                    algo_complexity = 2
                if event.key == pg.K_h:
                    sort.flag = False
                    heap_sort = threading.Thread(target=sort.heap_sort, daemon=True)
                    heap_sort.start()
                    start = True
                    algorithm = wrap_text("Heap Sort:", cs.FONT, cs.CONTROLS, cs.BLACK, cs.WHITE)
                    algo_complexity = 1

                if event.key == pg.K_TAB:
                    sort.reverse()
        if start and sort.sorted:
            start = False
            end = threading.Thread(target=lambda: show_sorted(sort), daemon=True)
            end.start()

        if not run:
            break
        if not plus.press and check_mouse_hover(x, y, plus.background):
            in_rect = True
            plus.set_colors(cs.WHITE, cs.BLUE)
        elif not minus.press and check_mouse_hover(x, y, minus.background):
            in_rect = True
            minus.set_colors(cs.WHITE, cs.BLUE)
        elif check_mouse_hover(x, y, theme_rect):
            in_rect = True
            rect_color = cs.SKY_BLUE
            theme_text[0] = wrap_text("Select theme", cs.FONT, minus.x - plus.x - 2 * cs.PAD - plus.size, cs.WHITE)

        elif in_rect:
            in_rect = False
            if not plus.press: plus.set_colors(cs.BLUE, cs.WHITE)
            if not minus.press: minus.set_colors(cs.BLUE, cs.WHITE)
            theme_text[0] = wrap_text("Select theme", cs.FONT, minus.x - plus.x - 2 * cs.PAD - plus.size, cs.BLUE)
            rect_color = cs.WHITE
        window.fill((0, 0, 0))
        if algorithm is not None:
            m = len(complexities[algo_complexity])
            h = complexities[algo_complexity][-1].get_height()
            for i in range(m - 1, -1, -1):
                word = complexities[algo_complexity][i]
                window.blit(word, (cs.WIDTH + center_text(word, cs.CONTROLS), cs.HEIGHT - h))
                h += word.get_height()
            for word in algorithm:
                window.blit(word, (cs.WIDTH + center_text(word, cs.CONTROLS), cs.HEIGHT - h))
                h += word.get_height()
        set_background(window, sort, sort_info, plus, minus, theme_text, rect_color)


if __name__ == '__main__':
    main()
