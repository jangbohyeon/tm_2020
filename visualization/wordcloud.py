from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import stylecloud
import numpy as np
from PIL import Image

word_count = dtm_20200801.sum()
word_dict = dict(word_count)

mask = np.array(Image.open('image.jpg'))

wc = WordCloud(mask=mask, max_font_size=100,\
 max_words=40, background_color="white",\
 font_path='../visualization/NanumBarunGothic.ttf')
plt.imshow(wc.generate_from_frequencies(word_dict), interpolation="bilinear")
plt.axis("off")
