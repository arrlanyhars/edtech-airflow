# Data Engineering Pipeline Documentation: Efficient Data Scraping using Parsing JSON API with Python in Airflow

## Overview
In this project, broadly speaking, I retrieve data from an external source, namely the [Dapodik Website](https://dapo.kemdikbud.go.id/), and then store it in BigQuery.

## Pipeline
As for the project pipeline, it can be illustrated as shown below.
<img width="1023" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/cfd05b32-6144-4e0f-a0c6-c954dd48ec6f">
<p>So, this project is limited to the "Data Sources" and "Infrastructure System" aspects because the "End System" is the responsibility of the data analyst. Currently, I am working as a data engineer. The only data source used in this project is the Dapodik Website. However, in a very large project, there could be a wide variety of data sources used. Data is extracted using the Python programming language exclusively, and the method employed is parsing JSON APIs. After extraction, the data is transformed to ensure its validity and then transferred to BigQuery.</p>

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
#### One of the JSON APIs used displays as follows:
<img width="1565" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/37146a77-4ef4-44da-93ee-7ae64c6f457d">

#### Extract
Data extraction is performed with two nested loops. The first loop iterates through the district names in Merauke Regency, and the second loop iterates through all the schools in each district, as shown below:
<img width="834" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/7a182b10-8f44-44c0-8bb8-51a61dff7aa2">

##### First Loop
<img width="737" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/f24b78d9-a629-4ad8-8b6a-31da33d5f6fc">
<p>Please take note of the URL "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=2&kode_wilayah=370100". The last 6 digits in the URL represent the district code. Therefore, the looping is performed based on these codes. The data looped for all districts is stored in the list_of_subdistrict_codes variable.</p>
<p><img width="226" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/bc463fb7-c1b9-4016-8f92-c20e184ced2f"></p>

##### Second Loop
<img width="763" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/8fdc1d93-6205-4f21-ac9e-152b3efafd19">
<p>Meanwhile, for the second loop, it involves retrieving data from each school within every district, encompassing "nama","npsn","bentuk_pendidikan","status_sekolah","pd","sinkron_terakhir","induk_provinsi", dan "induk_kabupaten".</p>

##### Storing Data to Virtual Dataframe
<img width="428" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/810ec68b-5dea-4178-a618-cad073385dcf">
<p>The extraction results are then stored in a virtual dataframe. Additionally, column names are modified for better comprehension.</p>

#### Transfrom
The transformation process in this project involves data validation, which checks whether the data is ready for use by the Data Analyst or not.
<p><img width="998" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/9ebfb6d7-0499-45a3-8cfd-cd771fffefe3"></p>

##### Check Null Values and Column Types
<img width="363" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/7a977c8a-17df-4520-b83c-790972f784b3">
<p>In the case of null values, it turns out that in the "Last_Sync" column, there are empty data fields. After checking the original website, it appears that some data in the "Last_Sync" column contains a "-". Additionally, the data type in the "Last_Sync" column is currently a string, whereas the desired type is a date. Meanwhile, the other columns are considered correct.</p>

##### Transformation Process
  - For null values, they are changed to 'Last Sync is Null'.
  - For strings in the "Last_Sync" column, they are converted to datetime according to the BigQuery format.
<p><img width="613" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/af38db56-0e80-4566-aa62-8062049e8fe5"></p>

##### Recheck Null Values and Column Types
<img width="358" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/4b1dbe38-6666-47f3-9557-07d5dd1484ae">
<p>At this stage, null values have been addressed, but the data type of the "Last_Sync" column remains as a string because there are values such as "Last Sync is Null," which serve as indicators that the previous value was null. Below is an example of validated data, and it is evident that the format of the "Last_Sync" column now aligns with the BigQuery format.</p>
<p>The format of "Last_Sync" before transformation.</p>
<p><img width="875" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/be6be036-5c15-49c4-8553-c01a929ad148"></p>
<p>The format of "Last_Sync" after transformation.</p>
<p><img width="942" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/fe41df3d-1ba5-4674-9b53-d57973979470"></p>

#### Load
Script:
<p><img width="739" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/1e2e1c5f-7c70-44e0-93b0-bb84a73ccae9"></p>
Logic:
<p><img width="978" alt="image" src="https://github.com/arrlanyhars/edtech-airflow/assets/71999653/a4f9ca4a-6c7b-49cf-8694-6774677bc459"></p>


# Attachments
Script: https://github.com/arrlanyhars/edtech-airflow/blob/main/dag_pipeline_airflow.py
<p>Website's Url: https://dapo.kemdikbud.go.id/sp/2/370100</p>
