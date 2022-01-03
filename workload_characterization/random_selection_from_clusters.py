import csv
import sys
import random


def read_data(filename):
    with open(filename, 'r') as f:
        csv_data = [line for line in csv.DictReader(f)]
    return csv_data


def random_selection(csv_data):
    num_cluster = max([row['Cluster'] for row in csv_data])
    random.shuffle(csv_data)
    selection = {}
    for row in csv_data:
        cluster = row['Cluster']
        if cluster not in selection:
            selection[cluster] = row
        if len(selection) == num_cluster:
            break
    return [row for row in selection.values()]


def write_data(filename, selection):
    with open(filename, 'w') as f:
        dict_writer = csv.DictWriter(f, selection[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(selection)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_filename> <output_filename>")
        exit(1)
    input_filename, output_filename = sys.argv[1], sys.argv[2]
    csv_data = read_data(input_filename)
    selection = random_selection(csv_data)
    write_data(output_filename, selection)
