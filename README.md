# Data Engineering Pipeline Documentation: Efficient Data Scraping using Parsing JSON API with Python in Airflow

## Overview
In this project, broadly speaking, I retrieve data from an external source, namely the [Dapodik Website](https://dapo.kemdikbud.go.id/), and then store it in BigQuery.

## Pipeline
As for the project pipeline, it can be illustrated as shown below.
<img width="1023" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/cfd05b32-6144-4e0f-a0c6-c954dd48ec6f">
<p>So, this project is limited to the "Data Sources" and "Infrastructure System" aspects because the "End System" is the responsibility of the data analyst. Currently, I am working as a data engineer. The only data source used in this project is the [Dapodik Website](https://dapo.kemdikbud.go.id/). However, in a very large project, there could be a wide variety of data sources used. Data is extracted using the Python programming language exclusively, and the method employed is parsing JSON APIs. After extraction, the data is transformed to ensure its validity and then transferred to BigQuery.</p>

## Requirements
  - Tools: Python, Airflow, Docker, and GCP Account
  - Method: Parse JSON API

## Constraint:
The data is only extracted from Kab. Merauke (Southern Papua).

## Data Model
### Source (Raw Data)
The data includes all schools in all districts within Merauke Regency.
<p>Url link: https://dapo.kemdikbud.go.id/sp/2/370100</p>
<img width="1160" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/d33e5dda-7dfd-43ff-9c14-7cf81afcdf69">
<img width="1160" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/5eadbd33-5cd9-4e86-b8bb-648d3cd64337">

### Result
<img width="1000" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/02dca743-4f6d-47d3-b86a-792abb1206b7">


## DAG Pipeline Explanation (Airflow)
Only one DAG is used in this project, which is named "bq_data_sekolah."
<p><img width="299" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/5292db76-c52d-4147-b351-fc8ebbd05e37">
</p>
<p>The script runs every hour using a batch system. However, due to the small amount of data, this project utilizes a "replace" system for the target table.</p>
<p><img width="445" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/86ef4abb-3171-41f5-8c45-91fa9bbc007c"></p>

### Tasks
The DAG used in this project consists of three tasks: "start," "data_processing_task," and "end."
<p><img width="307" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/3789e7dd-dc30-4e6c-bdf2-5f581ac1218f"></p>

The illustration of the tasks in the DAG is as follows:
<p><img width="950" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/c32f9c8f-1765-470d-acfe-9b9a2317fb92"></p>

### data_processing_task
#### Extract
Data extraction is performed with two nested loops. The first loop iterates through the district names in Merauke Regency, and the second loop iterates through all the schools in each district, as shown below:
<img width="688" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/fb66a6b6-8190-41f7-8d63-e599d230331f">

##### First Looping
<img width="834" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/7a182b10-8f44-44c0-8bb8-51a61dff7aa2">
<p>Please take note of the URL "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=2&kode_wilayah=370100". The last 6 digits in the URL represent the district code. Therefore, the looping is performed based on these codes. The data looped for all districts is stored in the subdistrict_codes variable.</p>
<p><img width="163" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/bb25dbc4-a81c-436e-bb9b-3c4ffde4bfca"></p>

##### Second Looping
<img width="820" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/ef544970-5926-4245-9eb5-2699529b36df">
<p>Meanwhile, for the second loop, it involves retrieving data from each school within every district, encompassing "nama","npsn","bentuk_pendidikan","status_sekolah","pd","sinkron_terakhir","induk_provinsi", dan "induk_kabupaten".</p>

##### Storing Data to Virtual Dataframe
<img width="434" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/e8ba50bb-ab41-411b-858e-3e341b2973d5">
<p>The extraction results are then stored in a virtual dataframe. Additionally, column names are modified for better comprehension.</p>

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
<p>Website's Url: https://dapo.kemdikbud.go.id/sp/2/370100</p>
