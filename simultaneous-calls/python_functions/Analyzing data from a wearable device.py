def analyze_wearable_data(data):
    total_heart_rate = 0
    total_steps = 0
    total_calories = 0

    for entry in data:
        total_heart_rate += entry['heart_rate']
        total_steps += entry['steps']
        total_calories += entry['calories']

    average_heart_rate = total_heart_rate / len(data)

    result = {
        "average_heart_rate": average_heart_rate,
        "total_steps": total_steps,
        "total_calories": total_calories
    }

    return result

# Example usage:
wearable_data = [
    {"timestamp": "2022-01-01 10:00:00", "heart_rate": 70, "steps": 1000, "calories": 50},
    {"timestamp": "2022-01-01 11:00:00", "heart_rate": 80, "steps": 1500, "calories": 80},
    {"timestamp": "2022-01-01 12:00:00", "heart_rate": 75, "steps": 1200, "calories": 60},
]

result = analyze_wearable_data(wearable_data)
print(result)