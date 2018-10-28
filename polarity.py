from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from resources_utils import delete_nick_and_url, substitute_slangs
from textblob import TextBlob
import matplotlib.pyplot as plt
import operator

sid = SIA()

path = "Dataset\\Tweets\\"
path_mod = "Dataset Modificato\\"


def count_line():
    non_blank_lines = 0

    with open(path + "dataset_dt_anger_60k.txt", 'r', encoding='utf-8') as inputFile:
        for line in inputFile:
            if line.strip():
                non_blank_lines += 1

    return non_blank_lines


def clean_file():
    i = 0
    with open(path + "dataset_dt_anger_60k.txt", 'r', encoding='utf-8') as inputFile:
        with open(path_mod + "plt_dt_anger.txt", 'w+', encoding='utf-8') as outFile:
            for line in inputFile:
                if line.strip():
                    line = delete_nick_and_url(line)
                    line = line.lower()
                    line = substitute_slangs(line)
                    outFile.write(line)


def textblob_polaryze_tweets():
    list_pol_tweets = {}
    list_pol_tweets['positive'] = 0
    list_pol_tweets['neutral'] = 0
    list_pol_tweets['negative'] = 0
    with open(path_mod + "plt_dt_anger.txt", 'r', encoding='utf-8') as inputFile:
        for line in inputFile:
            analysis = TextBlob(line)
            if analysis.sentiment.polarity > 0:
                list_pol_tweets['positive'] += 1
            elif analysis.sentiment.polarity == 0:
                list_pol_tweets['neutral'] += 1
            else:
                list_pol_tweets['negative'] += 1

    plot_chart("textblol_lib", list_pol_tweets, 0)


def nltk_polaryze_tweets():
    list_pol_tweets = {}
    list_pol_tweets['pos'] = 0
    list_pol_tweets['neu'] = 0
    list_pol_tweets['neg'] = 0
    c = 0
    with open(path_mod + "plt_dt_anger.txt", 'r', encoding='utf-8') as inputFile:
        for line in inputFile:
            analysis = sid.polarity_scores(line)
            mK = max(analysis.items(), key=operator.itemgetter(1))[0]
            if 'compound' not in mK:
                list_pol_tweets[mK] += 1
            else:
                c += 1

    plot_chart("nltk_lib", list_pol_tweets, c)


def plot_chart(libName, list_pol_tweets, n_compound):
    if n_compound == 0:
        nlines = count_line()
    else:
        nlines = n_compound

    labels = []
    percentage = []
    for el in list_pol_tweets:
        labels.append(el)
        p = round(list_pol_tweets[el] * 100 / nlines, 2)
        percentage.append(p)

    colors = ['green', 'yellow', 'red']

    plt.pie(percentage, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.savefig(path_mod + libName + '.png', bbox_inches='tight')


def main():
    clean_file()
    #textblob_polaryze_tweets()
    nltk_polaryze_tweets()


main()

