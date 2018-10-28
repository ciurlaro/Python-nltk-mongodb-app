from collections import Counter, defaultdict
from os import listdir
from os.path import isfile, join
import pprint
import os
import resources_utils

path = "Dataset\\Risorse-lessicali"
new_path = "Dataset Modificato\\Risorse-lessicali"


def make_resource_map(word_map):
    sub_dirs = [dI for dI in listdir(new_path) if os.path.isdir(os.path.join(new_path, dI))]
    for subdir_name in sub_dirs:
        files = [f for f in listdir(new_path + "\\" + subdir_name) if isfile(join(new_path + "\\" + subdir_name, f))]
        for file_name in files:
            count_word_occurrences(word_map, subdir_name, file_name)
    return word_map


def count_word_occurrences(word_map, subdir_name, file_name):
    with open(new_path + "\\" + subdir_name + "\\" + file_name, 'r',
              encoding="utf-8") as file:
        if subdir_name != "ConScore":
            handle_resource_file(word_map, file, file_name)


def handle_resource_file(word_map, file, file_name):
    words = [word for line in file for word in line.split()]
    for word, count in Counter(words).most_common():
        if word in word_map:
            if file_name in word_map[word]:
                word_map[word][file_name] += count
            else:
                word_map[word][file_name] = {}
                word_map[word][file_name] = count
        else:
            word_map[word] = {}
            word_map[word][file_name] = count


def make_score_map():
    score_map = defaultdict(lambda: defaultdict)

    sub_dirs = [dI for dI in listdir(path) if os.path.isdir(os.path.join(path, dI))]
    for subdir_name in sub_dirs:
        files = [f for f in listdir(path + "\\" + subdir_name) if
                 subdir_name == "ConScore" and isfile(join(path + "\\" + subdir_name, f))]
        for file_name in files:
            file_score_map = handle_score(file_name)
            score_map[file_name] = file_score_map
    return score_map


def handle_score(file_name):
    with open(path + "\\ConScore\\" + file_name, 'r', encoding="utf-8") as read_file:
        with open(new_path + "\\ConScore\\" + file_name[:-4] + ".txt", 'w+', encoding="utf-8") as write_file:
            file_score_map = defaultdict()

            for line in read_file:
                split_line = line.split()
                file_score_map[split_line[0]] = float(split_line[1])

            pprint.pprint(file_score_map, write_file)

    return file_score_map


def make_tweets_sentiment_map(tweets_sentiment_map):
    path = "Dataset Modificato\\Tweets"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in files:
        with open(path + "\\" + file, 'r', encoding="utf-8") as INPUT:
            words = [word for line in INPUT for word in line.split()]
            tweets_sentiment_map[INPUT.name][len(words)] = word_occurrences(words)
    return tweets_sentiment_map


def word_occurrences(words):
    tweets_map = defaultdict(int)
    for word in words:
        tweets_map[word] += 1
    return tweets_map


def percentage_resources_occurrences(word_map, tweets_sentiment_map):
    resource_percentage_map = defaultdict(lambda: defaultdict(float))

    for resource_word in word_map:
        for sentiment_file, total_words_number in tweets_sentiment_map.items():
            for total_words_number in tweets_sentiment_map[sentiment_file].keys():
                num = tweets_sentiment_map[sentiment_file][total_words_number][resource_word]
                if num != 0:
                    resource_percentage_map[resource_word][sentiment_file] = float(num)  # resource_percentage

    return resource_percentage_map


def percentage_tweets_occurrences(tweets_sentiment_map):
    tweets_percentage_map = defaultdict(lambda: defaultdict(float))

    for sentiment_file in tweets_sentiment_map.keys():
        for total_words_number in tweets_sentiment_map[sentiment_file]:
            for word in tweets_sentiment_map[sentiment_file][total_words_number]:
                num = tweets_sentiment_map[sentiment_file][total_words_number][word]
                if num != 0:
                    tweets_percentage_map[word][sentiment_file] = float(num)  # tweets_percentage
    return tweets_percentage_map


def print_maps_on_file(resource_map, resource_percentage_map, tweets_percentage_map):
    with open("Dataset Modificato\\resource_map.txt", 'w+', encoding="utf-8") as rm:
        pprint.pprint(resource_map, rm)

    with open("Dataset Modificato\\resource_percentage_map.txt", 'w+', encoding="utf-8") as rpm:
        pprint.pprint(resource_percentage_map, rpm)

    with open("Dataset Modificato\\tweets_percentage_map.txt", 'w+', encoding="utf-8") as tpm:
        pprint.pprint(tweets_percentage_map, tpm)


def print_hashtag_map():
    path = "Dataset Modificato\\Tweets"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in files:
        if not (file.startswith("emoji") and file.startswith("hashtag")):
            with open(path + "\\" + file, 'r', encoding="utf-8") as INPUT:
                hashtag_map = resources_utils.count_hashtag(file)
                ordered_hashtag_map = sorted(hashtag_map.items(), key=lambda x: x[1])
            with open(path + "\\Hashtag\\hashtag_in_" + file, 'w+', encoding="utf-8") as OUTPUT:
                pprint.pprint(ordered_hashtag_map, OUTPUT)


def print_emoji_map():
    path = "Dataset Modificato\\Tweets"
    files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in files:
        emoji_map = resources_utils.count_emoji(file)
        ordered_emoji_map = sorted(emoji_map.items(), key=lambda x: x[1])
        with open(path + "\\Emoji\\emoji_in_" + file, 'w+', encoding="utf-8") as OUTPUT:
            pprint.pprint(ordered_emoji_map, OUTPUT)

