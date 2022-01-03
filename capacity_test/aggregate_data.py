import csv
import itertools
import math
import matplotlib.pyplot as plt


def print_warning(msg):
    print("[!] Warning: {}".format(msg))


def read_csv(filename):
    with open(filename, 'r') as f:
        csv_data = [row for row in csv.DictReader(f)]
    return csv_data


def validate_success(csv_data):
    # performance test can be done iff the system is working properly
    assert all([row['responseCode'] == '200' for row in csv_data])


def get_throughput(csv_data):
    # rows should be already sorted but I want to make sure they are sorted
    csv_data = sorted(csv_data, key=lambda row: int(row['timeStamp']))
    min_ts = int(csv_data[0]['timeStamp'])
    max_ts = int(csv_data[-1]['timeStamp'])
    duration_seconds = (max_ts - min_ts) / 1000
    throughput_per_second = len(csv_data) / duration_seconds
    return throughput_per_second


def get_avg_response_time(csv_data, cov_threshold=0.5, filename="not specified", silent_warning=False):
    # should elapsed time be converted to seconds?
    elapsed_times = [int(row['elapsed']) / 1000 for row in csv_data]
    avg_response_time = sum(elapsed_times) / (len(elapsed_times) - 1)
    sqr_elapsed_times = [(int(row['elapsed']) / 1000 ) ** 2 for row in csv_data]
    std_dev = math.sqrt( ( sum(sqr_elapsed_times) / (len(elapsed_times) - 1) ) - (avg_response_time ** 2) )
    cov = std_dev / avg_response_time
    if cov > cov_threshold:
        median = int(csv_data[len(csv_data) // 2]['elapsed']) / 1000
        if not silent_warning:
            print_warning("COV about response time is {} for file {}; median is {}, average value is {}".format(
                cov, filename, median, avg_response_time))
    return avg_response_time


def aggregate_exps(results, cov_threshold=0.5, filename="not specified", silent_warning=False, field="not specified"):
    avg = sum(results) / len(results)
    std_dev = math.sqrt( sum([i ** 2 for i in results]) / len(results) - avg ** 2 )
    cov = std_dev / avg
    if cov > cov_threshold:
        median = results[len(results) // 2]
        if not silent_warning:
            print_warning("COV about {} is {} for experiment {}; taking median equal to {} instead of average value {}".format(
                field, cov, filename, median, avg))
        avg = median
    return avg
        

def filenames(exp_sizes):
    base = ["ctt_"]
    sizes = exp_sizes
    rep_base = ["_n"]
    n_rep = ["1", "2", "3"]
    ext = [".csv"]
    prod = itertools.product(base, sizes, rep_base, n_rep, ext)
    names = ["".join(list(i)) for i in prod]
    return names


def single_exps(exp_size):
    base = ["ctt_"]
    sizes = [exp_size]
    rep_base = ["_n"]
    n_rep = ["1", "2", "3"]
    ext = [".csv"]
    prod = itertools.product(base, sizes, rep_base, n_rep, ext)
    names = ["".join(list(i)) for i in prod]
    return names


def show_plots(aggregate_tps, aggregate_response_time):
    load = [i for i in sorted(aggregate_tps.keys())]
    aggregate_tps = [aggregate_tps[i] for i in load]
    aggregate_response_time = [aggregate_response_time[i] for i in load]

    plt.figure(1)
    plt.plot(load, aggregate_tps, label="Throughput", marker='o')
    plt.xlabel("Load")
    plt.ylabel("Throughput")

    plt.figure(2)
    plt.plot(load, aggregate_response_time, label="Response Time", marker='o')
    plt.xlabel("Load")
    plt.ylabel("Response Time")

    aggregate_power = [aggregate_tps[i] / aggregate_response_time[i] for i in range(len(aggregate_tps))]

    plt.figure(3)   
    plt.plot(load, aggregate_power, label="Power", marker='o')
    plt.xlabel("Load")
    plt.ylabel("Power")
    
    plt.show()


def plot_and_store_csv(aggregate_tps, aggregate_response_time):
    load = [i for i in sorted(aggregate_tps.keys())]
    log_load = [20 * math.log10(i) for i in sorted(aggregate_tps.keys())]
    aggregate_tps = [aggregate_tps[i] for i in load]
    aggregate_response_time = [aggregate_response_time[i] for i in load]
    
    plt.plot(load, aggregate_tps, label="Throughput", marker='o')
    plt.xlabel("Load")
    plt.ylabel("Throughput")
    plt.savefig("throughput.png")
    plt.close()
    
    plt.plot(log_load, aggregate_tps, label="Throughput", marker='o')
    plt.xlabel("Load (db)")
    plt.ylabel("Throughput")
    plt.savefig("throughput_log_load.png")
    plt.close()

    plt.plot(load, aggregate_response_time, label="Response Time", marker='o')
    plt.xlabel("Load")
    plt.ylabel("Response Time")
    plt.savefig("response_time.png")
    plt.close()

    plt.plot(log_load, aggregate_response_time, label="Response Time", marker='o')
    plt.xlabel("Load (db)")
    plt.ylabel("Response Time")
    plt.savefig("response_time_log_load.png")
    plt.close()

    aggregate_power = [aggregate_tps[i] / aggregate_response_time[i] for i in range(len(aggregate_tps))]
    
    plt.plot(load, aggregate_power, label="Power", marker='o')
    plt.xlabel("Load")
    plt.ylabel("Power")
    plt.savefig("power.png")
    plt.close()

    plt.plot(log_load, aggregate_power, label="Power", marker='o')
    plt.xlabel("Load (db)")
    plt.ylabel("Power")
    plt.savefig("power_log_load.png")
    plt.close()

    with open("aggregate.csv", 'w') as f:
        writer = csv.writer(f)
        fields = ["load_samples", "throughput_per_second", "response_time_seconds", "power"]
        writer.writerow(fields)
        for i in range(len(load)):
            row = [load[i], aggregate_tps[i], aggregate_response_time[i], aggregate_power[i]]
            writer.writerow(row)
    

if __name__ == "__main__":
    silent_warning = True
    exp_sizes = ["60", "120", "180", "240", "300", "450", "600", "900", "1200", "1500", "1800", "2100", "2400", "2700", "3000"]
    names = filenames(exp_sizes)
    data_dict = {name: read_csv(name) for name in names}
    
    [validate_success(data_dict[name]) for name in data_dict.keys()]
    
    tps = {name: get_throughput(data_dict[name]) for name in names}
    response_time = {name: get_avg_response_time(data_dict[name], filename=name, silent_warning=silent_warning) for name in names}

    aggregate_tps = {}
    aggregate_response_time = {}
    for size in exp_sizes:
        sub_names = single_exps(size)
        sub_tps = [tps[name] for name in sub_names]
        sub_response_time = [response_time[name] for name in sub_names]
        exp_name = sub_names[0][:sub_names[0].find("_n")]

        res_tps = aggregate_exps(sub_tps, filename=exp_name, field="tps", cov_threshold=0.5, silent_warning=silent_warning)
        res_response_time = aggregate_exps(sub_response_time, filename=exp_name, field="response time", cov_threshold=0.5, silent_warning=silent_warning)
        load = float(size.replace("_", "."))

        aggregate_tps[load] = res_tps
        aggregate_response_time[load] = res_response_time

    print(f"{aggregate_tps = }")
    print(f"{aggregate_response_time = }")
    plot_and_store_csv(aggregate_tps, aggregate_response_time)

