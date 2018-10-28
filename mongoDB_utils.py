from collections import defaultdict
import pymongo
import time
import re
import ast
from bson.code import Code

client = pymongo.MongoClient('localhost', 27017)
mydb = client['db_lab']


def fill_database(tweets_percentage_map, resource_percentage_map, resource_map):
    bulk_query = defaultdict(list)
    for data in tweets_percentage_map.keys():
        for sentiment in tweets_percentage_map[data].keys():
            if data in resource_map.keys():
                resource_file_list = []
                resource_sentiment = []
                for resource_file in resource_map[data]:
                    if sentiment[37:-8] in resource_file:
                        resource_file_list.append((resource_file, resource_map[data][resource_file]))
                resource_sentiment.append((sentiment[37:-8], resource_percentage_map[data][sentiment]))
                bulk_query[sentiment[37:-8]].append(insert_frequency(data, resource_file_list, resource_sentiment))
            else:
                elem = insert_word_tweet(data, tweets_percentage_map[data][sentiment])
                if elem is not None:
                    bulk_query[sentiment[37:-8]].append(elem)

    print(manage_insertion(bulk_query))


def insert_frequency(word, resource_file_list, resource_sentiment):
    column = []
    row = []

    for resource_file in resource_file_list:
        column.append(str(resource_file[0])[:-4])
        row.append(resource_file[1])

    for sentiment in resource_sentiment:
        s = ""
        if len(resource_file_list) != 0:
            for elem in resource_file_list:
                s += str(elem)[1:-1].replace(",", ":").replace(".txt", "") + ", "

        query = str("{'word' : '" + str(word) + "', " + s + "'frequency' : '" + str(int(sentiment[1])) + "'}")
        return ast.literal_eval(query)


def insert_word_tweet(data, freq):
    if re.match(r'[\x00-\x7F]+$', data) and len(data) <= 80:
        query = str("{'word': " + '"' + str(data) + '", ' + "'frequency': " + str(int(freq)) + "}")
        return ast.literal_eval(query)


def manage_insertion(bulk_query):
    start = time.time()
    bulk_insertion(bulk_query)
    return time.time() - start


def bulk_insertion(bulk_query):
    for sentiment in bulk_query.keys():
        my_col = mydb[sentiment]
        my_col.insert_many(bulk_query[sentiment])


def map_reduce_from_files():
    with open("map_function.js", 'r') as file:
        map = Code(file.read())

    with open("reduce_function.js", 'r') as file:
        reduce = Code(file.read())

    return map, reduce


def avg_over_maps(map, reduce, word):
    q = {"word": word}
    avg = [0, 0]

    for collection in mydb.collection_names():
        c = mydb.get_collection(collection)
        res = c.map_reduce(map, reduce, "map_reduce_result", query=q)
        for doc in res.find():
            freq = int(doc["value"])
            print(str(word) + ": " + str(collection) + ", " + str(freq))
            avg[0] += freq
            avg[1] += 1

    try:
        return int(avg[0] / avg[1])
    except ZeroDivisionError:
        return 0


def percentage_over_maps(map, reduce, word):
    q = {"word": word}
    tot = 0
    percentage_list = []

    for collection in mydb.collection_names():
        c = mydb.get_collection(collection)
        res = c.map_reduce(map, reduce, "map_reduce_result", query=q)
        for doc in res.find():
            freq = int(doc["value"])
            tot += freq
            percentage_list.append((collection, freq))

    count = 0
    for freq in percentage_list:
        p = round(freq[1]/tot*100, 2)
        count += p
        print(str(word) + ": " + str(freq[0]) + ", " + str(p) + "%")



