import sys
import os
import csv
import json

# maybe later:
# defaults = {
#     "output_file_types" : "json,csv", # can convert json to html at https://googlechrome.github.io/lighthouse/viewer/
#     "save_log" : True,

# }

on_phone_command = ' ' # https://github.com/GoogleChrome/lighthouse/blob/master/docs/readme.md#testing-on-a-mobile-device
# ^ must have previously connected with the phone with adb and set port to 9222 and forwarding daemon in adb set. Sample:
# $ adb kill-server
# $ adb devices -l
# * daemon not running. starting it now on port 5037 *
# * daemon started successfully *
# 00a2fd8b1e631fcb       device usb:335682009X product:bullhead model:Nexus_5X device:bullhead
# $ adb forward tcp:9222 localabstract:chrome_devtools_remote
# $ lighthouse --port=9222 --screenEmulation.disabled --throttling.cpuSlowdownMultiplier=1 https://example.com

def error_checker(json_filename):
    # Checking if there were any errors:
    
    with open(json_filename, encoding="utf-8") as file_obj: 
        json_obj = json.load(file_obj) 
        
        error = True
        try:
            json_obj['runtimeError']
        except:
            error = False 
    
    return error

def audit(urls):
    error_urls = {}
    for rank in urls:
        url = urls[rank]
        command = "lighthouse" + on_phone_command + "http://" + url + " --output json,csv --enable-error-reporting --output-path ./data/" + rank + "-" + url + ".json ./data/" + rank + "-" + url + ".csv"
        
        print("Auditing:", url)
        os.system(command) # for commands: https://github.com/GoogleChrome/lighthouse#using-the-node-cli
        if error_checker("./data/" + rank + "-" + url + ".report.json") == True:
            error_urls[rank] = url
            print("Audit failed for:", url)
        else:
            print("Audit successful for:", url)
    return error_urls

def parse_csv(filename):
    urls = {}
    with open(filename) as csv_file:
        # csv row format: rank, url
        csv_obj = csv.reader(csv_file)
        for row in csv_obj:
            urls[str(row[0])] = row[1].lower()
    return urls

if __name__ == "__main__":
    # expected terminal command: python3 lh_script.py data.csv phone=true
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
    else:
        sys.exit("ERROR: No data csv file provided. Program Exiting.")  

    if len(sys.argv) >= 3:
        if sys.argv[2] == 'phone=true':
            on_phone_command = ' --port=9222 --screenEmulation.disabled --throttling.cpuSlowdownMultiplier=1 '    

    urls = parse_csv(filename)


    error_urls = audit(urls)
    while len(error_urls) != 0: # re-audit websites that gave an error
        audit(error_urls)

    print("\n\n\n --- ALL DONE --- \n")