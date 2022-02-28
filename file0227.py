import pandas as pd
import os


def remarkdvd(dfs):  # 去空格与分别取出用户名和评论
    a = dfs.split('：', 1)
    if dfs.find('：') == -1:
        a = ['', '']
    return a


def updatesDate(date):  # 修改错误日期数据
    month = date.split('月')[0].rjust(2, '0')
    day = date.split("月")[1].split("日")[0].rjust(2, '0')
    time = date.split("日")[1]
    if int(month) <= 2:
        year = '2022'
    elif int(month) >= 8:
        year = '2021'
    newdate = year+'-'+month+'-'+day+time
    return newdate


def timecpl(time):  # 字符串修正添加空格函数
    a = time[:-5]
    b = time[-5:]
    return a+' '+b


def colop(df):
    for x in df.index:
        if df.loc[x, 'main_article'].find('的微博视频') > -1:  # 检索是否有视频项
            df.loc[x, 'video'] = 1
        if df.loc[x, 'img'] == 'f查看大图':
            df.loc[x, 'img'] = 1
        else:
            df.loc[x, 'img'] = 0
        if df.loc[x, 'num_forward'] == '转发':  # 用于主贴
            df.loc[x, 'num_forward'] = 0
        if df.loc[x, 'num_mark'] == '评论':
            df.loc[x, 'num_mark'] = 0
        else:  # 切分用户名评论
            df.loc[x, 'mark_name'] = remarkdvd(df.loc[x, 'mark'])[0]
            df.loc[x, 'mark_value'] = remarkdvd(df.loc[x, 'mark'])[1]
        if df.loc[x, 'num_like'] == '赞':
            df.loc[x, 'num_like'] = 0
        if df.loc[x, 'mark_like'] == '赞':  # 用于一级回复
            df.loc[x, 'mark_like'] = 0
        if df.loc[x, 'reply_like'] == '赞':  # 用于二级回复
            df.loc[x, 'reply_like'] = 0

        if df.loc[x, 'reply'] != 0:  # 有二级回复
            df.loc[x, 'reply_name'] = remarkdvd(df.loc[x, 'reply'])[0]
            df.loc[x, 'reply_value'] = remarkdvd(df.loc[x, 'reply'])[1]
            if df.loc[x, 'reply_name'] == df.loc[x, 'blogger']:  # 是否有博主互动
                df.loc[x, 'interactive'] = 1

        # 检索是否有日期错误,主贴评论回复 # 日期补全
        if df.loc[x, 'main_time'] != '0':  # 线判断字段非空,main
            # print(df.loc[x, 'main_time'])
            # print(1)
            if df.loc[x, 'main_time'].find('月') > -1:
                df.loc[x, 'main_time'] = updatesDate(df.loc[x, 'main_time'])
            if df.loc[x, 'main_time'][:2] != '20':
                df.loc[x, 'main_time'] = '20'+df.loc[x, 'main_time']
            df.loc[x, 'main_time'] = timecpl(df.loc[x, 'main_time'])  # 时间补空格
            # print(df.loc[x, 'main_time'])
            # 日期形式转化
            df.loc[x, 'main_time'] = pd.to_datetime(df.loc[x, 'main_time'])
        if df.loc[x, 'mark_time'] != '0':  # mark
            # print(df.loc[x, 'mark_time'])
            # print(2)
            if df.loc[x, 'mark_time'].find('月') > -1:  # 检索是否有日期错误
                df.loc[x, 'mark_time'] = updatesDate(df.loc[x, 'mark_time'])
            if df.loc[x, 'mark_time'][:2] != '20':
                df.loc[x, 'mark_time'] = '20'+df.loc[x, 'mark_time']
            df.loc[x, 'mark_time'] = timecpl(df.loc[x, 'mark_time'])
            # print(df.loc[x, 'mark_time'])
            df.loc[x, 'mark_time'] = pd.to_datetime(df.loc[x, 'mark_time'])
        if df.loc[x, 'reply_time'] != '0':  # reply
            # print(df.loc[x, 'reply_time'])
            # print(3)
            if df.loc[x, 'reply_time'].find('月') > -1:  # 检索是否有日期错误
                df.loc[x, 'reply_time'] = updatesDate(df.loc[x, 'reply_time'])
            if df.loc[x, 'reply_time'][:2] != '20':
                df.loc[x, 'reply_time'] = '20'+df.loc[x, 'reply_time']
            df.loc[x, 'reply_time'] = timecpl(df.loc[x, 'reply_time'])
            df.loc[x, 'reply_time'] = pd.to_datetime(df.loc[x, 'reply_time'])
            # print(df.loc[x, 'reply_time'])
        # 日期格式化

    return df


