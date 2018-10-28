#!/usr/bin/env python
from collections import defaultdict
import sys
import numpy as np
from PIL import Image
from os import path
import matplotlib.pyplot as plt
import map_utils
import string
from wordcloud import WordCloud, ImageColorGenerator
import io


d = path.dirname(__file__)
mask = np.array(Image.open(path.join(d, "brain.jpg")))


def make_clouds(percentage_map, sentiment, *str_to_img):
    cloud_map = defaultdict(float)

    for key in percentage_map.keys():
        percentage = percentage_map[key][sentiment]
        if percentage != 0:
            cloud_map[key] = percentage

    word_cloud = WordCloud(width=1920, height=1080, prefer_horizontal=0.50, background_color='white', max_words=1500,
                           mask=mask, random_state=1).fit_words(cloud_map)

    image_colors = ImageColorGenerator(mask)
    try:
        word_cloud.recolor(color_func=image_colors)
    except ValueError:
        e = sys.exc_info()[0]

    finally:
        # store default colored image
        plt.imshow(word_cloud.to_array())
        plt.axis("off")
        str_to_img = str(str_to_img)
        plt.savefig('a_new_cloud_' + str_to_img + '.png', interpolation="bilinear", bbox_inches='tight', dpi=1000)
        plt.show()


def score_clouds():
    cloud_map = map_utils.make_score_map()

    for key in cloud_map.keys():
        word_cloud = WordCloud(prefer_horizontal=0.50, background_color='white',
                               mask=mask).fit_words(cloud_map[key])
        plt.imshow(word_cloud.to_array())
        plt.axis("off")
        str_to_img = str(key[:-4])
        plt.savefig('a_new_cloud_' + str_to_img + '.png', interpolation="bilinear", bbox_inches='tight')
        plt.show()

