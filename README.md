# Dokumentasi Pipeline DE

## Overview
Dalam proyek ini, secara garis besar saya mengambil data dari eksternal source yakni [Dapodik Website](https://dapo.kemdikbud.go.id/) lalu menyimpannya ke BigQuery.

## Pipeline
Adapun pipeline proyek ini dapat terlihat seperti ilustrasi di bawah ini.
<img width="949" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/525e5960-e881-4229-a468-e109eb82ff90">
Jadi, proyek ini terbatas hanya pada bagian "Data Sources" dan "Infrastructure System" saja karena bagian "End System" merupakan jobdesk yang dilakukan oleh data analyst. Sedangkan saat ini yang saya lakukan adalah sebagai data engineer.
Data sources yang digunakan pada proyek ini hanya satu saja yakni [Dapodik Website](https://dapo.kemdikbud.go.id/), namun dalam suatu proyek yang sangat besar bisa jadi data sources yang digunakan sangat banyak dan beraneka ragam. Data diekstrack menggunakan bahasa pemrograman Python 100% dan metode yang digunakan adalah Parse JSON API. Kemudian setelah dilakuan extract, data ditransformasi agar lebih valid lalu ditansfer ke BigQuery.

## Requirements
  - Tools: Python, Airflow, Docker, and GCP Account
  - Method: Parse JSON API

## Batasan:
Data yang diambil hanya pada Kab. Merauke (Papua Selatan) saja.

## Data Model
### Source (Raw Data)
Data: Semua sekolah di semua kecamatan di Kabupaten Merauke.
<img width="1172" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/e0f23100-b354-4fe0-b023-c67aada0dbc0">
<img width="1172" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/84e5b06d-d761-40ce-8437-4f78fa7c56a6">

### Result
<img width="991" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/0e430d81-5518-4d58-984f-92bfb51aca8e">

## DAG Pipeline Explanation (Airflow)
DAG yang digunakan hanya satu saja dalam proyek ini yakni "bq_data_sekolah"
<p><img width="297" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/6a7aef3a-acf0-4ce6-9dd7-5232fd38a720"></p>

### Tasks
Task pada DAG yang digunakan ada tiga, yakni: start, data_processing_task, dan end 
<p></p><img width="389" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/707c4658-e5e4-4952-bd6a-5b156aac88dc"></p>

Adapun ilustrasi task-task pada DAG tersebut seperti gambar di bawah ini:
<img width="861" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/4556ce4f-f0c0-40d7-9ce1-f74026cff7fc">

### data_processing_task
#### Extract
Dilakukan extract data dengan dua kali looping, yakni looping pertama pada Nama Kecamatan di Kabupaten Merauke dan looping kedua pada semua sekolah di masing-masing kecamatan, seperti di bawah ini:
<img width="688" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/fb66a6b6-8190-41f7-8d63-e599d230331f">

##### First Looping
<img width="727" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/d7ea2266-58e7-421f-81c4-58a5a2c19732">
<p>Perhatikan url "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=2&kode_wilayah=370100". 6 digit terakhir pada url merupakan kode kecamatan. Maka dari itu looping yang dilakukan adalah pada kode-kode tersebut. Adapun data yang dilooping untuk semua kecamatan disimpan dalam variabel subdistrict_codes.</p>
<p><img width="163" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/704c2091-6742-4278-a040-e9be334b5ec2"></p>

##### Second Looping
<img width="820" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/ef544970-5926-4245-9eb5-2699529b36df">
<p>Sedangkan untuk looping kedua adalah pengambilan data-data dari masing-masing sekolah pada tiap-tiap kecamatan yang meliputi "nama","npsn","bentuk_pendidikan","status_sekolah","pd","sinkron_terakhir","induk_provinsi", dan "induk_kabupaten".</p>

##### Menyimpan ke Dataframe
<img width="434" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/e8ba50bb-ab41-411b-858e-3e341b2973d5">
Hasil ekstraksi kemudian disimpan ke dalam dataframe virtual. Selain itu dilakukan juga pengubahan nama kolom agar lebih mudah dipahami.

#### Transfrom
Proses transformasi yang dilakukan pada proyek ini adalah melakukan validasi data, yakni apakah data tersebut sudah siap digunakan oleh Data Analyst atau belum.
##### Cek Null Value dan Tipe Kolom
<img width="353" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/5f0926bf-1443-4940-a053-2a9dec8d8539">
<p>Pada null value, ternyata pada kolom "Last_Sync" terdapat data kosong. Setelah dilakukan pengecekan ke Website asli, ternyata ada value berisi "-" pada beberapa data di kolom "Last_Sync". Selain itu, tipe data pada kolom "Last_Sync" adalah string, yang mana tipe yang diinginkan adalah bersifat date. Sedangkan untuk kolom yang lain sudah dinilai aman.</p>

##### Proses Transformasi
  - Untuk null value diubah menjadi 'Last Sync is Null'.
  - Untuk string pada kolom "Last_Sync" diubah ke datetime sesuai format BigQuery.
<p><img width="609" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/15770c17-cf66-4d91-82d5-84d86253d0bb"></p>

##### Cek Ulang Null Value dan Tipe Kolom
<img width="363" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/3e1f94f4-43aa-4863-9812-7d04d3785371">
<p>Pada tahapan ini null value sudah hilang, sedangkan tipe kolom "Last_Sync" masih string karena di dalam kolom tersebut ada value "Last Sync is Null" yang merupakan penanda bahwa value sebelumnya adalah null. Berikut merupakan contoh hasil data yang sudah divalidasi, terlihat format kolom "Last_Sync" sudah sesuai dengan format pada BigQuery.</p>
<p>Format "Last_Sync" sebelum transformasi</p>
<p><img width="863" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/67c4ad07-9973-4ebb-b5b3-132d94cbbbac"></p>
<p>Format "Last_Sync" setelah transformasi</p>
<p><<img width="863" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/ec8dcb66-0430-4f95-971b-9bca11415041"></p>

