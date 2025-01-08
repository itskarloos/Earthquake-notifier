from datetime import datetime, timedelta

# Generate the start and end times dynamically
end_time = datetime.utcnow()
start_time = end_time - timedelta(minutes=1000)

# Parameters for the earthquake API
PARAMS = {
    "format": "geojson",              # Output format
    "starttime": start_time.isoformat(),  # Start date in ISO8601 format
    "endtime": end_time.isoformat(),      # End date in ISO8601 format
    "minmagnitude": 3,               # Minimum magnitude
    "maxmagnitude": 7,               # Maximum magnitude
    "minlatitude": 3.4,              # Ethiopia's southern boundary
    "maxlatitude": 14.9,             # Ethiopia's northern boundary
    "minlongitude": 32.9,            # Ethiopia's western boundary
    "maxlongitude": 48.0,            # Ethiopia's eastern boundary
    "orderby": "time",               # Order by most recent
    "limit": 10                      # Limit to 10 results
}
