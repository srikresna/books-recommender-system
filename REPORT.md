# Laporan Proyek Machine Learning - Sri Kresna Maha Dewa
## Project Overview

Membaca buku adalah cara yang efektif bagi setiap individu untuk memperoleh pengetahuan dan wawasan baru mengenai berbagai topik. Buku berperan sebagai sumber informasi dan pengetahuan yang dapat memperluas pemahaman tentang berbagai aspek kehidupan. Pepatah "Buku adalah jendela dunia" mencerminkan pentingnya membaca. Meskipun informasi mengenai berbagai jenis buku kini mudah diakses melalui internet, minat baca di Indonesia masih rendah, kemungkinan disebabkan oleh banyaknya pilihan buku yang membuat pembaca kesulitan menemukan yang sesuai dengan preferensi mereka.

Sebagai upaya meningkatkan minat baca masyarakat, salah satu solusinya adalah membangun sistem rekomendasi buku. Sistem ini menggunakan metode _Collaborative Filtering_ untuk membantu pembaca menemukan buku sesuai dengan kriteria dan preferensi mereka. Dengan adanya rekomendasi yang akurat, diharapkan pembaca dapat dengan mudah menemukan informasi yang mereka cari atau menemukan buku dengan kriteria serupa, sehingga minat baca masyarakat dapat meningkat.
## Business Understanding

Penelitian ini bertujuan menyusun sistem rekomendasi buku yang secara tepat memenuhi kriteria dan preferensi setiap pembaca. Dengan menerapkan metode _collaborative filtering_, sistem ini dirancang untuk memberikan rekomendasi yang sangat personal dan relevan. Data pembaca, termasuk preferensi, kriteria, dan histori bacaan, akan dianalisis untuk memahami dengan lebih baik pola bacaan dan keinginan pembaca. Dengan memadukan pendekatan _user-based_ dan _item-based_, serta memasukkan elemen _context-aware_, diharapkan sistem ini mampu menghasilkan rekomendasi buku yang tidak hanya sesuai dengan selera pembaca, tetapi juga mempertimbangkan konteks spesifik, seperti waktu dan lokasi.

Melalui pengembangan sistem rekomendasi ini, diharapkan dapat meningkatkan minat baca masyarakat. Dengan memberikan rekomendasi yang akurat dan relevan, diharapkan pembaca akan lebih terlibat dalam eksplorasi literatur, memperluas wawasan mereka, dan pada akhirnya, mendorong peningkatan minat baca di kalangan masyarakat.

### Problem Statements

- Bagaimana fitur yang dapat digunakan untuk membuat sistem rekomendasi?
- Bagaimana membuat sistem rekomendasi buku yang mungkin akan disukai berdasarkan _rating_ menggunakan _collaborative filtering_?

### Goals

- Memberikan sejumlah rekomendasi buku yang belum dibaca atau mungkin akan disukai oleh pembaca dengan menggunakan _collaborative filtering_.
- Membuat sebuah model yang memiliki kehandalan yang cukup agar rekomendasi bisa lebih akurat

### Solution statements
- Implementasi _Collaborative Filtering_: Penerapan metode _collaborative filtering_ akan dilakukan melalui penggunaan kelas `RecommenderNet`. Ini bertujuan membentuk model yang handal dan _robust_, memungkinkan sistem memahami preferensi pembaca dengan lebih baik melalui informasi dari pengguna lain.

- Model Evaluation menggunakan RMSE: Kualitas model yang dibangun akan dievaluasi dengan menggunakan metode _Root Mean Square Error_ (RMSE). Pendekatan ini akan memberikan gambaran yang akurat tentang sejauh mana perbedaan antara prediksi model dengan nilai aktual, mengukur tingkat ketepatan dan kehandalan rekomendasi yang diberikan.

- Fokus pada Kualitas dan Akurasi: Selain pembangunan model yang powerful, penelitian ini menempatkan penekanan pada evaluasi kritis dengan menggunakan RMSE. Hal ini bertujuan untuk memastikan bahwa sistem rekomendasi buku tidak hanya mampu memberikan rekomendasi personal, tetapi juga secara konsisten akurat dan dapat diandalkan dalam memenuhi preferensi pembaca.

