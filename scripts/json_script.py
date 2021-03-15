import json
import os
import csv
import matplotlib.pyplot as plt
import random


'''
{
    "Website": {
        "numeric": {
            "unused-javascript": {
                "score": 0.3, "overallsaving": 0.3
            },
            ......
        },
        "binary": {
    
        },
        "null": []
    }
}
'''

def greatestImpact(audits):
    # print(audits)
    impact = {}
    for website, scores_dict in audits.items(): #scores_dict is the dictionary of scores.
        numeric_scores = scores_dict["numeric_score_audits"]
        impact[website] = {} 

        for  metric, details in numeric_scores.items(): #metric is what is being scored (e.g. unused-javascript), while details include scoring detailsm overall savings etc. 
            try:
                impact[website][metric] = [details["score"], details["overallSavingsMs"]]   #format: website -> [score, savings]
            except:
                pass
        print(impact)

        # print(numeric_scores)



def makeAuditList ():
    audit_obj = {}
    for file_name in os.listdir("data/json_files"):
        file_name = file_name[:-5].lower()
        audit_obj[file_name] = {
            "numeric_score_audits": {},
            "binary_score_audits": {},
            "null_score_audits": []
        }
    for file_name in sorted(os.listdir("data/json_files"), key=lambda x: int(x.partition('-')[0])):
        with open("data/json_files/" + file_name) as json_file:
            # file_name = file_name.split('.')[0].lower()
            file_name = file_name[:-5].lower()
            json_file_obj = json.load(json_file)
            audits = json_file_obj["audits"]
            for key, value in audits.items():
                if value["scoreDisplayMode"] == "numeric":
                    if "details" in value and "numericValue" in value:
                        if "overallSavingsMs" in value["details"]:
                            audit_obj[file_name]['numeric_score_audits'].update({\
                                    value["id"]: {
                                        "score": value["score"],
                                        "overallSavingsMs": value["details"]["overallSavingsMs"],
                                        "numericValue": value["numericValue"],
                                        "numericUnit": value["numericUnit"]
                                    }})
                    elif "details" in value and "numericValue" not in value:
                        if "overallSavingsMs" in value["details"]:
                            audit_obj[file_name]['numeric_score_audits'].update({\
                                    value["id"]: {
                                        "score": value["score"],
                                        "overallSavingsMs": value["details"]["overallSavingsMs"]
                                    }})

                    elif "details" not in value and "numericValue" in value:
                        audit_obj[file_name]['numeric_score_audits'].update({\
                                value["id"]: {
                                    "score": value["score"],
                                    "numericValue": value["numericValue"],
                                    "numericUnit": value["numericUnit"]
                                }})
                    else:
                        audit_obj[file_name]['numeric_score_audits'].update({\
                                value["id"]: {
                                    "score": value["score"]
                                }})

                    # if "numericValue" in value:
                    #     audit_obj[file_name]["numeric_score_audits"].update({\
                    #             value["id"]: {
                    #                 "numericValue": value["numericValue"],
                    #                 "numericUnit": value["numericUnit"]
                    #             }})
                                
                elif value["scoreDisplayMode"] == "binary":
                    audit_obj[file_name]['binary_score_audits'].update({\
                            value["id"]: {
                                "score": value["score"]
                            }})
                    if "numericValue" in value:
                        audit_obj[file_name]["numeric_score_audits"].update({\
                                value["id"]: {
                                    "numericValue": value["numericValue"],
                                    "numericUnit": value["numericUnit"]
                                }})
                if value["score"] == None:
                    audit_obj[file_name]["null_score_audits"].append(value["id"])
                    if "numericValue" in value:
                        audit_obj[file_name]["numeric_score_audits"].update({\
                                value["id"]: {
                                    "numericValue": value["numericValue"],
                                    "numericUnit": value["numericUnit"]
                                }})
    return audit_obj


def plotGraph (x, y, title_, xlabel_, ylabel_, name):
    rgb = (random.random(), random.random(), random.random())
    plt.plot(x, y, c=rgb)
    plt.title(title_)
    plt.xlabel(xlabel_)
    plt.ylabel(ylabel_)
    # plt.show()
    plt.savefig(name)

def auditScorevsTime (audits):
    for key, value in audits.items():
        scorePoints = []
        savingsPoints = []
        i = 0
        if i < 10:
            for key2, value2 in value['numeric_score_audits'].items():
                if "overallSavingsMs" in value2:
                    scorePoints.append(value2['score'])
                    savingsPoints.append(value2['overallSavingsMs'])
        else:
            break
        plotGraph(scorePoints, savingsPoints, 'Score vs time_savings', 'score', 'potential saved time in ms', 'score-vs-overallSavingsMs')
        # break
        i += 1
    plt.show()

def specificAuditScoreTrend (auditName, audits):
    scorePoints = []
    count = 0
    for key, value in audits.items():
        if auditName in value['numeric_score_audits']:
            count += 1
            scorePoints.append(value['numeric_score_audits'][auditName]['score'])
    x = []
    for i in range(0, count):
        x.append(i+1)
    plotGraph(x, scorePoints, "Ranking-vs-" + auditName, "Ranking", "Score: " + auditName, "ranking-vs-" + auditName)


def readFile (fileName, websiteType, audits):
    filtered = {
        'e': [],
        'v': [],
        's': []
    }
    with open(fileName, 'r') as fileObj:
        fileObj = csv.reader(fileObj)
        i = 0
        for row in fileObj:
            if i < 200:
                if row[2] == 'e':
                    filtered['e'].append(row[0] + '-' + row[1])
                elif row[2] == 'v':
                    filtered['v'].append(row[0] + '-' + row[1])
                elif row[2] == 's':
                    filtered['s'].append(row[0] + '-' + row[1])
            i += 1
        return filtered
if __name__ == "__main__":
    audits = makeAuditList()
    print(audits['20-netflix.com']["numeric_score_audits"]["first-contentful-paint"])
    # specificAuditScoreTrend("unused-javascript", audits)
    # filtered = readFile("data/categories.csv", 'r', audits)
    # print(audits['01-google.com'])
    # newAudits = {}
    # i = 0
    # for key, value in filtered.items():
    #     print(value)
    #     for website in value:
    #         if i < 50:
    #             newAudits[website] = audits[website]
    #         else:
    #             break
    #     i += 1
    # print(newAudits)
    # print(audits['google']['numeric_score_audits'])
    # auditScorevsTime(audits)
    # print(greatestImpact(audits))
    # print (audits["39-adobe.com"]['numeric_score_audits']["unused-javascript"])