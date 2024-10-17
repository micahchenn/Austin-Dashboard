from datetime import datetime, timedelta




def calculate_date_range(date_range):
    end_date = datetime.now()
    if date_range == "day":
        start_date = end_date - timedelta(days=1)
    elif date_range == "week":
        start_date = end_date - timedelta(weeks=1)
    elif date_range == "month":
        start_date = end_date - timedelta(days=30)  # Approximate month
    elif date_range == "year":
        start_date = end_date - timedelta(days=365)
    else:
        raise ValueError("Invalid date range specified.")
    
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


