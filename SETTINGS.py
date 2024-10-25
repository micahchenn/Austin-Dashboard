# SETTINGS.py
PROBE_POLLING_INTERVAL = 60  # Interval in seconds for polling the probe data API

PM_DATE_RANGE = "month"  # Change this to "day", "week", "month", or "year"
UDC_DATE_RANGE = "month"  # Change this to "day", "week", "month", or "year"
CITY = "Austin"  # Change this to the desired city

TMC_NAME = "tmc"  # Change this to the appropriate TMC name for the city

# Segment IDs for each city
segments = {
    "Atlanta": ['112+05857'],  # Add the actual segment IDs for Atlanta
    "Texas": [],  # Add the segment IDs for Texas
    "Austin": [
        '112P05045', '112P05046', '112P05047', '112P13222', '112P04895',
        '112N16873', '112P04896', '112+05046', '112P04897', '112+05047',
        '112P04898', '112P04899', '112N04898', '112+04896', '112-04898',
        '112N04899', '112+04897', '112-04899', '112+04898', '112+04899',
        '112+04900'
    ]
}

# Data sources for each city
data_sources = {
    "Atlanta": "here_tmc",
    "Texas": "inrix_tmc",
    "Austin": "inrix_tmc"
}

# Automatically select segment IDs and data source based on CITY
SEGMENT_ID = segments[CITY]
DATA_SOURCE = data_sources[CITY]

DATA_SOURCE_DEFAULT = "inrix_tmc"  # Change this to the desired data source
# config.py

SEGMENT_CONFIGS = [
    {
        "alias": "Round Rock",
        "tmc_ids": ['112P05045', '112P05046', '112P05047', '112P13222', '112P04895'],
        "data_source": "inrix_tmc"
    },
    {
        "alias": "Westlake",
        "tmc_ids": ['112N04899', '112+04897', '112-04899', '112+04898', '112+04899'],
        "data_source": "inrix_tmc"
    },
    # Add as many configurations as you need
    {
        "alias": "Travis",
        "tmc_ids": ['112N09579', '112+09576', '112-09578', '112+09577', '112-09579', '112+09578'],
        "data_source": "inrix_tmc"
    },
    {
        "alias": "East Austin",
        "tmc_ids": ['112N09579', '112+09576', '112-09578', '112+09577', '112-09579', '112+09578'],
        "data_source": "inrix_tmc"
    },

    
]

# Combine all tmc_ids into a single list
ALL_TMC_IDS = []
for config in SEGMENT_CONFIGS:
    ALL_TMC_IDS.extend(config["tmc_ids"])
