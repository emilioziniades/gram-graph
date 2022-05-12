from math import pow, sqrt
from typing import Tuple, Callable, NamedTuple

from termcolor import cprint
import numpy as np


def print_green(text: str):
    cprint(text, "green")


def print_red(text: str):
    cprint(text, "red")


def print_yellow(text: str):
    cprint(text, "yellow")


def print_header(text: str):
    cprint(text, "grey", "on_white")


class Point(NamedTuple):
    x: float
    y: float


def find_gradient_and_intercept(p: Point, q: Point) -> Tuple[float, float]:
    grad = (p.y - q.y) / (p.x - q.x)
    intcpt = p.y - grad * p.x
    return grad, intcpt


def test_gradient_and_intercept():
    a = Point(0, 0)
    b = Point(2, 4)
    coef = find_gradient_and_intercept(a, b)
    assert coef == (2.0, 0.0)
    assert find_gradient_and_intercept(a, b) == find_gradient_and_intercept(b, a)


def dist(p: Point, q: Point):
    a, b = np.array(p), np.array(q)
    return np.linalg.norm(a - b, ord=2)


def test_dist():
    a = Point(0, 3)
    b = Point(4, 0)
    d = dist(a, b)
    assert d == 5.0
    a = Point(1, 0)
    b = Point(0, 1)
    d = dist(a, b)
    assert d == sqrt(2)


def shorten_line(p: Point, q: Point, delta: float):
    grad, intcpt = find_gradient_and_intercept(p, q)
    distance = dist(p, q)
    a = 1 + grad**2
    b = 2 * ((grad * intcpt) - p.x - (p.y * grad))
    c = p.x**2 + p.y**2 + intcpt**2 - (2 * p.y * intcpt) - (distance - delta) ** 2
    print(a, b, c)
    x_r, x_s = np.roots([a, b, c])
    r = Point(x_r, (grad * x_r) + intcpt)
    s = Point(x_s, (grad * x_s) + intcpt)
    if dist(q, r) < dist(q, s):
        return r
    else:
        return s


def test_shorten_line():
    a = Point(0, 0)
    b = Point(3, 4)
    delta = 1
    c = shorten_line(a, b, delta)
    assert dist(a, b) - delta == round(dist(a, c))