def opera(filename):  # 文件操作函数
    df = pd.read_csv(filename)
    df.replace('\s+', '', regex=True, inplace=True)  # 去除空格
    df.drop_duplicates(inplace=True)  # 数据去重
    df['reply_like'].fillna(0, inplace=True)  # 缺省值替换
    df['reply'].fillna(0, inplace=True)
    df['reply_time'].fillna(0, inplace=True)
    df['mark_like'].fillna(0, inplace=True)
    df['mark'].fillna(0, inplace=True)
    df['mark_time'].fillna(0, inplace=True)
    df.insert(loc=7, column='mark_name', value=None)  # 增加新列（用户名和评论）
    df.insert(loc=8, column='mark_value', value=None)
    df.insert(loc=0, column='blogger', value=filename[:-4])  # 增加新列（微博名）
    df.insert(loc=3, column='video', value=0)  # 增加新列（是否视频）
    df.insert(loc=14, column='reply_name', value=0)  # 增加新列（回复用户名）
    df.insert(loc=15, column='reply_value', value=0)  # 增加新列（回复）
    df.insert(loc=17, column='interactive', value=0)  # 增加新列（是否互动）
    df['mark'] = df['mark'].astype(str)  # 字符串化
    df['main_time'] = df['main_time'].astype(str)  # 字符串化
    df['mark_time'] = df['mark_time'].astype(str)  # 字符串化
    df['reply_time'] = df['reply_time'].astype(str)  # 字符串化
    df = colop(df)  # 遍历操作

    df['mark_name'].fillna(0, inplace=True)  # 缺省值替换
    df['mark_value'].fillna(0, inplace=True)
    df.drop(columns='mark', inplace=True)  # 删除mark列
    df.drop(columns='reply', inplace=True)  # 删除mark列
    # print(df.iloc[50:100, 1])
    newfilename = 'new'+filename
    df.to_csv(newfilename)
    # print(df.info())


# path表示路径
path = os.getcwd()  # 获取当前工作路径
# print(os.getcwd())
# 返回path下所有文件构成的一个list列表
filelist = os.listdir(path)
print(filelist)
# 遍历输出每一个文件的名字和类型
# os.mkdir('new')  # 创建新文件夹
for item in filelist:
    # 输出指定后缀类型的文件
    if(item.endswith('.csv')):
        opera(item)  # 遍历文件操作
        print(item)


#  0   blogger       8419 non-null   object
#  1   main_time     8419 non-null   object
#  2   main_article  8419 non-null   object
#  3   video         8419 non-null   int64
#  4   img           8419 non-null   object
#  5   num_forward   8419 non-null   object
#  6   num_mark      8419 non-null   int64
#  7   num_like      8419 non-null   object
#  8   mark_name     8419 non-null   object
#  9   mark_value    8419 non-null   object
#  10  mark_time     8419 non-null   object
#  11  mark_like     8419 non-null   object
#  12  reply_name    8419 non-null   object
#  13  reply_value   8419 non-null   object
#  14  reply_time    8419 non-null   object
#  15  interactive   8419 non-null   int64
#  16  reply_like    8419 non-null   object
