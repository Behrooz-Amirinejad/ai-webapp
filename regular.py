import re

# Define the regular expression pattern
date_pattern = r'^(0?[1-9]|[12][0-9]|3[01])-(January|February|March|April|May|June|July|August|September|October|November|December)-\d{4}$'

# Example dates to test
dates = [
    "31-July-2024",
    "1 January 2023",
    "15 February 1999",
    "30 Feb 2020",  # Invalid
    "31 April 2020", # Invalid
    "12 March 20",   # Invalid
]

# Check each date
for date in dates:
    if re.search(date_pattern, date):
        print(f"'{date}' matches the format.")
    else:
        print(f"'{date}' does not match the format.")
