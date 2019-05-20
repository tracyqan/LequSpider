

import pymysql
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import dates as mdates

class LequUser:

    def __init__(self):

        self.conn = pymysql.Connect(
            host ='localhost',
            port = 3306,
            user = 'root',
            passwd = 'root',
            db = 'lequ',
            charset = 'utf8',
        )
        self.sql = 'select * from lequ_user'

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

    def get_data(self):

        data = pd.read_sql(self.sql, self.conn)
        data['create_time'] = data['create_time'].map(lambda x: x.split()[0])
        data['last_login'] = data['last_login'].map(lambda x: x.split()[0])
        data['reply_times'] = data['reply_times'].map(lambda x: np.abs(x))
        data['forum_money'] = data['forum_money'].map(lambda x: np.abs(x))

        return data

    # 绘制创建时间分布图
    def create_time(self, data):

        data = data[data['create_time'] != '1970-1-1']
        data['create_time'] = pd.to_datetime(data['create_time'])
        data['last_login'] = pd.to_datetime(data['last_login'])
        tempdata_create = data.set_index('create_time')
        tempdata_create = tempdata_create.resample('M').count()
        tempdata_login = data.set_index('last_login')
        tempdata_login = tempdata_login.resample('M').count()
        # print(tempdata_create)
        x_create = tempdata_create.index
        y_create = tempdata_create.loc[:, 'id']
        x_login = tempdata_login.index
        y_login = tempdata_login.loc[:, 'id']
        # print(x)
        # print(y_create)
        # print(y_login)
        plt.figure(figsize=(15, 7))
        plt.subplot(1, 2, 1)
        plt.plot(x_create, y_create, color='blue', linewidth=1.0, linestyle='-', label='创建账号')
        plt.legend()
        plt.title('乐趣论坛账号注册数分布图')
        plt.subplot(1, 2, 2)
        plt.plot(x_login, y_login, color='red', linewidth=1.0, linestyle='-', label='最后登录')
        # 显示图示
        plt.legend()

        plt.title('乐趣论坛账号最后登录数分布图')
        plt.savefig('lequ_create_time.png')
        plt.show()

    # 乐趣论坛账号在线时长条形图
    def active_time(self, data):

        active1 = data[data['active_time'] <= 100].count().id
        active2 = data[(data['active_time'] > 100) & (data['active_time'] <= 500)].count().id
        active3 = data[(data['active_time'] > 500) & (data['active_time'] <= 1000)].count().id
        active4 = data[(data['active_time'] > 1000) & (data['active_time'] <= 1500)].count().id
        active5 = data[(data['active_time'] > 1500) & (data['active_time'] <= 2000)].count().id
        active6 = data[(data['active_time'] > 2000) & (data['active_time'] <= 2500)].count().id
        active7 = data[(data['active_time'] > 2500) & (data['active_time'] <= 3000)].count().id
        active8 = data[(data['active_time'] > 3000) & (data['active_time'] <= 3500)].count().id
        active9 = data[(data['active_time'] > 3500) & (data['active_time'] <= 4000)].count().id
        active10 = data[(data['active_time'] > 4000) & (data['active_time'] <= 4500)].count().id
        active11 = data[(data['active_time'] > 4500) & (data['active_time'] <= 5000)].count().id
        active12 = data[data['active_time'] > 5000].count().id
        x = ['0-100', '100-500', '500-1000', '1000-1500', '1500-2000', '2000-2500', '2500-3000', '3000-3500',
             '3500-4000', '4000-4500', '4500-5000', '5000-10000']
        y = [active1, active2, active3, active4, active5, active6, active7, active8, active9, active10, active11,
             active12]
        fig = plt.figure(figsize=(13, 7))
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(x, y)
        ax.set_xlabel('在线时长')
        ax.set_ylabel('人数')
        plt.title('乐趣论坛账号在线时长条形图')
        plt.savefig('lequ_active_time.png')
        plt.show()

    # 乐趣论坛用户回复数与论坛币折线图
    def money_reply(self, data):

        data['reply_times'] = data['reply_times'].map(lambda x:np.abs(x))
        data['forum_money'] = data['forum_money'].map(lambda x:np.abs(x))
        x = data['reply_times']
        y = data['forum_money']
        plt.figure(figsize=(13,7))
        ax = sns.scatterplot(x, y)
        ax.set_xlabel('用户回复数')
        ax.set_ylabel('用户论坛币')
        plt.savefig('money_reply.png')
        plt.show()

    # 论坛用户等级分布
    def level(self, data):
        levels = data['identity'].value_counts()
        levels = levels.drop('勋章颁发')
        x = levels.index
        y = levels.get_values()
        fig = plt.figure(figsize=(13, 7))
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(x, y)
        ax.set_xlabel('等级')
        ax.set_ylabel('人数')
        ax.set_title('乐趣论坛玩家等级-人数')
        plt.savefig('level.png')
        plt.show()

if __name__ == '__main__':
    user_analyze = LequUser()
    data = user_analyze.get_data()
    user_analyze.create_time(data)
    user_analyze.active_time(data)
    user_analyze.money_reply(data)
    user_analyze.level(data)