# Dokumentasi Pipeline DE

## Overview
Dalam proyek ini, secara garis besar saya mengambil data dari eksternal source yakni [Dapodik Website](https://dapo.kemdikbud.go.id/) lalu menyimpannya ke BigQuery.

## Pipeline
Adapun pipeline proyek ini dapat terlihat seperti ilustrasi di bawah ini.
<img width="949" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/525e5960-e881-4229-a468-e109eb82ff90">
Jadi, proyek ini terbatas hanya pada bagian "Data Sources" dan "Infrastructure System" saja karena bagian "End System" merupakan jobdesk yang dilakukan oleh data analyst. Sedangkan saat ini yang saya lakukan adalah sebagai data engineer.
Data sources yang digunakan pada proyek ini hanya satu saja yakni [Dapodik Website](https://dapo.kemdikbud.go.id/), namun dalam suatu proyek yang sangat besar bisa jadi data sources yang digunakan sangat banyak dan beraneka ragam. Data diekstrack menggunakan bahasa pemrograman Python 100% dan metode yang digunakan adalah Parse JSON API. Kemudian setelah dilakuan extract, data ditransformasi agar lebih valid lalu ditansfer ke BigQuery.

## Requirements
Python, Airflow, Docker, GCP Account
