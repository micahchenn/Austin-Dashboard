import requests
import uuid
import time
from datetime import datetime, timedelta
import certifi
from SETTINGS import PM_DATE_RANGE, SEGMENT_CONFIGS, PROBE_POLLING_INTERVAL
from utils import calculate_date_range


API_key = "80e7fd1270444f1ca112cba3fc4c836e"

# Define the date ranges to be used (Day, Week, Month)
DATE_RANGES = {
    "Day": (datetime.now(), datetime.now()),
    "Week": (datetime.now(), datetime.now() + timedelta(weeks=1)),
    "Month": (datetime.now(), datetime.now() + timedelta(days=30)),
}

def request_directory(mode):
    if mode == "PM_Export":
        return f"https://pda-api.ritis.org/v2/submit/pm?key={API_key}"
    elif mode == "PM_Result":
        return f"https://pda-api.ritis.org/v2/results/pm?key={API_key}&uuid="


def poll_job_status(job_id, alias, progress_message):
    url = f"https://pda-api.ritis.org/v2/jobs/status?key={API_key}&jobId={job_id}"
    while True:
        response = requests.get(url, verify=False)  # Disable SSL verification
        print(f"[{alias}] {progress_message}")
        print(f"Job status response status code: {response.status_code}")
        response_json = response.json()
        print(f"Job status response content: {response_json}")
        if response_json.get("state") in ["SUCCEEDED", "FAILED"]:
            return response_json
        print(f"Job for alias '{alias}' not yet complete. Waiting 10 seconds before polling again...")
        time.sleep(PROBE_POLLING_INTERVAL)  # Wait for polling interval


def fetch_pm_result(job_uuid, alias, date_range_name):
    url = request_directory("PM_Result") + job_uuid
    response = requests.get(url, verify=False)  # Disable SSL verification
    print(f"PM result response status code for alias '{alias}': {response.status_code}")
    if response.status_code == 200:
        # Append the date range name to the filename
        filename = f"API_Data/{alias}_{date_range_name}_pm_data.json"
        with open(filename, "w") as f:
            f.write(response.text)
        print(f"Data saved as {filename}")
    else:
        print(f"Error fetching PM result for alias '{alias}': {response.status_code}")


def submit_pm_job(tmc_ids, alias, data_source, start_date, end_date):
    url = request_directory("PM_Export")
    job_uuid = str(uuid.uuid4())

    params = {
        "uuid": job_uuid,
        "groupSegments": [
            {
                "alias": alias,
                "segments": {
                    "type": "TMC",
                    "ids": tmc_ids
                }
            }
        ],
        "dataSourceId": data_source,
        "requestIntervals": [
            {
                "dateRange": {"start": start_date.strftime("%Y-%m-%d"), "end": end_date.strftime("%Y-%m-%d")},
                "dow": [0, 1, 2, 3, 4, 5, 6],
                "granularity": {"type": "minutes", "value": 15}  # CHANGE TO 15 MINUTES
            }
        ],
        "metrics": [
            "bufferIndex", "planningTimeIndex", "travelTimeIndex", "congestion",
            "averageCongestion", "averageSpeed"
        ],
        "title": f"Performance Metrics Job for {alias}",
        "description": f"Job for calculating performance metrics for {alias}",
        "timeZone": "America/New_York",
        "country": "USA"
    }

    print(f"Submitting performance metrics job for {alias} to {url} with parameters:")
    print(params)

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=params, headers=headers, verify=False)  # Disable SSL verification
    print(f"Response status code for alias '{alias}': {response.status_code}")
    print(f"Response content: {response.content}")

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} for alias '{alias}'")
        return None, None

    response_json = response.json()
    job_id = response_json.get("id")
    return job_uuid, job_id

# Main function that loops through different configurations and date ranges
def main():
    total_segments = len(SEGMENT_CONFIGS)
    for index, config in enumerate(SEGMENT_CONFIGS):
        tmc_ids = config["tmc_ids"]
        alias = config["alias"]
        data_source = config["data_source"]

        for date_range_name, (start_date, end_date) in DATE_RANGES.items():
            progress_message = f"Processing {index+1}/{total_segments} TMCs for alias '{alias}' with date range '{date_range_name}'..."
            print(progress_message)

            job_uuid, job_id = submit_pm_job(tmc_ids, alias, data_source, start_date, end_date)
            if not job_uuid or not job_id:
                print(f"Skipping alias '{alias}' due to error in job submission.")
                continue

            job_status = poll_job_status(job_id, alias, progress_message)
            if job_status.get("state") == "SUCCEEDED":
                fetch_pm_result(job_uuid, alias, date_range_name)  # Pass the date range name for the filename
            elif job_status.get("state") == "FAILED":
                print(f"Job for alias '{alias}' failed.")

if __name__ == "__main__":
    main()