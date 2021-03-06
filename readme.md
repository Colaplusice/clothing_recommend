# 毕业设计--基于Django的服装推荐系统和论坛

## 说明

1. 新手建议结合pycharm使用，https://www.jetbrains.com/pycharm/，下载专业版试用30天。
2. 注册用户通过web界面来设置，不用通过Django命令来设置
3. 导入服装信息通过insert_movies_script.py来操作 (会删除已有的所有信息!)
猜你喜欢和周推荐服装，通过协调过滤计算和其他用户的距离，然后进行筛选。如果用户数量不足，推荐数目不够15条，就会自动从
服装中按照浏览数选一部分填充进去。
4. 前端展示 浏览最多，评分最多，收藏最多，写的比较直白，你可以改的委婉点: 最热服装，火爆排行...之类的。每种有10条。

## 推荐部分的整体思路

### 基于用户的推荐

通过用户给服装打分来进行推荐，如果没有用户打分，则按照热度返回。
通过计算Pearson距离找到N个距离相近的用户
将这些用户中已打分的结果(推荐用户未看过的部分)返回。

### 基于item的推荐

1. 计算物品相似度矩阵: https://www.jianshu.com/p/27b1c035b693
2. 遍历当前用户已打分的item，计算和未打分的item的相似距离。
3. 对相似距离进行排序 返回




## feature

1.	登录注册页面
2.	基于协同过滤的服装的分类，排序，搜索，打分功能
3.	基于协同过滤的周推荐和月推荐
4. 观影分享会等活动功能，用户报名功能
5. 发帖留言论坛功能


## fixed

1. 首页导航栏链接错误
2. 首页面为空
3. 登录注册页面
4. 推荐跳转登录
5. 周推荐用户没有评分时随机推荐
6. 按照收藏数量排序
7. 重新设计了 action 和UserAction model，拆分出了UserAction


## 服装模型

1. 浏览量 每次刷新页面的浏览数
2. 收藏量 user manytomany field 每个用户收藏一次
3. 评分   rate 每个用户评分一次
4. 在服装下面的评论加点赞功能

## 安装运行方法

## 安装依赖

pip install -r requirements.txt

## 运行

python manage.py runserver

## 后台

## 创建管理员

python manage.py createsuperuser

## 进入后台
127.0.0.1:8000/admin

