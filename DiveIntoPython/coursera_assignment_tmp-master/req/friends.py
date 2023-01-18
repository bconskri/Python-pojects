'''
Необходимо написать клиент к API VK , который будет считать распределение возрастов друзей для указанного пользователя.
На вход подается username или user_id пользователя.
На выходе получаем список пар (<возраст>, <количество друзей с таким возрастом>),
отсортированный по убыванию по второму ключу (количество друзей) и по возрастанию по первому ключу (возраст).
Например:
[(26, 8), (21, 6), (22, 6), (40, 2), (19, 1), (20, 1)]
'''

import requests
from datetime import datetime

def calc_age(uid):
    vk_user = requests.get('https://api.vk.com/method/users.get',
                params={'v': '5.81', 'access_token': '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711', 'user_ids': uid})
    data = vk_user.json()
    print(data)
    print(data['response'][0]['id'])
    vk_user_friends = requests.get('https://api.vk.com/method/friends.get',
        params={'v': '5.81', 'access_token': '17da724517da724517da72458517b8abce117da17da72454d235c274f1a2be5f45ee711',
                'fields': 'bdate', 'user_id': data['response'][0]['id']})
    data = vk_user_friends.json()
    print(data)

    friends_ages_dict = {}
    for i in range(data['response']['count']):
        friend = data['response']['items'][i]
        if ('bdate' in friend) and len(friend['bdate'].split('.')) == 3:
            birthday_year = int(friend['bdate'].split('.')[2])
            friend_age = datetime.now().year - birthday_year
            friends_ages_dict[friend['id']] = friend_age

    age_count_dict = {}
    for key, value in friends_ages_dict.items():
        if value in age_count_dict:
            age_count_dict[value] += 1
        else:
            age_count_dict[value] = 1

    return sorted(list(age_count_dict.items()), key=lambda x: (-x[1], x[0]))

if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
