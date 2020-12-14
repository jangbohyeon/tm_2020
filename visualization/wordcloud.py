voca_appear_20200801 = dtm_20200801.sum()
voca = voca_appear_20200801.sort_values(ascending=False)

word_count = dtm_20200801.sum()
word_dict = dict(word_count)

from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import stylecloud
import numpy as np
from PIL import Image


mask = np.array(Image.open('image.jpg'))

wc = WordCloud(mask=mask, max_font_size=100,\
 max_words=40, background_color="white",\
 font_path='../data_files/NanumBarunGothic.ttf')
plt.imshow(wc.generate_from_frequencies(word_dict), interpolation="bilinear")
plt.axis("off")
