import os
from os import listdir
from os.path import isfile, join
import nltk
from nltk.stem.porter import *
from nltk.corpus import state_union
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import *
import emot
from tweets_list_utils import pos_emoticons, neg_emoticons, stopwords, others, punctuations, slang_words

import pprint

ps = PorterStemmer()
word_net_lemmatizer = WordNetLemmatizer()
tokenizer = punkt.PunktSentenceTokenizer()
stem_map = defaultdict()
emoticon_map = defaultdict()
sentiment = ""

def clean_lexical_resources():
    path = "Dataset\\Risorse-lessicali"
    new_path = "Dataset Modificato\\Risorse-lessicali"

    sub_dirs = [dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path, dI))]
    for subdir in sub_dirs:
        if not os.path.exists(new_path + "\\" + subdir):
            os.mkdir(new_path + "\\" + subdir)
        files = [f for f in listdir(path + "\\" + subdir) if isfile(join(path + "\\" + subdir, f))]
        for file in files:
            with open(path + "\\" + subdir + "\\" + file, 'r', encoding="utf-8") as INPUT:
                with open(new_path + "\\" + subdir + "\\" + file, 'a+', encoding="utf-8") as new_file:
                    new_file.seek(0)
                    new_file.truncate()
                    for word in INPUT:
                        if not re.search(r"\B([a-zA-Z]+\_+[a-zA-Z])", word, re.IGNORECASE):
                            new_file.write(word)


def clean_dt_tweets():
    path = "Dataset\\"
    new_path = "Dataset Modificato\\"

    sub_dirs = [dI for dI in os.listdir(path) if os.path.isdir(os.path.join(path, dI)) and dI != "Risorse-lessicali"]
    for sub_dir in sub_dirs:
        if not (os.path.exists(new_path + "\\" + sub_dir)):
            os.mkdir(new_path + "\\" + sub_dir)
        files = [f for f in listdir(path + "\\" + sub_dir) if isfile(join(path + "\\" + sub_dir, f))]
        with open(new_path + "emotions.txt", 'w+', encoding="utf-8") as s:
            s.seek(0)
            s.truncate()
            for file in files:
                write_clean_dt(path, new_path, sub_dir, file)
            pprint.pprint(emoticon_map, s)


def write_clean_dt(path, new_path, sub_dir, file):
    with open(path + "\\" + sub_dir + "\\" + file, 'r', encoding="utf-8") as tweets:
        global sentiment
        sentiment = file[10: -7]
        emoticon_map[sentiment] = defaultdict()
        emoticon_map[sentiment]["pos"] = 0
        emoticon_map[sentiment]["neg"] = 0

        with open(new_path + "\\" + sub_dir + "\\" + file, 'a+', encoding="utf-8") as new_tweets_file:
            new_tweets_file.seek(0)
            new_tweets_file.truncate()

            for line in tweets:
                line = clean_line(line)
                new_tweets_file.write(line)


def clean_line(line):
    line = delete_nick_and_url(line)
    line = delete_emoji_and_emoticon(line)
    line = delete_punctuation(line)
    line = delete_digits(line)
    line = line.lower()
    line = substitute_slangs(line)
    # line = nltk.word_tokenize(line)  # toglie anche la punteggiatura
    # line = nltk.pos_tag(line)  # ha senso farlo se poi non uso i tag?
    # line = stem(line)
    line = word_net_lemmatizer.lemmatize(line)
    line = delete_stopwords(line)
    return line


def delete_nick_and_url(line):
    if "USERNAME" in line:
        line = line.replace("USERNAME", " ")
    if "URL" in line:
        line = line.replace("URL", " ")
    return line


def delete_emoji_and_emoticon(line):
    inline_emoji = emot.emoji(line)
    for data_x in inline_emoji:
        if data_x['value'] in line:
            line = line.replace(data_x['value'], ' ')
    for data_pe in pos_emoticons:
        if data_pe in line:
            line = line.replace(data_pe, ' ')
            emoticon_map[sentiment]["pos"] += 1
    for data_ne in neg_emoticons:
        if data_ne in line:
            line = line.replace(data_ne, ' ')
            emoticon_map[sentiment]["neg"] += 1
    for data_o in others:
        if data_o in line:
            line = line.replace(data_o, ' ')
    return line


def delete_punctuation(line):
    for punctuation_mark in punctuations:
        if punctuation_mark in line:
            line = line.replace(punctuation_mark, "")
    return line


def delete_digits(line):
    return ''.join(" " if c.isdigit() else c for c in line)


def substitute_slangs(line):
    for slang in slang_words:
        slang = " " + slang + " "
        standard = " " + slang_words[slang.replace(" ", "")] + " "

        if line.startswith(slang[1::]):
            line = line.replace(slang[1::], standard) + line[len(slang[1::])::]
        if slang in line:
            line = line.replace(slang, standard)
        if line.endswith(slang[::-1]):
            line = line[:-len(slang[1::])] + line.replace(slang[::-1], standard)
    return line


def stem(line):
    new_line = ""
    for elem in line:
        stemmed = ps.stem(elem[0])
        stem_map[stemmed] = elem[1]
        new_line += stemmed + " "
    return new_line


def delete_stopwords(line):
    for stop_word in stopwords:
        stop_word = " " + stop_word + " "

        if line.startswith(stop_word[1::]):
            line = line[len(stop_word[1::])::]
        if stop_word in line:
            line = line.replace(stop_word, " ")
        if line.endswith(stop_word[1:-1]):
            line = line[:-len(stop_word[::])]
    return line


def count_hashtag(file_name):
    hashtag_map = defaultdict(int)
    path = 'Dataset Modificato\\Tweets\\'
    with open(path + file_name, 'r', encoding="utf-8") as file_to_read:
        for line in file_to_read:
            for words in line.split():
                if words.startswith('#') and words != '#':
                    hashtag_map[words] += 1
    return hashtag_map


def count_emoji(file_name):
    emoji_map = defaultdict(float)
    path = 'Dataset\\Tweets\\'
    if file_name.startswith("dataset"):
        with open(path + file_name, 'r', encoding="utf-8") as file_to_read:
            for line in file_to_read:
                for emoji in emot.emoji(line):
                    emoji_map[emoji['value']] += 1
    return emoji_map
