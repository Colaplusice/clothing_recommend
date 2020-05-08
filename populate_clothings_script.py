# 添加和读取数据到数据库中
import csv
import os
import random
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clothing.settings")
django.setup()
from django.db.utils import IntegrityError

from user.models import Clothing, Tags, User, Rate

strs = 'abcdefghijk_mnopqrstuvwxyz'


def get_sed():
    return random.randint(5, 10)


# 随机生成username
def random_user_name(length=5):
    return ''.join(random.choices(strs, k=length))


def random_phone():
    res = ''.join([str(random.randint(0, 9)) for _ in range(11)])
    return res


def random_clothing_id(num=5):
    book_nums = Clothing.objects.all().order_by('?').values('id')[:num]
    print(book_nums)
    return [book['id'] for book in book_nums]


def random_mark():
    return random.randint(1, 5)


def random_pic():
    return random.randint(1, 105)


def cleanup():
    print('警告: 运行此脚本将清空所有数据，退出请快按ctrl+c')
    for i in range(5):
        time.sleep(1)
        print('倒计时 ', 4 - i)
    Clothing.objects.all().delete()
    Tags.objects.all().delete()
    Rate.objects.all().delete()


def populate_clothing_csv():
    opener = open('clothing.csv', 'r')
    lines = csv.reader(opener)
    for line in list(lines)[1:]:
        clothing_id = line[1]
        user_id = line[2]
        cloth_name = line[3]
        if cloth_name == '':
            cloth_name = 'I like it !'
        intro = line[4]
        rating = line[5]
        tag = line[-1]
        name = random_user_name(10)
        phone = random_phone()
        try:
            user, created = User.objects.get_or_create(id=user_id, defaults={'username': name, 'name': name,
                                                                             'password': name,
                                                                             'phone': phone,
                                                                             'address': name,
                                                                             'email': name + '@163.com'
                                                                             })
        except:
            name = random_user_name(11)
            user, created = User.objects.get_or_create(id=user_id, defaults={'username': name, 'name': name,
                                                                             'password': name,
                                                                             'phone': phone,
                                                                             'address': name,
                                                                             'email': name + '@163.com'
                                                                             })

        tag, created = Tags.objects.get_or_create(name=tag)
        while True:
            try:
                clothing, created = Clothing.objects.get_or_create(id=clothing_id, defaults={
                    'intro': intro,
                    'tags': tag,
                    'pic': str(random_pic()),
                    'name': cloth_name
                })
                break
            except IntegrityError as e:
                print(e.args)
                # cloth_name = random_user_name()
                print('error, retried')
        Rate.objects.get_or_create(clothing=clothing, user=user, defaults={'mark': rating})
    print('populate clothing csv done!')


def create_rating(user_id, clothing_id, rating):
    user = User.objects.filter(id=user_id).first()
    username = random_user_name()
    clothing = Clothing.objects.filter(id=clothing_id).first()
    if clothing is None:
        print('clothing is none')
        return
    if user is None:
        while True:
            try:
                print()
                user = User.objects.create(name=username, password=username, address=username, phone=random_phone(), id=user_id, username=username)
                break
            except IntegrityError as e:
                print(e)
                print('name repeat !')
                username = random_user_name(get_sed())
                print(username)
        print('create_user!!', user.id)
    Rate.objects.get_or_create(user_id=user_id, clothing_id=clothing_id, mark=rating)


def populate_rating_csv():
    # 数据清洗
    opener = open('ratings.csv', 'r')
    data = csv.reader(opener)
    # ['user_id', 'clothingId', 'rating', 'timestamp'])
    # df1 = pd.read_csv("data/clothing.csv", index_col=0)
    for da in list(data)[1:]:
        print(da)
        create_rating(da[0], da[1], da[2])
    print('populating rating csv  done!')


def main():
    cleanup()
    populate_clothing_csv()
    populate_rating_csv()


if __name__ == '__main__':
    print('run')

    main()
