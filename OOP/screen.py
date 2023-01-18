#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

SCREEN_DIM = (800, 600)


class Vec2d():
    """
    Реализовать класс 2-мерных векторов Vec2d
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, vec):
        return Vec2d(self.x + vec.x, self.y + vec.y)

    def __sub__(self, vec):
        return Vec2d(self.x - vec.x, self.y - vec.y)

    def __mul__(self, k):
        if isinstance(k, Vec2d):
            return self.x * k.x + self.y * k.y
        return Vec2d(self.x * k, self.y * k)

    def len(self, x):
        return (x.x ** 2 + x.y ** 2) ** .5

    def int_pair(self):
        return (int(self.x), int(self.y))

class Polyline:
    """
    Реализовать класс замкнутых ломаных Polyline с методами отвечающими за добавление в ломаную точки (Vec2d) c её
    скоростью, пересчёт координат точек (set_points) и отрисовку ломаной (draw_points).
    """
    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, point, speed):
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self):
        for i in range(len(self.points)):
            self.points[i] += self.speeds[i]
            if self.points[i].x > SCREEN_DIM[0] or self.points[i].x < 0:
                self.speeds[i] = Vec2d(- self.speeds[i].x, self.speeds[i].y)
            if self.points[i].y > SCREEN_DIM[1] or self.points[i].y < 0:
                self.speeds[i] = Vec2d(self.speeds[i].x, -self.speeds[i].y)

    def draw_points(self, display, color=(255, 255, 255), width=3, ):
        for p in self.points:
            pygame.draw.circle(display, color,
                               (int(p.x), int(p.y)), width)

class Knot(Polyline):
    """
    Реализовать класс Knot (наследник класса Polyline), в котором добавление и пересчёт координат инициируют вызов
    функции get_knot для расчёта точек кривой по добавляемым «опорным» точкам
    """
    def __init__(self, count):
        super().__init__()
        self.count = count
        self.knots = []

    def add_point(self, point, speed):
        super().add_point(point, speed)
        self.knots = self.get_knot()

    def set_points(self):
        super().set_points()
        self.knots = self.get_knot()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg]*alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self.count
        res = []
        for i in range(self.count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            return []
        res = []
        for i in range(-2, len(self.points) - 2):
            ptn = []
            ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
            ptn.append(self.points[i + 1])
            ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            res.extend(self.get_points(ptn))
        return res

    def draw_points(self, display, style="points", color=(255, 255, 255), width=3, ):
        """polyline drawing"""
        if style == "line":
            for p_n in range(-1, len(self.knots) - 1):
                pygame.draw.line(display, color,
                                 self.knots[p_n].int_pair(),
                                 self.knots[p_n + 1].int_pair(),
                                 width)

        elif style == "points":
            super().draw_points(display)

# =======================================================================================
# Функции отрисовки
# =======================================================================================
def draw_help():
    """функция отрисовки экрана справки программы"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = []
    data.append(["F1", "Show Help"])
    data.append(["R", "Restart"])
    data.append(["P", "Pause/Play"])
    data.append(["Num+", "More points"])
    data.append(["Num-", "Less points"])
    data.append(["", ""])
    data.append([str(steps), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


# =======================================================================================
# Основная программа
# =======================================================================================
if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")

    steps = 35
    working = True
    points = []
    speeds = []
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)

    knot = Knot(steps)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                knot.add_point(Vec2d(*event.pos), Vec2d(random.random() * 2, random.random() * 2))

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        knot.draw_points(gameDisplay)
        knot.draw_points(gameDisplay, "line", color)

        if not pause:
            knot.set_points()
        if show_help:
            draw_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
