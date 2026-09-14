Nama : Samuel Haganta Surbakti

NPM : 2506612814

Kelas : PBP D



### TUGAS 2 

1. Jelaskan alur yang terjadi ketika pengguna membuka halaman portofolio baru, mulai dari permintaan yang diterima proyek hingga data ditampilkan pada browser. Dalam jawabanmu, jelaskan peran urls.py proyek, urls.py aplikasi, view, model, dan template.

    a. Client mengakses URL dari browser 

    b. Django akan memetakan URL tersebut lalu mengarahkannya urls.py projek, lalu akan mengarahkannya lagi ke urls.py aplikasi (default / tidak diberikan tambahan suffix)
        - urls.py projek adalah router pertama yang akan mengarahkan path setelah client sudah mengakses URL, sedangkan urls.py aplikasi adalah router yang terbatas hanya dapat mengarahkan path ke path yang dimiliki oleh aplikasi, jadi cakupannya lebih kecil.
        - di projek ini, urls.py akan memberikan admin site jika mempunyai sufix 'admin/' atau akan mengarahkannya ke urls.py aplikasi jika tidak ada tambahan sufix

    c. urls.py projek akan mengarahkan request ke views.py sesuai dengan path yang dipilih, views.py akan memberikan response dengan memberikan template sekaligus context yang di dalamnya memiliki data model yang sudah diambil dari database yang sebelumnya modelnya sudah dibuat di models.py
        - models.py berisikan pemodelan dari suatu data yang ingin kita simpan di database. models.py berisikan atribut dan constrain dari tiap atribut.
        - template adalah sebuah file html biasa yang akan menjadi tampilan dari suatu website kita. Ternyata, kita juga bisa menjalankan kode python di html dengan bantuan django sehingga memudahkan kode yang membutuhkan logika. Kita juga bisa menyatukannya dengan context yang sudah didefinisikan di views.py sehingga kita tidak perlu meng-hardcode template kita
        -views.py adalah sebuah file yang menjadi otak pada django, ia memberikan response dari sebuah request. Response yang diberikan berupa template dengan gabungan context yang bisa berisikan data dari database.

    d. Response berupa template dan context-pun akan diberikan ke browser client untuk dirender


2. Mengapa data untuk bagian portofolio baru sebaiknya disimpan pada model dan tidak ditulis langsung di dalam template? Jelaskan dampaknya terhadap kemudahan pemeliharaan dan pengembangan aplikasi.

    Alasan mengapa data sebaiknya disimpan pada model adalah karena alasan REUSABILITY yang memungkinkan kita menggunakan data yang sama tanpa harus menulis ulang keseluruhan informasi tentang data. Selain itu, dengan menyimpan data dalam bentuk model membuat kode yang lebih terstruktur sehingga projek menjadi lebih modular dan juga scalable.

3. Apa perbedaan fungsi makemigrations dan migrate pada Django? Berikan contoh perubahan model yang mengharuskanmu menjalankan kedua perintah tersebut.

    fungsi makemigrations adalah fungsi yang berguna untuk menyimpan semua perubahan yang terjadi pada model (penambahan model atau perubahan atribut pada model yang sudah ada), sedangkan fungsi migrate berguna untuk membawa perubahan model data ini ke database, sehingga merubah bentuk tabel pada database.
    Contoh perubahan model yang mengharuskan kita menjalankan kedua perintah ini adalah merubah batasan constrain dari sebuah model. 
    contohnya di model saya, saya harus menggunakan kedua fungsi ini saat mengubah title = models.CharField(max_length=255) menjadi title = models.CharField(max_length=300).
    karena makemigration yang akan mencatat perubahan dan migrate yang akan menerapkan perubahan ke database.


### AI disclosure 
Saya menggunakan AI khususnya model Gemini 3.1 Pro untuk membantu saya dalam mengerjakan tugas kedua ini. Saya menggunakan AI untuk membantu saya dalam mengatasi error dan menggenerate sebagian dari kode html.

