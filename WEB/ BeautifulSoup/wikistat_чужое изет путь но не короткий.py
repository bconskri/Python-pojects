from bs4 import BeautifulSoup
import unittest
import re
import os

def build_tree(path, start, end):
    link_re = re.compile(r"(?<=/wiki/)[\w()]+")  # Искать ссылки можно как угодно, не обязательно через re
    files = dict.fromkeys(os.listdir(path))  # Словарь вида {"filename1": None, "filename2": None, ...}
    # TODO Проставить всем ключам в files правильного родителя в значение, начиная от start
    link_list = [start]
    while link_list:
        for id, link in enumerate(link_list):
            with open("{}{}".format(path, link), encoding='utf-8') as data:
                file_links = link_re.findall(data.read())
                for lnk in [i for i in file_links if i in files.keys()]:
                    if files.get(lnk) is None:
                        files[lnk] = link
                        if lnk == end:
                            return files
                        link_list.append(lnk)
            link_list.pop(id)
    return files


# Вспомогательная функция, её наличие не обязательно и не будет проверяться
def build_bridge(path, start, end):
    files = build_tree(path, start, end)
    # TODO Добавить нужные страницы в bridge
    parent = end
    bridge = [parent]
    while parent != start:
        parent = files[parent]
        if parent is not None:
            bridge.append(parent)
        else:
            bridge.append(start)
            parent = start
    return bridge[::-1]


def get_statistics(path, start_page, end_page):

    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""

    statistics = {}
    # получаем список страниц, с которых необходимо собрать статистику
    bridge = build_bridge(path, start_page, end_page)
    for page in bridge:
        # statistics = [sum(i) for i in zip(statistics, parse(path+page))]
        statistics[page] = parse(path+page)

    print(statistics)

def parse(path_to_file):    
    # Поместите ваш код здесь.
    # ВАЖНО!!!
    # При открытии файла, добавьте в функцию open необязательный параметр
    # encoding='utf-8', его отсутствие в коде будет вызвать падение вашего
    # решения на грейдере с ошибкой UnicodeDecodeError
    with open(path_to_file, encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'lxml')

        body = soup.find(id="bodyContent")

        img_counts = len(body('img', width=lambda x: int(x or 0) >= 200))

        h_counts = len([i.text for i in body(name=re.compile(r'[hH1-6]{2}')) if i.text[0] in 'ETC'])

        a_counts = 0
        a_found = body.find_all('a')
        for a in a_found:
            links = 1
            for i in a.find_next_siblings():
                if i.name == 'a':
                    links += 1
                else:
                    break

            a_counts = max(a_counts, links)

        l_count = 0
        lists_found = body(['ul', 'ol'])
        for l in lists_found:
            if not l.find_parents(['ul', 'ol']):
                l_count += 1

        # print([img_counts, h_counts, a_counts, l_count])

    return [img_counts, h_counts, a_counts, l_count]

# Набор тестов для проверки студентами решений по заданию "Практическое задание
# по Beautiful Soup - 2". По умолчанию файл с решением называется chain_of_respons.py,
# измените в импорте название модуля solution, если файл с решением имеет другое имя.

STATISTICS = {
    'Artificial_intelligence': [8, 19, 13, 198],
    'Binyamina_train_station_suicide_bombing': [1, 3, 6, 21],
    'Brain': [19, 5, 25, 11],
    'Haifa_bus_16_suicide_bombing': [1, 4, 15, 23],
    'Hidamari_no_Ki': [1, 5, 5, 35],
    'IBM': [13, 3, 21, 33],
    'Iron_Age': [4, 8, 15, 22],
    'London': [53, 16, 31, 125],
    'Mei_Kurokawa': [1, 1, 2, 7],
    'PlayStation_3': [13, 5, 14, 148],
    'Python_(programming_language)': [2, 5, 17, 41],
    'Second_Intifada': [9, 13, 14, 84],
    'Stone_Age': [13, 10, 12, 40],
    'The_New_York_Times': [5, 9, 8, 42],
    'Wild_Arms_(video_game)': [3, 3, 10, 27],
    'Woolwich': [15, 9, 19, 38]}

TESTCASES = (
    ('wiki/', 'Stone_Age', 'Python_(programming_language)',
     ['Stone_Age', 'Brain', 'Artificial_intelligence', 'Python_(programming_language)']),

    ('wiki/', 'The_New_York_Times', 'Stone_Age',
     ['The_New_York_Times', 'London', 'Woolwich', 'Iron_Age', 'Stone_Age']),

    ('wiki/', 'Artificial_intelligence', 'Mei_Kurokawa',
     ['Artificial_intelligence', 'IBM', 'PlayStation_3', 'Wild_Arms_(video_game)',
      'Hidamari_no_Ki', 'Mei_Kurokawa']),

    ('wiki/', 'The_New_York_Times', "Binyamina_train_station_suicide_bombing",
     ['The_New_York_Times', 'Second_Intifada', 'Haifa_bus_16_suicide_bombing',
      'Binyamina_train_station_suicide_bombing']),

    ('wiki/', 'Stone_Age', 'Stone_Age',
     ['Stone_Age', ]),
)


class TestBuildBrige(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = build_bridge(path, start_page, end_page)
                self.assertEqual(result, expected)


class TestGetStatistics(unittest.TestCase):
    def test_build_bridge(self):
        for path, start_page, end_page, expected in TESTCASES:
            with self.subTest(path=path,
                              start_page=start_page,
                              end_page=end_page,
                              expected=expected):
                result = get_statistics(path, start_page, end_page)
                self.assertEqual(result, {page: STATISTICS[page] for page in expected})


if __name__ == '__main__':
    unittest.main()
    #print(build_bridge("wiki/",'Stone_Age','Artificial_intelligence'))
    # get_statistics("wiki/",'Stone_Age','Artificial_intelligence')