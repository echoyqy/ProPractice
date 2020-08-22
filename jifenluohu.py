# utf-8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

luohu_data = pd.read_csv('./项目/bj_luohu.csv', index_col='id')
luohu_data.describe()
# 按照company分组并计算每组的个数
# 对公司人数进行排序
company_data = luohu_data.groupby("company", as_index=False).count()[['company', 'name']]
company_data.rename(columns={'name': 'people_count'}, inplace=True)
company_sort_data = company_data.sort_values('people_count', ascending=False)
# 取出人数为1的公司
company_one_people = company_sort_data[company_sort_data['people_count'] == 1]
print('company_one_people has:', company_one_people['company'])
# 取出人数前大于等于50的公司
company_more_people = company_sort_data[company_sort_data['people_count'] >= 50]
print('company_more_people has:', company_more_people)
# 取出人数前50的公司
print('company_more_people has:', company_sort_data .head(50))

# 落户分数的分布情况
# 根据步长为5进行分数的切割
bins = pd.cut(luohu_data['score'], bins=np.arange(90, 130, 5))
people_score = luohu_data['score'].groupby(bins).count()
print(people_score)
# 处理index
people_score.index = [str(x.left)+'~'+str(x.right) for x in people_score.index]
x = people_score.index
y = people_score
plt.bar(x, y, alpha=1)
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.title('积分分布图')
plt.show()

# 年龄分布
luohu_data['age'] = ((pd.to_datetime('2020-01')-pd.to_datetime(luohu_data['birthday']))/pd.Timedelta('365 days'))
ages = pd.cut(luohu_data['age'], bins=np.arange(40, 45, 1))
people_age = luohu_data['age'].groupby(ages).count()
people_age.index = [str(x.left)+'~'+str(x.right) for x in people_age.index]
x = people_age.index
y = people_age
plt.bar(x, y, alpha=1)
plt.title('年龄分布图')
plt.show()



