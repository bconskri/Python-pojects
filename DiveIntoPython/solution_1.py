"""
Программа принимает в качестве аргумента строку, состоящую из цифр.
Гарантируется, что других символов в переданном параметре нет и на вход всегда подается не пустая строка.
Программа должна вычислить сумму цифр из которых состоит строка и вывести полученный результат на печать в стандартный вывод.
"""

import sys

if __name__ == '__main__':
    digit_string = sys.argv[1]

    digit_sum = 0
    for d in digit_string:
        digit_sum += int(d)

    print(digit_sum)