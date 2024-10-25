import requests
import uuid
import time
from SETTINGS import SEGMENT_CONFIGS, UDC_DATE_RANGE, PROBE_POLLING_INTERVAL
from utils import calculate_date_range

API_key = "80e7fd1270444f1ca112cba3fc4c836e"



def request_udc_directory():
    return f"https://pda-api.ritis.org/v2/submit/udc?key={API_key}"



def submit_udc_job(data_source, segment_ids):
    url = request_udc_directory()
    job_uuid = str(uuid.uuid4())
    start_date, end_date = calculate_date_range(UDC_DATE_RANGE)
    
    params = {
        "uuid": job_uuid,
        "dataSourceId": data_source,
        "segments": {
            "type": "tmc",
            "ids": segment_ids
        },
        "dates": [
            {
                "start": start_date,
                "end": end_date
            }
        ],
        "costs": {
            "catt.inrix.udc.commercial": {"2024": 4.0},
            "catt.inrix.udc.passenger": {"2024": 5.0}
        },
        "volumePriority": ["inrix_2013"],
        "carOccupancy": 1.7,
        "threshold": 0,
        "thresholdType": "none",
        "calculateAgainst": "freeflow",
        "percentCommercial": 10,
        "useDefaultPercent": False
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=params, headers=headers, verify=False)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return None, None

    response_json = response.json()
    job_id = response_json.get("id")
    return job_uuid, job_id



def poll_udc_job_status(job_id):
    url = f"https://pda-api.ritis.org/v2/jobs/status?key={API_key}&jobId={job_id}"
    while True:
        response = requests.get(url, verify=False)
        response_json = response.json()
        if response_json.get("state") in ["SUCCEEDED", "FAILED"]:
            return response_json
        print("Waiting for job completion...")
        time.sleep(PROBE_POLLING_INTERVAL)



def fetch_udc_result(job_uuid, alias):
    url = f"https://pda-api.ritis.org/v2/results/udc?key={API_key}&uuid={job_uuid}"
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        filename = f"API_Data/{alias}_udc_data.json"
        with open(filename, "w") as f:
            f.write(response.text)
        print(f"Data saved as {filename}")
    else:
        print(f"Error fetching UDC result for {alias}: {response.status_code}")



def run_job_for_segment(config):
    alias = config['alias']
    data_source = config['data_source']
    segment_ids = config['tmc_ids']

    print(f"Starting UDC job for {alias}...")
    job_uuid, job_id = submit_udc_job(data_source, segment_ids)
    if not job_uuid or not job_id:
        print(f"Failed to start job for {alias}")
        return

    job_status = poll_udc_job_status(job_id)
    if job_status.get("state") == "SUCCEEDED":
        fetch_udc_result(job_uuid, alias)
    elif job_status.get("state") == "FAILED":
        print(f"UDC job failed for {alias}")



def main():
    for config in SEGMENT_CONFIGS:
        run_job_for_segment(config)

if __name__ == "__main__":
    main()
    