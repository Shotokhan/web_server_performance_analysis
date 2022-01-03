import itertools
import csv


def read_csv(filename):
    with open(filename, 'r') as f:
        csv_data = [row for row in csv.DictReader(f)]
    return csv_data


def get_throughput(csv_data):
    csv_data = sorted(csv_data, key=lambda row: int(row['timeStamp']))
    min_ts = int(csv_data[0]['timeStamp'])
    max_ts = int(csv_data[-1]['timeStamp'])
    duration_seconds = (max_ts - min_ts) / 1000
    throughput_per_second = len(csv_data) / duration_seconds
    return throughput_per_second


def get_avg_response_time(csv_data):
    elapsed_times = [int(row['elapsed']) / 1000 for row in csv_data]
    avg_response_time = sum(elapsed_times) / (len(elapsed_times) - 1)
    return avg_response_time


def filenames(ctt_rate=None, page_size=None, n_reps=5):
    if ctt_rate is None:
        ctt_rates = ["low_", "medium_", "high_"]
    else:
        ctt_rates = [ctt_rate + "_"]
    if page_size is None:
        page_sizes = ["low_", "medium_", "high_"]
    else:
        page_sizes = [page_size + "_"]
    n_rep = [str(i+1) for i in range(n_reps)]
    ext = [".csv"]
    prod = itertools.product(ctt_rates, page_sizes, n_rep, ext)
    names = ["".join(list(i)) for i in prod]
    return names


def write_csv(experiments, mean_response_time, mean_tps, filename):
    # I take experiments as input because I want ordered rows
    # experiments = [k for k in mean_response_time.keys()]
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        fields = ["Experiment", "Average_Response_Time", "Throughput"]
        writer.writerow(fields)
        for exp in experiments:
            row = [exp, mean_response_time[exp], mean_tps[exp]]
            writer.writerow(row)


def old_main():
    n_reps = 5
    sizes = ["low", "medium", "high"]
    mean_response_time = {}
    mean_tps = {}
    sorted_keys = []
    for ctt_rate in sizes:
        for page_size in sizes:
            names = filenames(ctt_rate=ctt_rate, page_size=page_size)
            throughput_list = []
            avg_response_time_list = []
            for name in names:
                csv_data = read_csv(name)
                throughput_list.append(get_throughput(csv_data))
                avg_response_time_list.append(get_avg_response_time(csv_data))
            mean_throughput = sum(throughput_list) / n_reps
            mean_avg_response_time = sum(avg_response_time_list) / n_reps
            
            current_key = f"ctt_{ctt_rate}_page_size_{page_size}"
            sorted_keys.append(current_key)
            mean_tps[current_key] = mean_throughput
            mean_response_time[current_key] = mean_avg_response_time
    write_csv(sorted_keys, mean_response_time, mean_tps, "aggregate.csv")


if __name__ == "__main__":
    names = filenames()
    resp_time_dict = {}
    tps_dict = {}
    for name in names:
        csv_data = read_csv(name)
        resp_time = get_avg_response_time(csv_data)
        tps = get_throughput(csv_data)

        resp_time_dict[name] = resp_time
        tps_dict[name] = tps
    write_csv(names, resp_time_dict, tps_dict, "aggregate.csv")

