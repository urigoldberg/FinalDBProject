import csv

def flush_to_csv(file, list):
    with open(file, 'a') as csvfile:
        writer = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for k, v in albums:
            writer.writerow(v)