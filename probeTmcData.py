import requests
import uuid
import time
from datetime import datetime, timedelta
from SETTINGS import CITY, ALL_TMC_IDS, DATA_SOURCE_DEFAULT

API_key = "80e7fd1270444f1ca112cba3fc4c836e"





def request_directory(mode):
    if mode == "Network":
        return f"https://pda-api.ritis.org/v2/segment/search/tmcs?key={API_key}"
    elif mode == "Export":
        return f"https://pda-api.ritis.org/v2/submit/export?key={API_key}"
    elif mode == "Result":
        return f"https://pda-api.ritis.org/v2/results/export?key={API_key}&uuid="



def get_dates(TIME_RANGE="day"):
    today = datetime.now()
    
    if TIME_RANGE == "day":
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
    elif TIME_RANGE == "week":
        start_date = today - timedelta(days=7)
        end_date = today
    elif TIME_RANGE == "month":
        start_date = today - timedelta(days=30)
        end_date = today
    elif TIME_RANGE == "year":
        start_date = today - timedelta(days=365)
        end_date = today
    else:
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
    
    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def submit_export_job():
    url = request_directory("Export")
    job_uuid = str(uuid.uuid4())  

    all_columns = [
        "speed", "historical_average_speed", "average_speed",
        "reference_speed", "travel_time_minutes", "travel_time",
        "confidence_score", "confidence", "data_quality", "cvalue"
    ]

    start_date, end_date = get_dates("day")

    params = {
        "uuid": job_uuid,
        "segments": {"type": "tmc", "ids": ALL_TMC_IDS},
        "dates": [{"start": start_date, "end": end_date}],
        "dow": [0, 1, 2, 3, 4, 5, 6],
        "dsFields": [{"id": DATA_SOURCE_DEFAULT, "columns": all_columns}],
        "title": "Probe Data Export",
        "description": "Export job for raw probe data",
        "granularity": {"type": "minutes", "value": 1},
        "includeIsoTzd": False,
        "timeZone": "America/New_York",
        "country": "USA",
        "outputFormat": "csv"
    }
    
    print(f'\n\nWe are in {CITY}, using {DATA_SOURCE_DEFAULT}\n\n')
    print(f"Submitting export job to {url} with parameters:")
    print(params)

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=params, headers=headers, verify=False)
    print("Response status code:", response.status_code)
    print("Response content:", response.content)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return None, None

    response_json = response.json()
    job_id = response_json.get("id")
    return job_uuid, job_id

def poll_job_status(job_id):
    url = f"https://pda-api.ritis.org/v2/jobs/status?key={API_key}&jobId={job_id}"
    while True:
        response = requests.get(url, verify=False)
        print("Job status response status code:", response.status_code)
        response_json = response.json()
        print("Job status response content:", response_json)
        if response_json.get("state") in ["SUCCEEDED", "FAILED"]:
            return response_json
        print("Job not yet complete. Waiting...")
        time.sleep(10) # Wait for 10 seconds before checking again

def fetch_export_result(job_uuid):
    url = request_directory("Result") + job_uuid
    response = requests.get(url, verify=False)
    print("Export result response status code:", response.status_code)
    if response.status_code == 200:
        with open("probe_data.zip", "wb") as f:
            f.write(response.content)
        print("Data saved as probe_data.zip")
    else:
        print(f"Error fetching export result: {response.status_code}")

def main():
    job_uuid, job_id = submit_export_job()
    if not job_uuid or not job_id:
        return
    while True:
        job_status = poll_job_status(job_id)
        if job_status.get("state") == "SUCCEEDED":
            fetch_export_result(job_uuid)
            break
        elif job_status.get("state") == "FAILED":
            print("Job failed.")
            break

if __name__ == "__main__":
    main()