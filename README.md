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
Dilakukan extract data dengan 2x looping, yakni looping pada Nama Kecamatan di Kabupaten Merauke dan looping pada semua sekolah di masing-masing kecamatan,

