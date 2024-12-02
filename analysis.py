import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import jieba
from wordcloud import WordCloud
from collections import Counter
import re


# 读取 CSV 文件并转换为 DataFrame
df = pd.read_csv('comments.csv')
print(len(df))
#df = df.head(10)
# 将评论列合并为一个字符串，并进行中文分词
comments = df['comment'].str.cat(sep=' ')
comments = comments.replace('\n',' ')
comments = re.sub(r'[^\u4e00-\u9fa5a-zA-Z\s]', '', comments)
print(len(comments))
word_list = list(jieba.cut(comments))
word_list = [word for word in word_list if len(word)>1]
#words = " ".join(word_list)
#print(word_list)
#print(words)
# 统计词频
word_freq = Counter(word_list)
if ' ' in word_freq:
    del word_freq[' ']


# 生成词云
wordcloud = WordCloud(font_path=r'C:\Windows\Fonts\STHUPO.ttf', background_color="white", scale=20).generate_from_frequencies(word_freq)

# 绘制词云图
plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

# 输出词频前十的单词
top_50_words = word_freq.most_common(50)
for word, freq in top_50_words:
    print(word, freq)



# 打印 DataFrame 的前几行
#print(df.head(20))

# 使用 groupby() 和 count() 统计每个成员发了多少评论，并按评论数量从高到低排序

'''
comment_counts = df.groupby('member')['comment'].count().sort_values(ascending=False)
print(comment_counts.head(20))
data = comment_counts.values
data_array = np.array(data)

# 计算均值和方差
mean_value = np.mean(data_array)
variance_value = np.var(data_array)
median_value = np.median(data_array)

# 输出中位数
print("中位数：", median_value)
# 输出均值和方差
print("均值：", mean_value)
print("方差：", variance_value)

count_greater_than_10 = len([x for x in data if x > 20])
# 打印结果
print("大于20的元素个数：", count_greater_than_10)
print("总元素个数：", len(data))
'''
'''
filtered_data = [x for x in data if x > 50]

# 绘制直方图
plt.hist(filtered_data, bins=20, edgecolor='black')  # 设置 bins 参数为 20，可根据需要调整
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram Analysis (Values > 50)')
plt.show()
'''

