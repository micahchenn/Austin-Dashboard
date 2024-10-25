import subprocess
import sys
import time




def run_scripts():
    # Step 1: Run the probeRawData.py script
    result = subprocess.run([sys.executable, "probePmData.py"])
    if result.returncode != 0:
        print("probeRawData.py failed. Exiting.")
        return  # Exit the loop if this script fails

    # Step 2: Run the extractData.py script to unzip the file
    result = subprocess.run([sys.executable, "ProbeUdcData.py"])
    if result.returncode != 0:
        print("extractData.py failed. Exiting.")
        return  # Exit the loop if this script fails

    result = subprocess.run([sys.executable, "extractData.py"])
    if result.returncode != 0:
        print("algo.py failed. Exiting.")
        return  # Exit the loop if this script fails
    

    # Step 3: Run the algo.py script to analyze the data
    result = subprocess.run([sys.executable, "extractUDCData.py"])
    if result.returncode != 0:
        print("algo.py failed. Exiting.")
        return  # Exit the loop if this script fails

    result = subprocess.run([sys.executable, "summarizeData.py"])
    if result.returncode != 0:
        print("algo.py failed. Exiting.")
        return  # Exit the loop if this script fails



def TMC_Dat():
    result = subprocess.run([sys.executable, "probeTMCData.py"])
    if result.returncode != 0:
        print("probeRawData.py failed. Exiting.")
        return  # Exit the loop if this script fails
    
    result = subprocess.run([sys.executable, "timestamp.py"])
    if result.returncode != 0:
        print("time.py failed. Exiting.")
        return  # Exit the loop if this script fails





while True:
    run_scripts()
    TMC_Dat()
    print("Waiting for 5 minutes before running the scripts again...")
    #time.sleep(300)  
