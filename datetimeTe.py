# from itertools import groupby
# from datetime import datetime

# # Example data
# class Item:
#     def __init__(self, date, value):
#         self.date = date
#         self.value = value

# data = [
#     Item(datetime(2024, 7, 31), 10),
#     Item(datetime(2024, 7, 31), 15),
#     Item(datetime(2024, 8, 1), 5),
#     Item(datetime(2024, 8, 1), 20),
# ]

# # Sort data by date to prepare for grouping
# data.sort(key=lambda item: item.date)

# # Group data by date
# grouped_by_date = groupby(data, key=lambda item: item.date)

# # Calculate total value and count for each date
# sum_and_count_by_date = {
#     date: {
#         'total_value': sum(item.value for item in group_list),
#         'count': len(group_list),
#         'double_count': 2 + sum(item.value for item in group_list)
#     }
#     for date, group in grouped_by_date
#     for group_list in [list(group)]  # Convert group to a list
# }

# # Display results
# for date, stats in sum_and_count_by_date.items():
#     print(f"Date: {date}, Total Value: {stats['total_value']}, Count: {stats['count']}, doubleSum: {stats['double_count']}")


# from itertools import groupby
# from operator import itemgetter

# # Example data: list of dictionaries with multiple columns
# data = [
#     {"name": "Alice", "city": "New York", "age": 30},
#     {"name": "Bob", "city": "Los Angeles", "age": 25},
#     {"name": "Alice", "city": "New York", "age": 28},
#     {"name": "Charlie", "city": "New York", "age": 35},
#     {"name": "Bob", "city": "Los Angeles", "age": 25},
#     {"name": "Alice", "city": "San Francisco", "age": 30},
# ]

# # Specify the columns to group by
# group_keys = ['name', 'city']

# # Sort data by the group keys
# sorted_data = sorted(data, key=itemgetter(*group_keys))

# # Group by the specified keys
# grouped_data = groupby(sorted_data, key=itemgetter(*group_keys))

# # Process the groups
# for key, group in grouped_data:
#     group_list = list(group)
#     count = len(group_list)
#     ageSum = sum(item['age'] for item in group_list)
#     print(f"Group: {key}, Count: {count}, Items: {group_list}, Sum: {ageSum}")

from itertools import groupby
from operator import attrgetter
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

# Define a dataclass to represent each data item
@dataclass
class Person:
    name: str
    city: str
    age: int
    start_time: datetime
    duration: timedelta

# Example list of Person instances
data: List[Person] = [
    Person(name="Alice", city="New York", age=30, start_time=datetime(2024, 8, 8, 9, 0), duration=timedelta(hours=1, minutes=30)),
    Person(name="Bob", city="Los Angeles", age=25, start_time=datetime(2024, 8, 8, 10, 0), duration=timedelta(hours=2)),
    Person(name="Alice", city="New York", age=28, start_time=datetime(2024, 8, 8, 11, 0), duration=timedelta(hours=1)),
    Person(name="Charlie", city="New York", age=35, start_time=datetime(2024, 8, 8, 9, 0), duration=timedelta(hours=1, minutes=45)),
    Person(name="Bob", city="Los Angeles", age=25, start_time=datetime(2024, 8, 8, 13, 0), duration=timedelta(hours=1, minutes=15)),
    Person(name="Alice", city="San Francisco", age=30, start_time=datetime(2024, 8, 8, 10, 0), duration=timedelta(hours=1, minutes=30)),
]

# Specify the attributes to group by
group_keys = ['name', 'city']

# Sort data by the group keys
sorted_data = sorted(data, key=attrgetter(*group_keys))

# Group by the specified attributes
grouped_data = groupby(sorted_data, key=attrgetter(*group_keys))

# Process the groups
for key, group in grouped_data:
    group_list = list(group)
    count = len(group_list)
    total_age = sum(item.age for item in group_list)
    total_duration = sum((item.duration for item in group_list), timedelta())
    print(f"Group: {key}, Count: {count}, Total Age: {total_age}, Total Duration: {total_duration}, Items: {group_list}")
