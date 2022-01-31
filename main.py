import jieba
import process
import matplotlib.pyplot as plt
from wordcloud import WordCloud

if __name__ == '__main__':
    test = process.DataProcess('dataset/dataset2019.json')
    dataset = test.fetch_data()
    data = dataset['content']
    seg_set = []
    for each in data:
        seg = jieba.cut(each)
        for word in list(seg):
            if len(word) < 2:
                continue
            else:
                seg_set.append(word)

    # print(seg_set)
    final = ' '.join(seg_set)
    wc = WordCloud()
    wc.generate(final)
    print(wc.words_)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
