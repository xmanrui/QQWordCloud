# -*- coding: utf-8 -*-

import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import jieba

log_path = './CC++ Loft.txt'
font = './font/SourceHanSerifSC-Regular.otf'
stop_words_path = './stop_words.txt'
add_words_path = './add_words.txt'


def set_show_chinese():
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


def convert_name(name):
    if name == '基哥' or name == '斯基':
        converted_name = '司机'
    elif name == '光光':
        converted_name = '逆光'
    elif name == '大吊':
        converted_name = '大屌'
    elif name == 'D老师':
        converted_name = 'D神'
    elif name == '风' or name == '风比' or name == '风b' or name == '风B':
        converted_name = '风逼'
    elif name == '浩子':
        converted_name = '浩总'
    else:
        converted_name = name

    return converted_name


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def stop_words_list(file_path):
    stopwords = [line.strip() for line in open(file_path, 'r', encoding='utf-8').readlines() if line.strip()]
    return set(stopwords)


def main():
    stopwords = stop_words_list(stop_words_path)

    with open(log_path, 'r', encoding='utf8') as fh:
        all_text = fh.read()
        pattern = '(2017-01-01[\\s\\S]+)'  # 为了提高运行效率，只分析2017-01-01以后的信息
        p = re.compile(pattern, re.M)
        r = p.findall(all_text)
        valid_text = r[0]

    pattern = '(\\d{4}-\\d{2}-\\d{2} \\d{1,2}:\\d{2}:\\d{2})[ |\\t]+【\\S+】\\S+\\n(\\S+)\\n'
    p = re.compile(pattern, re.M)
    r = p.findall(valid_text)

    messages = ''
    for i in r:
        if i[1] != '[图片]':
            messages += i[1]

    print(messages)
    jieba.load_userdict(add_words_path)
    seg = jieba.cut(messages, cut_all=False, HMM=True)
    seg = [s.title() for s in seg]
    seg = [i for i in seg if i not in stopwords]
    seg = [convert_name(i) for i in seg]
    set_show_chinese()
    text = ' '.join(seg)

    wc = WordCloud(collocations=False, font_path=font, width=1800, height=1800, margin=2, max_words=1000).generate(text)
    plt.imshow(wc)
    plt.title('C/C++ Loft聊天词云图', fontsize=20)
    plt.axis("off")
    plt.show()
    wc.to_file('./wordcloud.png')

if __name__ == '__main__':
    main()
