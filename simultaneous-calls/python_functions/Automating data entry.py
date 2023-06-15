import csv

def automate_data_entry(file_name):
    data_list = []

    with open(file_name, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            data_list.append(row)

    return data_list

# Example usage
file_name = 'data.csv'
data = automate_data_entry(file_name)
print(data)