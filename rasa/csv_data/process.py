input_file = open("unprocessed.txt", "r")
output_file = open("processed.txt", "w+")

for line in input_file:
    output_file.write("- " + line)