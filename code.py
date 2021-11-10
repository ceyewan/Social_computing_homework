import pandas as pd
from jieba.analyse import *
import jieba
import csv
from wordexpansion import ChineseSoPmi

file = "review.csv"


def separate_csv(file):
    """ 将评论按照正向或者负向分别写入两个文件 """
    a = 1
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if a < 4002:
                a += 1
                continue
            with open("comments_0.csv", "a", encoding="utf-8", newline="") as f2:
                wirter = csv.writer(f2)
                wirter.writerow(row)
            a += 1
    a = 1
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if a == 1:
                a += 1
                continue
            with open("comments_1.csv", "a", encoding="utf-8", newline="") as f2:
                wirter = csv.writer(f2)
                wirter.writerow(row)
            a += 1
            if a > 4001:
                break


def jieba_get_high_frequency_words():
    """ 用jieba分词分别提取出正向和负向的高频词 """
    col_name = [
        'ID',
        'comment'
    ]
    csvpd = pd.read_csv("comments_1.csv", names=col_name)['comment']
    data = ''.join(csvpd)
    with open("high_frequency_word_1.csv", "w", encoding="utf-8", newline="") as f:
        csvwriter = csv.writer(f)
        i = 1
        for keyword, weight in textrank(data, topK=50, withWeight=True):
            csvwriter.writerow([i, keyword])
            i += 1

    csvpd = pd.read_csv("comments_0.csv", names=col_name)['comment']
    data = ''.join(csvpd)
    with open("high_frequency_word_0.csv", "w", encoding="utf-8", newline="") as f:
        csvwriter = csv.writer(f)
        i = 1
        for keyword, weight in textrank(data, topK=50, withWeight=True):
            csvwriter.writerow([i, keyword])
            i += 1


def get_thesaurus(file):
    """ 将所有的评论都写入一个txt文件，用于后面的情感分析 """
    csvpd = pd.read_csv(file)['review']
    data = '\n'.join(csvpd)
    f = open('comments.txt', 'w', encoding='utf-8')
    f.write(data)
    f.close()


def make_seed_words():
    """ 从提取出来的高频词中选取一些种子词，写入txt文件，用去情感分析 """
    with open('seed_words.txt', 'w', encoding='utf-8') as f:
        f.write('好吃' + '\t' + 'pos' + '\n')
        f.write('速度快' + '\t' + 'pos' + '\n')
        f.write('好评' + '\t' + 'pos' + '\n')
        f.write('喜欢' + '\t' + 'pos' + '\n')
        f.write('实惠' + '\t' + 'pos' + '\n')
        f.write('回购' + '\t' + 'pos' + '\n')
        f.write('准时' + '\t' + 'pos' + '\n')
        f.write('满意' + '\t' + 'pos' + '\n')
        f.write('没有' + '\t' + 'neg' + '\n')
        f.write('不会' + '\t' + 'neg' + '\n')
        f.write('取消' + '\t' + 'neg' + '\n')
        f.write('垃圾' + '\t' + 'neg' + '\n')
        f.write('送错' + '\t' + 'neg' + '\n')
        f.write('客服' + '\t' + 'neg' + '\n')

# 利用现成的库进行情感分析
sopmier = ChineseSoPmi(inputtext_file='comments.txt',
                       seedword_txtfile='seed_words.txt',
                       pos_candi_txt_file='pos_candi.txt',
                       neg_candi_txtfile='neg_candi.txt')


if __name__ == '__main__':
    separate_csv(file)
    jieba_get_high_frequency_words()
    get_thesaurus(file)
    make_seed_words()
    sopmier.sopmi()
