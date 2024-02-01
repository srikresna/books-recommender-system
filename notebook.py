# -*- coding: utf-8 -*-
"""notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QghaQZoUz-fjuQGPvSpwjsYhPcZWciGH
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from pathlib import Path

import warnings
warnings.filterwarnings('ignore')

!pip install -q kaggle

from google.colab import files
files.upload()

!rm -r ~/.kaggle
!mkdir ~/.kaggle
!mv ./kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d zygmunt/goodbooks-10k

!unzip /content/goodbooks-10k.zip

buku = pd.read_csv('/content/books.csv')
genre = pd.read_csv('/content/book_tags.csv')
tags_genre = pd.read_csv('/content/tags.csv')
user = pd.read_csv('/content/to_read.csv')
rating = pd.read_csv('/content/ratings.csv')

buku.info()

buku.head()

buku.shape

print('Jumlah buku: ', len(buku.book_id.unique()))
print('Jumlah author: ', len(buku.authors.unique()))

genre.info()

genre.head()

genre.shape

print('Jumlah genre buku: ', len(genre.tag_id.unique()))

tags_genre.info()

tags_genre.head()

tags_genre.shape

print('Jumlah jenis genre buku: ', len(tags_genre.tag_name.unique()))

rating.info()

rating.head()

rating.shape

rate = rating.groupby('rating').count()
rate

plt.figure(figsize=(8,4))
plt.title('Total rating')
plt.xlabel('Rating')
plt.ylabel('Jumlah Buku')
plt.bar(rate.index, rate['book_id'])
plt.grid(True)
plt.show()

"""**Dataset users**"""

user.head()

user.info()

user.describe()

print('Jumlah user: ', len(user.user_id.unique()))

"""gabungkan tag id"""

tags = np.concatenate((
    genre.tag_id.unique(),
    tags_genre.tag_id.unique()
))

tags = np.sort(np.unique(tags))

print('Jumlah genre berdasarkan tag_id: ', len(tags))

"""jumlah rating"""

books = pd.merge(rating, buku, on='book_id', how='left')
books

"""melihat missing value / NaN"""

books.isnull().sum()

books = books.dropna()

books.groupby('book_id').sum()

"""gabungkan Data dengan Judul, Penulis, dan Tahun Terbit Buku"""

rate = rating
rate

df = pd.merge(rating, books[['book_id', 'authors', 'title', 'original_publication_year']], on='book_id', how='left')
df

df.isnull().sum()

#menghapus data yang bernilai kosong
df = df.dropna()

#menghapus data yang duplikat
df = df.drop_duplicates('book_id')
df

"""mnegubah user_id menjadi list unique dan melakukan encoding

"""

dr = rating

id_user = dr['user_id'].unique().tolist()
user_to_user_encoded = {x: i for i, x in enumerate(id_user)}
user_encoded_to_user = {i: x for i, x in enumerate(id_user)}

"""mengubah book_id menjadi list unique dan melakukan encoding"""

id_buku = dr['book_id'].unique().tolist()
buku_to_buku_encoded = {x: i for i, x in enumerate(id_buku)}
buku_encoded_to_buku = {i: x for i, x in enumerate(id_buku)}

"""Mendapatkan jumlah readers"""

num_readers = len(user_to_user_encoded)
print(num_readers)

"""Mendapatkan jumlah resto"""

num_books = len(buku_encoded_to_buku)
print(num_books)

"""Mengubah rating menjadi nilai float

"""

dr['rating'] = dr['rating'].values.astype(np.float32)

# Nilai minimum rating
min_rating = min(dr['rating'])

# Nilai maksimal rating
max_rating = max(dr['rating'])

min_rating, max_rating

"""acak"""

dr = dr.sample(frac=1, random_state=42)
dr

"""splitting"""

x = dr[['user_id', 'book_id']].values
y = dr['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values

train_indices = int(0.8 * dr.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)

"""buat model"""

class RecommenderNet(tf.keras.Model):

  # Insialisasi fungsi
  def __init__(self, num_users, num_resto, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_readers = num_readers
    self.num_books = num_books
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding( # layer embedding user
        num_readers,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_readers, 1) # layer embedding user bias
    self.book_embedding = layers.Embedding( # layer embeddings resto
        num_books,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.book_bias = layers.Embedding(num_books, 1) # layer embedding resto bias

  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0]) # memanggil layer embedding 1
    user_bias = self.user_bias(inputs[:, 0]) # memanggil layer embedding 2
    book_vector = self.book_embedding(inputs[:, 1]) # memanggil layer embedding 3
    book_bias = self.book_bias(inputs[:, 1]) # memanggil layer embedding 4

    dot_user_book = tf.tensordot(user_vector, book_vector, 2)

    x = dot_user_book + user_bias + book_bias

    return tf.nn.sigmoid(x) # activation sigmoid

"""compile model"""

model = RecommenderNet(num_readers, num_books, 50)

model.compile(
    loss = tf.keras.losses.BinaryCrossentropy(),
    optimizer = keras.optimizers.Adam(learning_rate=0.001),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

"""training"""

history = model.fit(
    x = x_train,
    y = y_train,
    batch_size = 128,
    epochs = 10,
    validation_data = (x_val, y_val)
)

"""plot kinerja model"""

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()