# Source: https://towardsdatascience.com/create-word-cloud-into-any-shape-you-want-using-python-d0b88834bc32
# 'https://science.nasa.gov/science-news/citizenscience/citizen-scientist-leads-discovery-of-34-ultracool-brown%3Ddwarfs-with-companions'

import matplotlib.pyplot as plt
import numpy as np

from newspaper import Article
from wordcloud import WordCloud
from wordcloud import STOPWORDS
from wordcloud import ImageColorGenerator
from PIL import Image

link_to_file = str(input("Input a link to a document: "))
article = Article(link_to_file)
article.download()
article.parse()

# background_color = Color of background
# max_words = The maximum number of unique words used
# stopwords = stopword list (most commonly used list of words in English)
# max_font_size = Maximum font size
# random_state = To ensure that random numbers are generated in the
# same order, so the results will be the same even if generated several times
# width = width size of the output
# height = height size of the output

mask = np.array(Image.open("data/rocket.jpg"))
mask_colors = ImageColorGenerator(mask)
wc = WordCloud(background_color="white", max_words=2000, 
        stopwords=STOPWORDS, max_font_size=256, 
        random_state=42,
        mask=mask, width=mask.shape[1], height=mask.shape[0],
        color_func=mask_colors) #width=500, height=500

wc.generate(article.text)
plt.imshow(wc, interpolation="bilinear")
plt.axis('off')
plt.show()