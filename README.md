# Dokumentasi Pipeline DE

## Overview
In this project, broadly speaking, I retrieve data from an external source, namely the [Dapodik Website](https://dapo.kemdikbud.go.id/), and then store it in BigQuery.

## Pipeline
As for the project pipeline, it can be illustrated as shown below.
<img width="949" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/525e5960-e881-4229-a468-e109eb82ff90">
So, this project is limited to the "Data Sources" and "Infrastructure System" aspects because the "End System" is the responsibility of the data analyst. Currently, I am working as a data engineer. The only data source used in this project is the [Dapodik Website](https://dapo.kemdikbud.go.id/). However, in a very large project, there could be a wide variety of data sources used. Data is extracted using the Python programming language exclusively, and the method employed is parsing JSON APIs. After extraction, the data is transformed to ensure its validity and then transferred to BigQuery.

## Requirements
  - Tools: Python, Airflow, Docker, and GCP Account
  - Method: Parse JSON API

## Constraint:
The data is only extracted from Kab. Merauke (Southern Papua).

## Data Model
### Source (Raw Data)
The data includes all schools in all districts within Merauke Regency.
<img width="1172" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/e0f23100-b354-4fe0-b023-c67aada0dbc0">
<img width="1172" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/84e5b06d-d761-40ce-8437-4f78fa7c56a6">

### Result
<img width="991" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/0e430d81-5518-4d58-984f-92bfb51aca8e">

## DAG Pipeline Explanation (Airflow)
Only one DAG is used in this project, which is named "bq_data_sekolah."
<p><img width="297" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/6a7aef3a-acf0-4ce6-9dd7-5232fd38a720"></p>
<p>The script runs every hour using a batch system. However, due to the small amount of data, this project utilizes a "replace" system for the target table.</p>
<p><img width="447" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/ae19ff6e-2f17-4e15-8994-32750593488e">
</p>

### Tasks
The DAG used in this project consists of three tasks: "start," "data_processing_task," and "end."
<p></p><img width="389" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/707c4658-e5e4-4952-bd6a-5b156aac88dc"></p>

The illustration of the tasks in the DAG is as follows:
<img width="861" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/4556ce4f-f0c0-40d7-9ce1-f74026cff7fc">

### data_processing_task
#### Extract
Data extraction is performed with two nested loops. The first loop iterates through the district names in Merauke Regency, and the second loop iterates through all the schools in each district, as shown below:
<img width="688" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/fb66a6b6-8190-41f7-8d63-e599d230331f">

##### First Looping
<img width="727" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/d7ea2266-58e7-421f-81c4-58a5a2c19732">
<p>Please take note of the URL "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=2&kode_wilayah=370100". The last 6 digits in the URL represent the district code. Therefore, the looping is performed based on these codes. The data looped for all districts is stored in the subdistrict_codes variable.</p>
<p><img width="163" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/704c2091-6742-4278-a040-e9be334b5ec2"></p>

##### Second Looping
<img width="820" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/ef544970-5926-4245-9eb5-2699529b36df">
<p>Meanwhile, for the second loop, it involves retrieving data from each school within every district, encompassing "nama","npsn","bentuk_pendidikan","status_sekolah","pd","sinkron_terakhir","induk_provinsi", dan "induk_kabupaten".</p>

##### Storing Data to Virtual Dataframe
<img width="434" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/e8ba50bb-ab41-411b-858e-3e341b2973d5">
The extraction results are then stored in a virtual dataframe. Additionally, column names are modified for better comprehension.

#### Transfrom
The transformation process in this project involves data validation, which checks whether the data is ready for use by the Data Analyst or not.
<p><img width="993" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/0f047be0-1599-4cab-af30-9e673f2c972c"></p>

##### Check Null Values and Column Types
<img width="353" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/5f0926bf-1443-4940-a053-2a9dec8d8539">
<p>In the case of null values, it turns out that in the "Last_Sync" column, there are empty data fields. After checking the original website, it appears that some data in the "Last_Sync" column contains a "-". Additionally, the data type in the "Last_Sync" column is currently a string, whereas the desired type is a date. Meanwhile, the other columns are considered correct.</p>

##### Transformation Process
  - For null values, they are changed to 'Last Sync is Null'.
  - For strings in the "Last_Sync" column, they are converted to datetime according to the BigQuery format.
<p><img width="609" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/15770c17-cf66-4d91-82d5-84d86253d0bb"></p>

##### Recheck Null Values and Column Types
<img width="363" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/3e1f94f4-43aa-4863-9812-7d04d3785371">
<p>At this stage, null values have been addressed, but the data type of the "Last_Sync" column remains as a string because there are values such as "Last Sync is Null," which serve as indicators that the previous value was null. Below is an example of validated data, and it is evident that the format of the "Last_Sync" column now aligns with the BigQuery format.</p>
<p>Format "Last_Sync" sebelum transformasi</p>
<p><img width="863" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/67c4ad07-9973-4ebb-b5b3-132d94cbbbac"></p>
<p>Format "Last_Sync" setelah transformasi</p>
<p><img width="863" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/ec8dcb66-0430-4f95-971b-9bca11415041"></p>

#### Load
Script:
<p><img width="922" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/ddc8736e-19f3-4502-b9e4-871b54ee904a"></p>
Logic:
<p><img width="912" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/5af2d7ee-c7e1-4712-b3fd-4320ae803bf9">
</p>


# Attachment
Script: https://github.com/arrlanyhars/edtech-airflow/blob/main/dag_pipeline_airflow.py
<p>Website's Url: https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=2&kode_wilayah=370100</p>
