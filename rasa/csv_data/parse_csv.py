import pandas as pd
import csv

file = "food_names/huge_ass_database.csv"
output_file = open("processed.txt", "w+")
with open(file, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter="\t")
    for line in csv_reader:
        if line[7] == "":
            continue
        else:
            output_file.write("- " + line[7] + "\n")