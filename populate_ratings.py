import csv
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing.settings')
import django

django.setup()

from user.models import Rate, User, Clothing
from populate_clothings_script import random_user_name, random_phone
from django.db.utils import IntegrityError


# def delete_db():
#     print('truncate db')
#     count = Rate.objects.all().count()
#     if count > 1:
#         Rate.objects.all().delete()
#     print('finished truncate db')
#

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
                user = User.objects.create(name=username, password=username, address=username, phone=random_phone(), id=user_id)
                break
            except IntegrityError:
                print('name repeat !')
                username = random_user_name()
        print('create_user!!', user.id)
    rating, created = Rate.objects.get_or_create(user_id=user_id, clothing_id=clothing_id, mark=rating)


def populate_rating_csv():
    # 数据清洗
    opener = open('ratings.csv', 'r')
    data = csv.reader(opener)
    # ['user_id', 'clothingId', 'rating', 'timestamp'])
    # df1 = pd.read_csv("data/clothing.csv", index_col=0)
    for da in list(data)[1:]:
        print(da)
        create_rating(da[0], da[1], da[2])
    print('data process done!')


if __name__ == '__main__':
    print("Starting ClothingRec Population data...")
    # delete_db()
    populate_rating_csv()
