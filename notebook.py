# -*- coding: utf-8 -*-
"""notebook.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QghaQZoUz-fjuQGPvSpwjsYhPcZWciGH

<h3> Sri Kresna Maha Dewa

<h1> Import Library </h1>
Import beberapa library yang akan kita pakai di project kali ini
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

"""Mari donwload terlebih dahulu datasetnya"""

!pip install -q kaggle

from google.colab import files
files.upload()

!rm -r ~/.kaggle
!mkdir ~/.kaggle
!mv ./kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d zygmunt/goodbooks-10k

!unzip /content/goodbooks-10k.zip

"""simpan datasetnya kedalam variabel agar dapat kita akses lebih lanjut kedepannya"""

buku = pd.read_csv('/content/books.csv')
genre = pd.read_csv('/content/book_tags.csv')
tags_genre = pd.read_csv('/content/tags.csv')
user = pd.read_csv('/content/to_read.csv')
rating = pd.read_csv('/content/ratings.csv')

"""<h1>Data Understanding</h1>

mari cek detail dari data yang kit punya
"""

buku.info()

buku.head()

buku.shape

"""CEK jumlah buku dan author yang ada"""

print('Jumlah buku: ', len(buku.book_id.unique()))
print('Jumlah author: ', len(buku.authors.unique()))

genre.info()

genre.head()

genre.shape

"""CEK jumlah genre yang ada di dataset"""

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

"""LIHAT bagaimana seberan rating dari dataset"""

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

"""TOTAL User yang ada di dataset"""

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

"""Bersihkan missing value"""

books = books.dropna()

books.groupby('book_id').sum()

"""gabungkan Data dengan Judul, Penulis, dan Tahun Terbit Buku"""

rate = rating
rate

"""Gabungkan dataset yang terpisah-pisah menjadi satu melalui book_id"""

df = pd.merge(rating, books[['book_id', 'authors', 'title', 'original_publication_year']], on='book_id', how='left')
df

"""Cek kembali missing value nya"""

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

from tensorflow.keras import layers, models, optimizers, regularizers

class RecommenderNet(tf.keras.Model):
    def __init__(self, num_users, num_books, embedding_size, learning_rate=0.001, dropout_rate=0.2, regularization_rate=1e-5, **kwargs):
        super(RecommenderNet, self).__init__(**kwargs)

        self.num_users = num_users
        self.num_books = num_books
        self.embedding_size = embedding_size

        # Embedding layers with regularizers
        self.user_embedding = layers.Embedding(
            num_users,
            embedding_size,
            embeddings_initializer='he_normal',
            embeddings_regularizer=regularizers.l2(regularization_rate)
        )
        self.user_bias = layers.Embedding(num_users, 1)

        self.book_embedding = layers.Embedding(
            num_books,
            embedding_size,
            embeddings_initializer='he_normal',
            embeddings_regularizer=regularizers.l2(regularization_rate)
        )
        self.book_bias = layers.Embedding(num_books, 1)

        # Dropout layers
        self.dropout_user = layers.Dropout(dropout_rate)
        self.dropout_book = layers.Dropout(dropout_rate)

        # Learning rate for optimizer
        self.optimizer = optimizers.Adam(learning_rate=learning_rate)

    def call(self, inputs):
        user_vector = self.user_embedding(inputs[:, 0])
        user_vector = self.dropout_user(user_vector)
        user_bias = self.user_bias(inputs[:, 0])

        book_vector = self.book_embedding(inputs[:, 1])
        book_vector = self.dropout_book(book_vector)
        book_bias = self.book_bias(inputs[:, 1])

        dot_user_book = tf.tensordot(user_vector, book_vector, 2)
        x = dot_user_book + user_bias + book_bias

        return tf.nn.sigmoid(x)

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

book_df = df
data = pd.read_csv('/content/ratings.csv')

# Mengambil sample user
id_pembaca = data.user_id.sample(1).iloc[0]
book_read_by_user = data[data.user_id == id_pembaca]

id_pembaca, book_read_by_user

book_df

# Operator bitwise (~), bisa diketahui di sini https://docs.python.org/3/reference/expressions.html
book_not_read = book_df[~book_df['book_id'].isin(book_read_by_user.book_id.values)]['book_id']
book_not_read = list(
    set(book_not_read)
    .intersection(set(buku_to_buku_encoded.keys()))
)

book_not_read = [[buku_to_buku_encoded.get(x)] for x in book_not_read]
user_encoder = user_to_user_encoded.get(id_pembaca)
user_book_array = np.hstack(
    ([[user_encoder]] * len(book_not_read), book_not_read)
)

user_book_array.shape

rate_buku = model.predict(user_book_array).flatten()

top_ratings_indices = rate_buku.argsort()[-10:][::-1]
recommended_book_ids = [
    buku_encoded_to_buku.get(book_not_read[x][0]) for x in top_ratings_indices
]

recommended_book_ids

top_book_user = (
    book_read_by_user.sort_values(
        by = 'rating',
        ascending=False
    )
    .head(5)
    .book_id.values
)

top_book_user

print('Menampilkan Rekomendasi Buku untuk User ID: {}'.format(id_pembaca))
print('===' * 12)
print('Rekomendasi Buku dengan Rating Tinggi dari Pembaca')
print('----' * 12)

book_df_rows = book_df[book_df['book_id'].isin(top_book_user)]
for row in book_df_rows.itertuples():
    print(row.penulis, ':', row.judul_buku)

print('----' * 12)
print('Top 10 Rekomendasi Buku')
print('----' * 12)

recommended_book = book_df[book_df['book_id'].isin(recommended_book_ids)]
for row in recommended_book.itertuples():
    print(row.authors, ':', row.title)