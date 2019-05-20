
import pandas as pd
import pymysql
import pkuseg
from wordcloud import WordCloud
import matplotlib.pyplot as plt


class ContentAnalyze():

    def __init__(self):
        self.conn = pymysql.Connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            passwd = 'root',
            db = 'lequ',
            charset = 'utf8',)
        self.sql = 'select * from content'
        self.most_reply_theme = []
        self.most_read_theme = []


    def get_data(self):
        data = pd.read_sql(self.sql, self.conn)

        # 按回复数对数据进行排序, ascending=False:从大到小排序, drop=True:重置索引并删除原来的索引
        reply_data = data.sort_values(by='reply_count', ascending=False).reset_index(drop=True)
        # 按查看书对数据进行排序
        read_data = data.sort_values(by='read_count', ascending=False).reset_index(drop=True)
        # 遍历获取前10,存入列表中
        for i in range(10):
            read_temp = {}
            reply_temp = {}
            reply_temp['name'] = reply_data.iloc[i]['name']
            reply_temp['content'] = reply_data.iloc[i]['content']
            reply_temp['public_time'] = reply_data.iloc[i]['public_time']
            reply_temp['read_count'] = reply_data.iloc[i]['read_count']
            reply_temp['reply_count'] = reply_data.iloc[i]['reply_count']

            read_temp['name'] = read_data.iloc[i]['name']
            read_temp['content'] = read_data.iloc[i]['content']
            read_temp['public_time'] = read_data.iloc[i]['public_time']
            read_temp['read_count'] = read_data.iloc[i]['read_count']
            read_temp['reply_count'] = read_data.iloc[i]['reply_count']
            self.most_reply_theme.append(reply_temp)
            self.most_read_theme.append(read_temp)



        return data

    def create_word_cloud(self, data):
        """
        制作乐趣帖子内容的词云图
        :param data: 帖子数据
        :return:
        """
        contents = ''.join(data['content'])
        seg = pkuseg.pkuseg()
        words = seg.cut(contents)
        with open('stopwords.txt', 'r', encoding='utf-8') as f:
            stop_word = f.read().split()
        stop_word.extend(['uqee', 'bid', 'nxzb'])
        words = ' '.join([x for x in words if x not in stop_word])

        wd = WordCloud(
            font_path='./simhei.ttf',
            width=600,
            height=400,
            mask=plt.imread('back_01.jpg')
        )
        wd.generate(words)
        wd.to_file('lequ_content.png')

    def user_public_time(self, data):
        data['public_time'] = pd.to_datetime(data['public_time'])


    def run(self):
        data = self.get_data()
        self.create_word_cloud(data)


if __name__ == '__main__':
    content_analyze = ContentAnalyze()
    content_analyze.run()
    print('前10查看数的帖子:', content_analyze.most_read_theme)
    print('前10回复数的帖子:', content_analyze.most_reply_theme)

