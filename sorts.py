import time

import constants as cs
import pygame as pg
import random


class Sort:

    THEMES = [(cs.WHITE, cs.WHITE, cs.WHITE),
              (cs.WHITE, cs.LIGHT_GREY, cs.GREY),
              (cs.WHITE, cs.LIGHT_BLUE, cs.SKY_BLUE),
              (cs.WHITE, cs.LIGHT_GREEN, cs.LIME),
              (cs.WHITE, cs.LIGHT_PINK, cs.PINK),
              (cs.RED, cs.GREEN, cs.BLUE)]

    def __init__(self, size, theme=0):
        self.size = size
        self.theme = theme
        self.block_width = cs.WIDTH / self.size
        self.blocks = []
        self.max_height = int(self.size * self.block_width * cs.HEIGHT // cs.WIDTH) + 1
        self.flag = False
        self.colors = [self.THEMES[theme][i % 3] for i in range(self.size)]
        self.sorted = True
        self.control_color = cs.RED
        self.set_blocks()

    def set_colors(self):
        self.colors = [self.THEMES[self.theme][i % 3] for i in range(self.size)]
        self.control_color = cs.RED if self.theme != 5 else cs.WHITE

    def set_blocks(self):
        self.block_width = cs.WIDTH / self.size
        self.blocks = [pg.Rect(self.block_width * i, cs.HEIGHT - i * self.block_width * cs.HEIGHT // cs.WIDTH,
                               self.block_width, (i + 1) * self.block_width * cs.HEIGHT // cs.WIDTH)
                       for i in range(self.size)]
        self.set_colors()

    def shuffle(self):
        self.sorted = False
        for i in range(self.size):
            u = random.randint(0, self.size - 1)
            self.blocks[u].x, self.blocks[i].x = self.blocks[i].x, self.blocks[u].x
            self.blocks[u], self.blocks[i] = self.blocks[i], self.blocks[u]

    def reverse(self):
        self.sorted = False
        start, end = 0, self.size - 1
        while start < end:
            self.blocks[start].x, self.blocks[end].x, self.blocks[start], self.blocks[end] = \
                self.blocks[end].x, self.blocks[start].x, self.blocks[end], self.blocks[start]
            start += 1
            end -= 1

    def bubble_sort(self):
        if self.sorted: return
        for i in range(1, self.size):
            for j in range(self.size - i):
                if self.flag: return
                prev = self.colors[j], self.colors[j + 1]
                self.colors[j], self.colors[j + 1] = self.control_color, self.control_color
                if self.blocks[j].height > self.blocks[j + 1].height:
                    time.sleep(0.0001)
                    self.blocks[j].x, self.blocks[j + 1].x = self.blocks[j + 1].x, self.blocks[j].x
                    self.blocks[j], self.blocks[j + 1] = self.blocks[j + 1], self.blocks[j]
                self.colors[j], self.colors[j + 1] = prev
        self.sorted = True

    def insertion_sort(self):

        if self.sorted: return
        for i in range(1, self.size):
            if self.flag: return
            j = i - 1
            k = i
            key = self.blocks[i]
            while j >= 0 and key.h < self.blocks[j].h:
                if self.flag: return
                prev = self.colors[k], self.colors[j]
                self.colors[k], self.colors[j] = self.control_color, self.control_color
                time.sleep(0.001)
                self.colors[k], self.colors[j] = prev
                self.blocks[k].x, self.blocks[j].x = self.blocks[j].x, self.blocks[k].x
                self.blocks[k], self.blocks[j] = self.blocks[j], self.blocks[k]
                key = self.blocks[j]
                k = j
                j -= 1
        self.sorted = True

    def selection_sort(self):
        if self.sorted: return

        for i in range(self.size):
            idx = i

            for j in range(i + 1, self.size):
                prev = self.colors[idx], self.colors[j]
                self.colors[idx], self.colors[j] = self.control_color, self.control_color
                time.sleep(0.001)
                self.colors[idx], self.colors[j] = prev
                if self.blocks[idx].h > self.blocks[j].h:
                    idx = j
            self.blocks[idx].x, self.blocks[i].x = self.blocks[i].x, self.blocks[idx].x
            self.blocks[idx], self.blocks[i] = self.blocks[i], self.blocks[idx]

        self.sorted = True

    def quick_sort(self):
        if self.sorted: return

        def sort(p=0, q=self.size - 1):
            if p >= q or self.flag:
                return
            i = p - 1
            pivot = self.blocks[q]
            for j in range(p, q):
                if self.flag: return
                if self.blocks[j].height < pivot.height:
                    i += 1
                    prev = self.colors[j], self.colors[i]
                    self.colors[j], self.colors[i] = self.control_color, self.control_color
                    time.sleep(0.001)
                    self.colors[j], self.colors[i] = prev
                    self.blocks[i].x, self.blocks[j].x = self.blocks[j].x, self.blocks[i].x
                    self.blocks[i], self.blocks[j] = self.blocks[j], self.blocks[i]
            i += 1
            self.blocks[i].x, self.blocks[q].x = self.blocks[q].x, self.blocks[i].x
            self.blocks[i], self.blocks[q] = self.blocks[q], self.blocks[i]
            sort(p, i - 1)
            sort(i + 1, q)
        sort()
        if self.flag: return
        self.sorted = True

    def merge_sort(self):
        if self.sorted: return

        def merge(T, T1, T2, p):
            idx, i, j = 0, 0, 0
            n, m = len(T1), len(T2)
            while i < n and j < m:
                if self.flag: return
                prev = self.colors[i + p], self.colors[j + p + n]
                self.colors[i + p], self.colors[j + p + n] = self.control_color, self.control_color
                time.sleep(0.001)
                self.colors[i + p], self.colors[j + p + n] = prev
                if T1[i].h < T2[j].h:
                    T[idx] = T1[i]
                    i += 1
                    idx += 1
                else:
                    T[idx] = T2[j]
                    j += 1
                    idx += 1
            while i < n:
                if self.flag: return
                T[idx] = T1[i]
                i += 1
                idx += 1

            while j < m:
                if self.flag: return
                T[idx] = T2[j]
                j += 1
                idx += 1

        def sort(T, p):
            if len(T) <= 1 or self.flag:
                return
            half = len(T) // 2
            T1 = T[:half]
            T2 = T[half:]
            sort(T1, p)
            sort(T2, p + half)
            merge(T, T1, T2, p)
            for i, val in enumerate(T):
                if self.flag: return
                self.blocks[i + p] = val
                self.blocks[i + p].x = (i + p) * self.block_width

        t = self.blocks[:]
        sort(t, 0)
        if self.flag: return
        self.sorted = True

    def heap_sort(self):
        if self.sorted: return

        def left(i): return 2 * i + 1

        def right(i): return 2 * i + 2

        def parent(i): return (i - 1) // 2

        def heapify(i, n):
            l = left(i)
            r = right(i)
            idx = i
            if l < n and self.blocks[idx].h < self.blocks[l].h:
                idx = l
            if r < n and self.blocks[idx].h < self.blocks[r].h:
                idx = r
            if idx != i:
                prev = self.colors[i], self.colors[idx]
                self.colors[i], self.colors[idx] = self.control_color, self.control_color
                time.sleep(0.0001)
                self.colors[idx], self.colors[i] = prev
                self.blocks[i].x, self.blocks[idx].x = self.blocks[idx].x, self.blocks[i].x
                self.blocks[i], self.blocks[idx] = self.blocks[idx], self.blocks[i]
                self.colors[i], self.colors[idx] = self.colors[idx], self.colors[i]
                heapify(idx, n)

        for j in range(parent(self.size - 1), -1, -1):
            heapify(j, self.size)

        for j in range(self.size - 1, 0, -1):
            if self.flag: return
            self.blocks[j].x, self.blocks[0].x = self.blocks[0].x, self.blocks[j].x
            self.blocks[j], self.blocks[0] = self.blocks[0], self.blocks[j]
            self.colors[j], self.colors[0] = self.colors[0], self.colors[j]
            heapify(0, j)
        self.sorted = True
