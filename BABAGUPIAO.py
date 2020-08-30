import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as mpf
import warnings


def get_deal_date(w, is_buy=True):
    if is_buy == True:
        return True if w[0] == False and w[1] == True else False
    else:
        return True if w[0] == True and w[1] == False else False


plt.rcParams["font.family"] = "SimHei"     # 设置可以显示中文字体
plt.rcParams["axes.unicode_minus"] = False
warnings.filterwarnings("ignore")          # 忽略警告信息

data = pd.read_csv("./项目/BABA_stock.csv")    # 加载数据集
# # 数据概览
# print(data.info())
# # 字段的类型统计信息
# print(data.describe())
# # 随机抽样5条数据
# print(data.sample(10))

# 对日期进行转换
data["date"] = pd.to_datetime(data['date'])
# 根据日期进行降序排列
data.set_index("date", drop=False, inplace=True)
# 指定一列为索引
data.sort_index(inplace=True)
# 按照索引进行排序

# 只取出近三年的数据
data = data[data['date'] > "2017-05-01"]
# print(data.head())
# print(data.describe())
# print(data.shape)
# 处理空值
# print(data.isnull().sum())


# ----数据分析
fig = plt.figure(figsize=(24, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_xticks(range(0, len(data.index), 70))
ax.set_xticklabels(data.index[::70])

mpf.candlestick2_ochl(ax, data['open'], data['close'], data['high'], data['low'], width=0.6, colorup='r', colordown='g', alpha=0.75)
# plt.show()
# 涨跌情况的分析
close_info = data["close"]
open_info = data['open']
total_count = data.shape[0]
rise_count = len(data[close_info-open_info > 0])
fail_count = len(data[close_info-open_info < 0])
# print('上涨天数：', rise_count)
# print('下跌天数：', fail_count)
# print('上涨概率：{:.2%}'.format(rise_count/total_count))
# print('下跌概率：{:.2%}'.format(fail_count/total_count))


# 指定交易策略
# 股价超出10日均线买入，跌破十日均线卖出，在卖出前不会进行下一次买入。
# 简单起见，只用收盘价进行分析。
# 计算10日均线
df = data['close']
ma10 = df.rolling(10).mean()
ma10_model = df - ma10 > 10

se_buy = ma10_model.rolling(2).apply(get_deal_date, raw=False).fillna(0).astype('bool')
# print(se_buy)
# apply的args接收数组或者字典给自定义参数传参
se_sale = ma10_model.rolling(2).apply(get_deal_date, raw=False, args=[False]).fillna(0).astype('bool')
# print(se_sale)
# 具体的买卖点情况
buy_info = df[se_buy.values]
sale_info = df[se_sale.values]
# print(buy_info)
# print(buy_info.describe())
# print(sale_info.describe())
# print(ma10_model)
# 盈利情况分析
no_index_buy = buy_info.reset_index(drop=True)
no_index_sale = se_sale.reset_index(drop=True)
# 每次交易情况
profit = no_index_sale-no_index_buy
print(profit.sum())
print(profit.describe())
