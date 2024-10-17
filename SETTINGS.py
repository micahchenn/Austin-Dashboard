# SETTINGS.py

PM_DATE_RANGE = "week"  # Change this to "day", "week", "month", or "year"
CITY = "Austin"  # Change this to the desired city

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
