import re
import time
import datetime
import json
import csv


def parse_vmstat_log(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    key_pat = re.compile("[a-zA-Z]+")
    keys = re.findall(key_pat, lines[1].strip())
    keys = [f"vmstat_{k}" for k in keys[:-1]]
    keys.append("timestamp")
    
    lines = [line.strip() for line in lines[2:]]
    num_pat = re.compile("[0-9]+")
    timestamp_pat = re.compile("[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}")
    data = []
    for line in lines:
        data_scheme = {k: 0 for k in keys}
        values = re.findall(num_pat, line)
        try:
            [ data_scheme.update({keys[i]: values[i]}) for i in range(len(keys)) ]
        except IndexError:
            print(len(keys))
            print(f"{keys = }")
            print(len(values))
            print(f"{values = }")
            exit(1)
        timestamp = re.findall(timestamp_pat, line)[0]
        timestamp = int(time.mktime(datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').timetuple()))
        data_scheme[keys[-1]] = timestamp
        data.append(data_scheme)
    return data


def parse_iostat_log(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    data = data['sysstat']['hosts'][0]['statistics']
    data = [sample['disk'][0] for sample in data]
    data = [{f"iostat_{k}": sample[k] for k in sample.keys()} for sample in data]
    return data


def aggregate_LL(vmstat, iostat):
    [ vmstat_sample.update(iostat_sample) for vmstat_sample, iostat_sample in zip(vmstat, iostat) ]
    return vmstat


def write_csv(low_level, outfile):
    with open(outfile, 'w') as f:
        dict_writer = csv.DictWriter(f, low_level[0].keys())
        dict_writer.writeheader()
        dict_writer.writerows(low_level)


if __name__ == "__main__":
    vmstat = parse_vmstat_log("vmstat_log_file.txt")
    iostat = parse_iostat_log("iostat_log_file.txt")
    low_level = aggregate_LL(vmstat, iostat)
    write_csv(low_level, "low_level_stats.csv")
