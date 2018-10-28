# import mongoDB_utils
# import oracleDB_utils
# mysqlDB_utils
import resources_utils
from collections import defaultdict
import map_utils
import cloud_utils

path = "Dataset\\Risorse-lessicali"
new_path = "Dataset Modificato\\Risorse-lessicali"
emotions = ["anger", "anticipation", "disgust", "fear", "joy", "sadness", "surprise", "trust"]


def main():
    print()
    cleaning_resources()
    maps = generating_maps()
    # filling_databases(maps[3], maps[2], maps[0])
    generating_clouds(maps[3])


def cleaning_resources():
    resources_utils.clean_lexical_resources()
    resources_utils.clean_dt_tweets()


def generating_maps():
    resource_map = map_utils.make_resource_map({})
    tweets_sentiment_map = map_utils.make_tweets_sentiment_map(defaultdict(lambda: defaultdict(int)))
    resource_percentage_map = map_utils.percentage_resources_occurrences(resource_map, tweets_sentiment_map)
    tweets_percentage_map = map_utils.percentage_tweets_occurrences(tweets_sentiment_map)

    map_utils.print_hashtag_map()
    map_utils.print_emoji_map()
    map_utils.print_maps_on_file(resource_map, resource_percentage_map, tweets_percentage_map)

    return resource_map, tweets_sentiment_map, resource_percentage_map, tweets_percentage_map


def filling_databases(tweets_percentage_map, resource_percentage_map, resource_map):
    print("filling_databases ...")
    # oracleDB_utils.fill_database(tweets_percentage_map, resource_percentage_map, resource_map)
    # mysqlDB_utils.fill_database(tweets_percentage_map, resource_percentage_map, resource_map)
    # mongoDB_utils.fill_database(tweets_percentage_map, resource_percentage_map, resource_map)


def generating_clouds(tweets_percentage_map, sentiment=None):
    if sentiment in emotions:
        cloud_utils.make_clouds(tweets_percentage_map,
                                'Dataset Modificato\\Tweets\\dataset_dt_' + sentiment + '_60k.txt', 'trust')
    else:
        for i in range(len(emotions)):
            cloud_utils.make_clouds(tweets_percentage_map,
                                    'Dataset Modificato\\Tweets\\dataset_dt_' + emotions[i] + '_60k.txt', emotions[i])

    # cloud_utils.score_clouds()


main()
