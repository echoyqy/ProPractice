import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('项目/googleplaystore.csv')
# 简单的浏览数据
# print(df.head())
# print(df.shape)
print(df.count())
print(df.info())
print(df.describe())
print(df.isnull().sum())

# APP处理
# 查看有没有重复值
print(df["App"].value_counts())
# 也可以用的语句
# print(pd.unique(df["App"]).size)

# Category处理
# 数据处理-异常值
df['Category'].value_counts(dropna=False)
print(df['Category'].value_counts())
# 观察到了异常值
print(df[df['Category'] == '1.9'])
# 丢掉异常值
df.drop(index=10472, inplace=True)

# # 处理 Rating
print(df['Rating'].value_counts(dropna=False))
# # # 均值填充
df['Rating'].fillna(df['Rating'].mean(), inplace=True)
# print(df['Rating'].value_counts(dropna=False))

# # Reviews数据清洗
print(df['Reviews'].value_counts(dropna=False))
print(df['Reviews'].str.isnumeric().sum())
print('通过取反布尔值，取出非数值的结果。结果为空说明上一步删除的异常值就是--------------')
print(df[~df['Reviews'].str.isnumeric()])
print(df['Reviews'].dtypes)
df['Reviews'] = df['Reviews'].astype('int64')
print('转换后Reviews列数据类型--------------')
print(df['Reviews'].dtypes)

# # Size数据清洗
print(df['Size'].value_counts(dropna=False))
print(df['Size'].dtypes)
# 此刻里面有单位M， K，需处理
df['Size'] = df['Size'].str.replace('M', 'e+6')
df['Size'] = df['Size'].str.replace('k', 'e+3')
print(df['Size'].value_counts(dropna=False))


# 接下来处理异常数据Varies with device
# 想过要判断是不是所有异常值都在Varies with device中
# 自定义函数，判断每条数据是否可转换为数值型


def is_float(i):
    try:
        float(i)
        return True
    except:
        return False


result_f = df['Size'].apply(is_float)
print(result_f)
print(result_f.value_counts())
# 将字符Varies with device替换成0
df['Size'] = df['Size'].str.replace('Varies with device', '0')
# 类型转换
df['Size'] = df['Size'].astype('float64')
print(df['Size'].value_counts(dropna=False))
# 替换平均值
df['Size'].replace(0, df['Size'].mean(), inplace=True)

# 处理installs列
print(df['Installs'].value_counts(dropna=False))
# 替换
df['Installs'] = df['Installs'].str.replace('+', '')
df['Installs'] = df['Installs'].str.replace(',', '')
print(df['Installs'].value_counts(dropna=False))
df['Installs'] = df['Installs'].astype('int64')

# 处理type列
print(df['Type'].value_counts(dropna=False))
#  删除1列NAN数据
print(df[df['Type'].isnull()])
df.drop(index=9148, inplace=True)

# 删除app重复行
df.drop_duplicates('App', inplace=True)

# 数据分析
# 按照类别分组，看每个类别下有多少种APP，可以看出开发者更倾向于开发哪种APP
print(df.groupby('Category').count().sort_values('App', ascending=False))
# 计算每个类别的安装次数均值：可看出社交通信及娱乐类最被用户需要
print(df.groupby('Category').mean().sort_values('Installs', ascending=False))
# 计算类别下的评论数据:可看出社交通信及游戏类评论最多
print(df.groupby('Category').mean().sort_values('Reviews', ascending=False))
# 计算类别下的评分数据,平均值计算的各类别评分差值不大，还需要其他方式分析
print(df.groupby('Category').mean().sort_values('Rating', ascending=False))
# 付费和免费数量对比,大部分app为免费
print(df.groupby('Type').count())

# 付费和免费的安装次数统计
print(df.groupby('Type').sum().sort_values('Installs', ascending=False))
# 依据付费及类别分组，观察评论数
print(df.groupby(['Type', 'Category']).mean().sort_values('Reviews', ascending=False))
# 看评论安装数比率，付费的更高
df = df.groupby(['Type', 'Category']).mean()
print((df['Reviews']/df['Installs']).sort_values(ascending=False))
# 相关性，可看出安装数和评论数相关
print(df.corr())

