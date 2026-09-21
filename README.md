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



### TUGAS 3

1. Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan {% csrf_token %} pada form tersebut!

    Setelah membaca beberapa sumber, alasan utama menggunakan ModelForm ternyata adalah karena aspek DRY (Dont Repeat Yourself). Maksudnya, karena kita sudah mendefinisikan atribut model dan batasan / constrain-nya tiap atributnya, kita tidak perlu lagi menentukan widgetnya. Namun, saya sadar kita tetap harus mendefinisikanya di tugas kali ini, saya berasumsi karena styling widget. Tak hanya ini, ModelForm juga digunakan karena alasan penyimpanan data yang instan ke database dengan menggunakan .save(). penggunaan  {% csrf_token %} diwajibkan karena alasan keamanan, spesifiknya "Cross-Site Request Forgery", yaitu pemalsuan authentication dengan penyalahgunaan cookie di browser. 

2. Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?

    Alasan JSON lebih disukai adalah karena ukuran yang jauh lebih ringkas, parser yang sangat cepat, integrasi yang native dengan JavaScript frontend, dan juga karena sifat bentuk datanya yang berupa objek dan gampang dibaca karena sebenarnya datanya hanyalah pasangan key-value.

3. Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?

    ```
    def get_projects_json(request):
        title_query = request.GET.get("title", "").strip()
        projects = Project.objects.all()

        if title_query:
            projects = projects.filter(title__icontains=title_query)

        projects_json = serializers.serialize("json", projects)
        return HttpResponse(projects_json, content_type="application/json")
    ```

    - request client yang dipetakan ke fungsi get_projects_json ditangkap 
    - data diambil dari database langsung
    - lalu melakukan Serialization (pengubahan format data ke JSON)
    - memberikan respons berupa HttpResponse yang berisi aplikasi yang hanya berisikan data projek dengan format JSON

    Serialization harus dilakukan karena alasan tipe data yang cocok, data yang dikirim dari database bertipe objek QuerySet yang tidak bisa dikirim melalui HttpResponse, tetapi sebaliknya dengan JSON, Httpresponse mendukung data bertipe JSON. Hal lain dan mungkin yang utama addalah karena JSON adalah format data yang universal yang digunakan untuk data delivery melalui internet.


### AI disclosure 
Saya menggunakan AI khususnya model Gemini 3.1 Pro untuk membantu saya dalam mengerjakan tugas kedua ini. Saya menggunakan AI untuk membantu saya dalam mengatasi error dan menggenerate sebagian dari kode html.

