import os

import pandas as pd
from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel
from pyspark.sql import SparkSession

# from pyspark import
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clothing.settings")
import django

django.setup()

from user.models import Rate, Clothing

os.environ['SPARK_HOME'] = '/usr/local/Cellar/apache-spark/2.4.5/libexec'


# sys.path.append('/usr/local/Cellar/apache-spark/2.4.5/libexec')
# sys.path.append('D:\spark-3.0.0-preview2-bin-hadoop2.7\python')
# als_model_path='../data/als-m'
class AlsModel(object):
    _instance = None
    als = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, k=10):
        self.k = k
        self.spark = SparkSession.builder.appName("clothes").enableHiveSupport().getOrCreate()

    def build(self, data):
        print('this is data', data)
        sparkDF = self.spark.createDataFrame(data)
        als = ALS.train(sparkDF, self.k, 5)
        pre = als.recommendProducts(600, self.k)
        self.als = als
        print(pre)
        self.save_model(self.spark.sparkContext, als)
        return als

    def save_model(self, sc, model):
        """存储模型"""
        # try:
        path = "./model_data/als-model"
        try:
            os.rmdir('./model_data/als-model/metadata')
            os.rmdir('./model_data/als-model/data')
        except FileNotFoundError:
            pass
        model.save(sc, path)
        print('save success')
        # except Mo Exception:
        # print("模型已存在,先删除后创建")
        return model

    def train(self):
        data = load_all_ratings()
        return self.build(data=data)

    def load_model(self):
        sc = self.spark.sparkContext
        try:
            model = MatrixFactorizationModel.load(sc, "./model_data/als-model")
            print('载入成功!')
            return model
        except Exception:
            print("模型不存在, 请先训练模型")
            return self.train()


def load_all_ratings(min_ratings=1):
    # 提取相关列的数据
    columns = ['clothing_id', 'user_id', 'mark']
    ratings_data = Rate.objects.all().values(*columns)
    ratings = pd.DataFrame.from_records(ratings_data, columns=columns)
    ratings['clothing_id'] = ratings['clothing_id'].astype(int)
    ratings['user_id'] = ratings['user_id'].astype(int)
    ratings['mark'] = ratings['mark'].astype(float)
    return ratings


def asl_recommend_by_user_id(user_id):
    res = model.recommendProducts(user_id, 10)
    clothes_list = []
    for rating in res:
        clothes_id = rating.product
        clothes_list.append(Clothing.objects.filter(id=clothes_id).first())
    return clothes_list


print('load als....')
als = AlsModel(k=10)
model = als.load_model()