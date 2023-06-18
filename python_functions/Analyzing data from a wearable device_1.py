import csv
from datetime import datetime

def analyze_wearable_data(file_path, target_date):
    total_heart_rate = 0
    total_steps = 0
    heart_rate_count = 0

    with open(file_path, mode='r') as csvfile:
        data_reader = csv.reader(csvfile)
        next(data_reader)  # Skip header

        for row in data_reader:            
            timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            if timestamp.date() == target_date.date():
                heart_rate = int(row[1])
                steps = int(row[2])
                
                total_heart_rate += heart_rate
                total_steps += steps
                heart_rate_count += 1

    if heart_rate_count == 0:
        return "No data available for the given date."
    else:
        average_heart_rate = total_heart_rate / heart_rate_count
        return f"Average heart rate: {average_heart_rate}, Total steps: {total_steps}"

# Example usage
file_path = "wearable_data.csv"
target_date = datetime.strptime("2021-06-20", "%Y-%m-%d")
result = analyze_wearable_data(file_path, target_date)
print(result)