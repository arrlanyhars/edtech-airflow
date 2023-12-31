from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
from google.cloud import bigquery
import pendulum
from airflow.models.dag import DAG
from airflow.operators.dummy_operator import DummyOperator
import requests
import json
import pandas as pd
from airflow.utils.dates import days_ago
from google.cloud import storage
import os


GOOGLE_CLOUD_CREDENTIALS = {
  "type": "service_account",
  "project_id": "xxx",
  "private_key_id": "xxx",
  "private_key": "xxx",
  "client_email": "xxx",
  "client_id": "xxx",
  "auth_uri": "xxx",
  "token_uri": "xxx",
  "auth_provider_x509_cert_url": "xxx",
  "client_x509_cert_url": "xxx",
  "universe_domain": "googleapis.com"
}

storage_client = storage.Client()
client = bigquery.Client(credentials=bigquery.Credentials.from_service_account_info(GOOGLE_CLOUD_CREDENTIALS))

def extract_and_transform_data():
	#EXTRACT
	url = "https://dapo.kemdikbud.go.id/rekap/dataSekolah?id_level_wilayah=2&kode_wilayah=370100"
	
	response = requests.get(url)
	
	subdistrict_codes = []
	if response.status_code == 200:
		json_data = response.json()
		if isinstance(json_data, list):
			for item in json_data:
				subdistrict_codes.append(item.get("kode_wilayah"))
		else:
			print("Data isn't json array.")
	else:
		print("Failed. Status code:", response.status_code)
	
	list_of_subdistrict_codes = []
	for code in subdistrict_codes:
		code = code.replace("  ","")
		list_of_subdistrict_codes.append(int(code))
	
	frames = []
	for i in list_of_subdistrict_codes:
		url = f"https://dapo.kemdikbud.go.id/rekap/progresSP?id_level_wilayah=3&kode_wilayah={i}"
	
		response = requests.get(url)
	
		if response.status_code == 200:
			json_data = response.json()
			if isinstance(json_data, list):
				for item in json_data:
					selected_columns = ["nama",
							    "npsn",
							    "bentuk_pendidikan",
							    "status_sekolah",
							    "pd",
							    "sinkron_terakhir",
							    "induk_provinsi",
							    "induk_kabupaten"]
					df = pd.DataFrame([{col: item[col] for col in selected_columns} for item in json_data])
			else:
	      			print("Data isn't json array.")
		else:
	  		print("Failed. Status code:", response.status_code)

	df = df.rename(columns={"nama": "Nama",
				"npsn": "NPSN",
			      	"bentuk_pendidikan": "Level",
			      	"status_sekolah": "Status",
			      	"pd": "Students",
			      	"sinkron_terakhir": "Last_Sync",
			      	"induk_provinsi": "Province",
			      	"induk_kabupaten": "Subdistrict"
				})
	frames.append(df)
	result = pd.concat(frames)
	
	#Transformation
	valid_result = result.copy()
	valid_result = valid_result.fillna(0)
	def fill_date(x):
		if x['Last_Sync'] == 0:
			fill = 'Last Sync is Null'
		else:
			fill = pd.to_datetime(x['Last_Sync'], format='%d %b %Y %H:%M:%S')
		return fill
	
	valid_result['Last_Sync'] = valid_result.apply(lambda x: fill_date(x), axis=1)


	#LOAD
	destination_table_id  = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
	dataset_ref = client.dataset("xxxxxxxxxxxxxxxxxxxxxxxxxxxx", project="xxxxxxxxxxxxxxxxxxxxxxxxxxxx")
	table_ref = dataset_ref.table("xxxxxxxxxxxxxxxxxxxxxxxxxxxx")
	
	available = 0
	try:
		client.get_table(table_ref)
		available = 1
	except Exception as e:
		print("Not available: ", str(e))
	
	if available == 1:
		query = f"""
			DROP TABLE `xxxxxxxxxxxxxxxxxxxxxxxxxxxx`
		"""
		client.query(query).result
	else:
		client.load_table_from_dataframe(valid_result, destination_table_id)
	
	client.load_table_from_dataframe(valid_result, destination_table_id)

default_args = {
    	'owner': 'bq-airflow'
}

with DAG(
	dag_id = "bq_data_sekolah",
	default_args=default_args,
	schedule_interval="0 */1 * * *",
	start_date=days_ago(1),
) as dag:
	start = DummyOperator(task_id="start")
	
	data_processing_task = PythonOperator(
		task_id='extract_and_transform_data',
        	python_callable=extract_and_transform_data,
        	dag=dag,
    	)
	
	end = DummyOperator(task_id="end")

	start >> data_processing_task >> end

	if __name__ == "__main__":
        	dag.cli()
