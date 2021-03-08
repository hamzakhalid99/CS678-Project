import csv
import os

top_50 = []
with open('Alexa_top_50_global_09-02-2021.csv') as csv_file:
    csv_obj = csv.reader(csv_file)
    i = 1
    for row in csv_obj:
        top_50.append("rank#" + str(i) + "-" + row[0])
        i += 1

# for commands and stuff:
# https://github.com/GoogleChrome/lighthouse#using-the-node-cli

for i in range(len(top_50)):
    command = "lighthouse http://" + top_50[i] + " --output=json --output-path ./" + top_50[i] + ".json"
    os.system(command)

print("\n\n\n --- DONE --- \n")