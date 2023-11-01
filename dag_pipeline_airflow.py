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
  "project_id": "sandbox-data-401207",
  "private_key_id": "4c2d814d3cffb546b3b98b9cb36c50d4cddc9fde",
  "private_key": "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC0pYRdrts08gU7\n1Hq4vUE2kB9U1rmNSuoWy2i5qMMVYyZmIYXKQYZ/V0bFQR6z/OTdg9fo5fwjRwUW\nTVE9BoQ4Ke5h4PPUd73zKvKlgNU43eg6INcZRyRmE4vHe3quG/OA3sdhaevS9phP\nhIcOWxkByX3UPhEmurR/dRh9PXN2CyoB/aYAdBPeL+KHf/CNFVdX/2CLLszJUjcM\noIvyuaA7W3nQmad8FoPorvtCO9+B7PzDbGP522WS7ms4A9Oj0IW9n2NoYffEsi7Z\nylASofF4LuLAv60+KWKrlu+J+XHCRrhDAzJ2eKtsCjVtokqbDCd50J7gJg4MrAoz\nUAFjJeKxAgMBAAECggEACyHnIBnaPu9KRMdhn7hkCC+GCsWnzi4HcourAsQEb7E6\nSNF4jAARQJA5l4bdlER5uy/4koz3xpnGFbuCjeL0q3xkCSqihB2z+kQTi4D+wuAk\nA08KSm/Arby3IL46j3fAABlaiqWLJ6dUOBRH+WnCRwKqizWe+3bGkFNARNmQX74S\nYImhcz9k1OpHVwzSROnzjSf8NDcQQGV/WICZ4fidHDzFkpRu3wQXbuHQLjUrefXU\n8BC5QdnisVcIgk5f03RBRwlBRQLX6vYswUtC6PKc+xnKtS9HJB1+FL/d4GdGFICT\n3/bbyoZlbL0sl0lyMfjKj+ebaYgOg/uti0wXBqTv9QKBgQDa0qL4fQi6PFvNVtjU\nCYAYGu36TiT09qBTTSGevXnZgwqp1prkfh689LhuPQt1AgBiEZndpclzQ1r4Erj7\nVbrPWmq9w/8cinI09rh+hn+9vRnvFUSzlPRaXHopCg+D6QJRWx4PHxzf61KC3ZGN\nkZZ2VgmAq/fArVpUn99xfmr09QKBgQDTVnZ9OJIGwFNwzzfldtgjIsrL2WkVIrg+\nnJ79x2K6eub0PiJ7l00ExZSltTCQFE6a/IMxTqhLk15nwyF6LAJ96HTqt0iqp5Gm\nqciUOV2tsAkQMexByPybRRW7R3F3E9+UHPtav3lWAiU5Ll6T116uQlW/ewhQspSI\nPZ9aJKhBTQKBgQCK2+e3MAD9zZej8lyeEXlL0qr5j+U73dVXhzayeSJ9uP5nUFvy\na2YuGk1/BxXiJmb/1JODZ9UyY6eyjI7+TyTAuGvMCDg3cFOQ8I+bGtatHPb8FM8H\n9popTU3oBQ5bct2ZquykQ+Ya4kX17YyT/bMxXN+i233YsykDUoCEkOhmkQKBgQCs\nSIYbmuxgGJVtF2Bn7bRRIGHWQIxLsJwmXqO2Gr6/asWwQp71xegBhdiiJc1LB2L1\nMfj5TzgfNCn3yLkX0ZzOa5w0Y+oXRLeV+D8Npp5Zo3IgA7KoBmL3aSBIJfu3qTnQ\nkrfNyN3vYZxauxRazW3f/S/OA0xKDOrNDf9ECzIm2QKBgGRxuPQqKnzqH60YdrH2\npciLMD/HXumCzBFfx16rlAqq+eOCQ8GqP04GT9MqqfyBRvdSL+3BzYn1nlBH0Igi\nHKw2mu4FSxxedHZ2ui8GfLuOEGdDgBgKVytJ9ey5W4zTldnT59x56kQYExv4zvtf\nHPD8TmrcBSjyi9UFsIgmZhQL",
  "client_email": "test-de-skolla@sandbox-data-401207.iam.gserviceaccount.com",
  "client_id": "114411713664981792475",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test-de-skolla%40sandbox-data-401207.iam.gserviceaccount.com",
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
					selected_columns = ["nama", "npsn", "bentuk_pendidikan","status_sekolah","pd","sinkron_terakhir","induk_provinsi","induk_kabupaten"]
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

	destination_table_id  = "sandbox-data-401207.technical_test_de.ArryandaMaulani_PapuaSelatanKabMerauke_technicalTestSkolla"
	dataset_ref = client.dataset("technical_test_de", project="sandbox-data-401207")
	table_ref = dataset_ref.table("ArryandaMaulani_PapuaSelatanKabMerauke_technicalTestSkolla")
	
	available = 0
	try:
		client.get_table(table_ref)
		available = 1
	except Exception as e:
		print("Not available: ", str(e))
	
	if available == 1:
		query = f"""
			DROP TABLE `sandbox-data-401207.technical_test_de.ArryandaMaulani_PapuaSelatanKabMerauke_technicalTestSkolla`
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
