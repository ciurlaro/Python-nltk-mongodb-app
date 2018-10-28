from collections import defaultdict
import time
import re
import mysql.connector

config = {
        'host': 'localhost',
        'port': 3306,
        'database': 'db_lab',
        'user': 'root',
        'password': 'welcome',
        'charset': 'utf8',
        'use_unicode': True,
        'get_warnings': True,
    }

db = mysql.connector.Connect(**config)


def fill_database(tweets_percentage_map, resource_percentage_map, resource_map):
    queries = []
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
                queries.append(insert_frequency(data, resource_file_list, resource_sentiment))
            else:
                elem = insert_word_tweet(data, tweets_percentage_map[data][sentiment])
                if elem is not None:
                    bulk_query[sentiment[37:-8]].append(elem)

    print(manage_insertion(bulk_query, queries))


def insert_frequency(word, resource_file_list, resource_sentiment):
    column = []
    raw = []
    fields = ", "
    values = ", "

    for resource_file in resource_file_list:
        column.append(str(resource_file[0])[:-4])
        raw.append(resource_file[1])

    for sentiment in resource_sentiment:
        if len(resource_file_list) != 0:
            fields = ", " + str(column).replace("'", "")[1:-1] + ", "
            values = ", " + str(raw).replace("'", "")[1:-1] + ", "

        query = "insert into db_lab." + str(sentiment[0]).upper() + "_SENTIMENT (word" + str(fields).upper() \
                + "frequency) VALUES ('" + str(word) + "'" + values + str(int(sentiment[1])) + ")"
        return query


def insert_word_tweet(data, freq):
    if re.match(r'[\x00-\x7F]+$', data) and len(data) <= 80:
        return str(data), str(int(freq))


def bulk_insertion(bulk_query):
    cur = db.cursor()
    for key in bulk_query.keys():
        statement = "INSERT INTO db_lab." + key + "_SENTIMENT(word, frequency) VALUES (%s, %s)"
        cur.executemany(statement, bulk_query[key])
        db.commit()
    cur.close()


def manage_insertion(bulk_query, queries):
    start = time.time()
    bulk_insertion(bulk_query)

    for query in queries:
        try:
            cursor = db.cursor()
            cursor.execute(query)
            cursor.close()
        except Exception:
            import sys
            ex = sys.exc_info()[0]

    db.commit()
    return time.time() - start


