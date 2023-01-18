"""
Описание задания

В этом задании вам требуется отправить POST запрос на следующий https://datasend.webpython.graders.eldf.ru/submissions/1/

В запросе должен содержаться заголовок Authorization со способом аутентификации Basic логином alladin и паролем opensesame закодированными в base64.

Authorization: Basic YWxsYWRpbjpvcGVuc2VzYW1l

Запрос можно отправить любым удобным для вас способом, но мы рекомендуем использовать библиотеку requests, так как она понадобится вам при выполнении последующих заданий.

В ответе на запрос вы получите инструкции для последующего запроса который приведет вас к специальному коду который является ответом на это задание.
"""
from base64 import b64encode

import requests as requests
from requests.auth import HTTPBasicAuth


def main():

    # data = requests.post(
    #     'https://datasend.webpython.graders.eldf.ru/submissions/1/',
    #     auth = HTTPBasicAuth('alladin', b64encode('YWxsYWRpbjpvcGVuc2VzYW1l'.encode('utf-8')))
    # ).json()

    data = requests.post(
        'https://datasend.webpython.graders.eldf.ru/submissions/1/',
        auth = HTTPBasicAuth('alladin', 'opensesame')
    ).json()

    print(data)

    data = requests.put(
        'https://datasend.webpython.graders.eldf.ru/submissions/secretlocation/',
        auth = HTTPBasicAuth('alibaba', '40razboinikov')
    ).json()

    print(data)


if __name__ == "__main__":
    main()