## Data Understanding
Dataset yang digunakan diambil dari situs **Kaggle** yang berjudul [_"goodbooks-10k"_](https://www.kaggle.com/datasets/zygmunt/goodbooks-10k?select=books.csv). Dataset ini berisi 5 file dengan ekstensi csv, yaitu:
1. **'book_tags.csv'**, file ini berisi data tag buku (label), diurutkan berdasarkan ascending goodreadsbookid dan count descending.
   - goodreads_id : ID dari goodreads
   - tag_id : ID tag (genre)
   - count : Jumlah goodreads

2. **'books.csv'**, berisi informasi mengenai buku.
   - id : ID dari file books
   - book_id : ID buku
   - best_book_id : ID dari buku populer
   - work_id : ID karya
   - books_count : jumlah edisi buku tertentu
   - isbn : nomor isbn
   - authors : nama penulis
   - original_publication_year : tahun terbit buku
   - original_title : judul asli buku
   
4. **'ratings.csv'**, berisi rating buku sesuai id pengguna.
   - book_id : ID buku
   - user_id : ID Pengguna
   - rating : rating buku

5. **'tag.csv'**, berisi tentang pemetaan id-nama tag.
   - tag_id : ID tag (genre)
   - tag_name : Nama tag (genre)

6. **'to_read.csv'**, daftar buku yang ditandai oleh pengguna "untuk dibaca". Diurutkan berdasarkan user_id dan book_id.
   - user_id : ID pengguna/pembaca
   - book_id : ID buku
   
    Dari data didapatkan Jumlah User = 48871.
      
File yang digunakan untuk pemodelan adalah file 'books.csv' dan 'ratings.csv' dengan menggunakan variabel **'user_id', 'book_id', 'authors', 'original_title'** dengan model _collaborative filtering_.


## Data Preparation
Teknik yang digunakan untuk data preparation antara lain sebagai berikut:
1. **Mengatasi Missing Value**, dilakukan pengecekan data apakah ada data yang kosong dan berapa jumlahnya menggunakan `isnull().sum()`, sehingga didapatkan hasil:
   ```sh
     book_id                             0
     user_id                             0
     rating                              0
     authors                      88860317
     title                        88860317
     original_publication_year    88870317
     dtype: int64
   ```
2. **Encoding Data**, melakukan penyandian (_encoding_) fitur **'user_id'** dan **book_id** ke bentuk indeks integer.
3. **Membagi Dataset**, dataset akan dibagi menjadi data train dan data test dengan rasio 80:20. Namun sebelum itu dilakukan pengacakan dataset agar distribusinya random/acak. Teknik _Encoding_ Data dan Membagi Dataset dilakukan untuk nantinya dipakai pada model _collaborative filtering_.

## Modeling

_Collaborative filtering_ bergantung pada pendapat komunitas pengguna. Ia tidak memerlukan atribut untuk setiap itemnya seperti pada sistem berbasis konten. Model ini memprediksi kegunaan item berdasarkan penilaian pengguna sebelumnya, misalnya cara pemberian _rating_ terhadap suatu item. Metode ini merekomendasikan item-item yang dipilih oleh pengguna lain dengan kemiripan model item dari pengguna saat ini.

Pada tahap ini, model akan menghitung skor kecocokan antara pembaca(_user_) dan buku menggunakan tekenik _embedding_. Langkah yang pertama adalah melakukan proses _embedding_ terhadap data pembaca(_user_) dan buku. Kemudian lakukan perkalian dot antara _embedding_ pembaca dan buku. Tambahkan bias untuk setiap pembaca dan buku. Fungsi sigmoid digunakan untuk menetapkan skor kecocokan dalam skala [0,1]. Langkah-langkah yang disebutkan diatas akan dimasukkan ke dalam sebuah class dari Keras bernama `RecommenderNet()`.

Kelebihan:
- Rekomendasi yang dihasilkan cenderung sangat _personalized_ karena didasarkan pada preferensi pengguna secara individu.
- Tidak perlu informasi rinci tentang setiap item karena mengandalkan pola perilaku pengguna.

Kekurangan:
- Cold-start problem: Algoritma menghadapi kesulitan dalam memberikan rekomendasi untuk pengguna atau item baru yang belum memiliki informasi preferensi terdokumentasi.
- Sparse problem: Keterbatasan dalam keakuratan algoritma dapat muncul ketika terdapat matriks _rating_ pengguna-item yang bersifat _sparse_, yaitu ketika terdapat banyak nilai kosong atau jarang diisi, mempengaruhi kemampuan model untuk memberikan rekomendasi yang tepat.

## Evaluation

Metrik evaluasi yang digunakan pada proyek ini adalah _Root Mean Square Error_.

_**Root Mean Squared Error**_

Metrik RMSE _(Root Mean Square Error)_ digunakan pada penelitian ini untuk mengevaluasi kinerja model yang dihasilkan. RMSE merupakan cara standar untuk mengukur kesalahan model dalam memprediksi data kuantitatif. _Root Mean Squared Error_ (RMSE) mengevaluasi model regresi linear dengan mengukur tingkat akurasi hasil perkiraan suatu model. RMSE dihitung dengan mengkuadratkan error (prediksi – observasi) dibagi dengan jumlah data (= rata-rata), lalu diakarkan. Perhitungan RMSE ditunjukkan pada rumus berikut.

$$RMSE = \sqrt{\Sigma_{i=1}^{n}{\frac{(ŷ_i - y_i)^{2}}{n}}}$$

Keterangan: 

RMSE = nilai _root mean square error_

y = nilai hasil observasi

ŷ = nilai hasil prediksi

i = urutan data

n = jumlah data

Nilai RMSE rendah menunjukkan bahwa variasi nilai yang dihasilkan oleh suatu model prakiraan mendekati variasi nilai obeservasinya. RMSE menghitung seberapa bedanya seperangkat nilai. Semakin kecil nilai RMSE, semakin dekat nilai yang diprediksi dan diamati. 

Visulaisasi evaluasi metrik menggunakan RMSE setelah pelatihan untuk model Collaborative filtering dapat dilihat pada Gambar 2.

![rmse](img.png)
> Gambar 1. Visualisasi Hasil RMSE

 Dari visualisasi diatas didapatkan nilai error akhir sebesar 0.3527 dan validasi error sebesar 0.5760 yang bisa dikatakan sudah bagus untuk sebuah sistem rekomendasi. 

## Kesimpulan
- Model _collaborative filtering_ dievaluasi menggunakan metode _Root Mean Square Error_ (RMSE) untuk mengukur sejauh mana perbedaan antara prediksi model dengan nilai aktual. Nilai RMSE yang dihasilkan sebesar 0.5760 mencerminkan tingkat akurasi model dalam memberikan rekomendasi. Semakin rendah nilai RMSE, semakin baik kinerja model dalam memprediksi preferensi pengguna.

- Dengan nilai RMSE yang relatif rendah, dapat disimpulkan bahwa model _collaborative filtering_ ini memiliki tingkat ketepatan yang baik dalam memprediksi kecocokan antara pembaca (_user_) dan buku. Hal ini menunjukkan bahwa rekomendasi yang dihasilkan oleh model cenderung mendekati preferensi sebenarnya dari pengguna.
Potensial untuk Peningkatan:

- Meskipun nilai RMSE yang diperoleh sudah menggambarkan kualitas model yang baik, terdapat potensi untuk melakukan peningkatan lebih lanjut. Pengoptimalan _parameter_, penambahan fitur, atau eksplorasi model yang lebih kompleks dapat menjadi langkah-langkah selanjutnya untuk meningkatkan kinerja model dan memberikan rekomendasi yang lebih presisi.

- Kesimpulan dari evaluasi ini menekankan pentingnya evaluasi terus-menerus terhadap model rekomendasi. Seiring perubahan preferensi pengguna dan pertumbuhan data, model perlu terus diperbarui dan disesuaikan untuk menjaga tingkat akurasi dan keandalan rekomendasi.

- Sebelum menarik kesimpulan final, perlu juga mempertimbangkan relevansi nilai RMSE dengan konteks aplikasi dan kebutuhan pengguna. Sebuah nilai RMSE yang rendah mungkin tidak selalu menjamin kepuasan pengguna, sehingga pemahaman mendalam terhadap kebutuhan pengguna sangat penting dalam mengevaluasi kualitas rekomendasi.

## Referensi
Alkaff, M., Khatimi, H., & Eriadi, A. (2020). Sistem Rekomendasi Buku pada Perpustakaan Daerah Provinsi Kalimantan Selatan Menggunakan Metode Content-Based Filtering. MATRIK: Jurnal Manajemen, Teknik Informatika Dan Rekayasa Komputer, 20(1), 193-202.

ZAYYAD, M. R. A. (2021). Sistem Rekomendasi Buku Menggunakan Metode Content Based Filtering.

Arfisko, H. H., & Wibowo, A. T. (2022). Sistem Rekomendasi Film Menggunakan Metode Hybrid Collaborative Filtering Dan Content-Based Filtering. eProceedings of Engineering, 9(3).
