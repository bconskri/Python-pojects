from bs4 import BeautifulSoup
import unittest
import re

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


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()
    # parse('wiki/Stone_Age')