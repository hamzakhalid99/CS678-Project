import json
import os
import csv
import matplotlib.pyplot as plt
import random
import pprint
import numpy as np

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
        "null": [] -> {}
    }
}
'''



#not being used
def greatestImpact(audits, metricOne, metricTwo):
    # print(audits)
    impact = {}
    for website, scores_dict in audits.items(): #scores_dict is the dictionary of scores.
        numeric_scores = scores_dict["numeric_score_audits"]
        binary_scores = scores_dict["binary_score_audits"]
        null_scores = scores_dict["null_score_audits"]
        impact[website] = {} 
        for  metric, details in numeric_scores.items(): #metric is what is being scored (e.g. unused-javascript), while details include scoring detailsm overall savings etc. 
            try:
                impact[website][metric] = [details["score"], details["overallSavingsMs"], details["numericValue"], details["numericUnit"]]   #format: website -> [score, savings]
            except:
                pass
        for  metric, details in binary_scores.items(): #metric is what is being scored (e.g. unused-javascript), while details include scoring detailsm overall savings etc. 
            # print("here", metric)
            try:
                impact[website][metric] = [details["score"], details["overallSavingsMs"], details["numericValue"], details["numericUnit"]]   #format: website -> [score, savings]
            except:
                pass
        for  metric, details in null_scores.items(): #metric is what is being scored (e.g. unused-javascript), while details include scoring detailsm overall savings etc. 
            try:
                impact[website][metric] = [details["score"], details["overallSavingsMs"], details["numericValue"], details["numericUnit"]]   #format: website -> [score, savings]
            except:
                pass
    # print(impact["20-netflix.com"]["unused-javascript"])
    
    metricOneValues = []
    metricTwoValues = []

    for website, metric in impact.items():
        # print (metric)
        for key, val in metric.items():
            if key == metricOne:
                metricOneValues.append(impact[website][key][2])

            elif key == metricTwo:
                metricTwoValues.append(impact[website][key][2])
    
    # print (metricOneValues, metricTwoValues)

    y_axis = list(range(1,len(metricOneValues)+1))

    plotGraph (y_axis, metricOneValues, metricOne+" vs "+metricTwo, "Rank of website", "Average savings", metricOne+"_vs_"+metricTwo)
    plotGraph (y_axis, metricTwoValues, metricOne+" vs "+metricTwo, "Rank of website", "Average savings", metricOne+"_vs_"+metricTwo)
    # plt.show()

def makeAuditList ():
    audit_obj = {}
    for file_name in os.listdir("../data/json_files"):
        file_name = file_name[:-5].lower()
        audit_obj[file_name] = {
            "numeric_score_audits": {},
            "binary_score_audits": {},
            "null_score_audits": {}
        }
    for file_name in sorted(os.listdir("../data/json_files"), key=lambda x: int(x.partition('-')[0])):
        with open("../data/json_files/" + file_name) as json_file:
            # file_name = file_name.split('.')[0].lower()
            file_name = file_name[:-5].lower()
            json_file_obj = json.load(json_file)
            audits = json_file_obj["audits"]
            # print(audits['largest-contentful-paint'])
            for key, value in audits.items():
                # if key == 'largest-contentful-paint':
                #     print(file_name)
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

                    elif "details" not in value and ("numericValue" in value):
                        # print('here')
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
                                
                elif value["scoreDisplayMode"] == "binary":
                    if "numericValue" in value:
                        audit_obj[file_name]['binary_score_audits'].update({\
                                value["id"]: {
                                    "score": value["score"],
                                    "numericValue": value["numericValue"],
                                    "numericUnit": value["numericUnit"]
                                }})
                    else:
                        audit_obj[file_name]["binary_score_audits"].update({\
                                value["id"]: {
                                    "score": value["score"],
                                }})

                elif value["score"] == None:
                    if "numericValue" in value:
                        audit_obj[file_name]['null_score_audits'].update({\
                                value["id"]: {
                                    "score": value["score"],
                                    "numericValue": value["numericValue"],
                                    "numericUnit": value["numericUnit"]
                                }})

                    else:
                        audit_obj[file_name]["null_score_audits"].update({\
                                value["id"]: {
                                    "score": value["score"]
                                }})
    return audit_obj



def auditScorevsTime (audits):
    for key, value in audits.items():
        scorePoints = []
        savingsPoints = []
        # i = 0
        # if i < 10:
        for key2, value2 in value['numeric_score_audits'].items():
            if "overallSavingsMs" in value2:
                scorePoints.append(value2['score'])
                savingsPoints.append(value2['overallSavingsMs'])
        # else:
        #     break
        # break
        # i += 1
    plotGraph(scorePoints, savingsPoints, 'Score vs time_savings', 'score', 'potential saved time in ms', 'score-vs-overallSavingsMs')
    # plt.show()

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



#not being used
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


def performanceMetricAnalysis (audits, metricOne, metricTwo):
    metricOneNumericVals = []
    metricOneScores = []
    metricTwoNumericVals = []
    metricTwoSCores = []
    for key, value in audits.items():
        for key2, value2 in value['numeric_score_audits'].items():
            if key2 == metricTwo:
                if 'score' in value2:
                    metricTwoSCores.append(value2['score'])
                if 'numericValue' in value2:
                    metricTwoNumericVals.append(value2['numericValue'])
            if key2 == metricOne:
                if 'score' in value2:
                    metricOneScores.append(value2['score'])
                if 'numericValue' in value2:
                    metricOneNumericVals.append(value2['numericValue'])
    plotGraph(metricOneScores, metricTwoNumericVals, metricOne + " score vs " + metricTwo + " numeric Value", metricOne + " scores", metricTwo + ' numericValue', metricOne + " score vs " + metricTwo + " numeric Value")

def plotGraph (x, y, title_, xlabel_, ylabel_, name):
    rgb = (random.random(), random.random(), random.random())
    x = np.array(x)
    y = np.array(y)
    m, b = np.polyfit(x, y, 1)
    plt.plot(x, m*x + b, c=rgb)
    plt.title(title_)
    plt.xlabel(xlabel_)
    # plt.set_label(legend_)
    plt.ylabel(ylabel_)
    # plt.legend()
    # plt.savefig(name)
    # plt.show()

def overallMetricAnalysis (audits, metric):
    scores = {}
    numericValues = []
    for key, value in audits.items():
        for key2, value2 in value['numeric_score_audits'].items():
            if 'score' in value2:
                scores[key2] = []
            if key2 == metric:
                numericValues.append(value2['numericValue'])

    for key, value in audits.items():
        for key2, value2 in value['numeric_score_audits'].items():
            if 'score' in value2:
                scores[key2].append(value2['score'])
            else:
                # print(key)
                pass

    # print(len(scores['preload-lcp-image']))
    for key, value in audits.items():
        for key2, value2 in value['numeric_score_audits'].items():
            # if len(numericValues) != len(scores[key2]):
            #     print(key2, key)
            # print()
            try:
                plotGraph(scores[key2], numericValues, metric + " numeric Value vs diagnostic results scores", 'score' ,  metric \
                    + " numeric Values", 'effect of different diagnostics on ' + metric)
                
                gradient = gradientCalculator(scores[key2], numericValues)
                print(gradient)
                print()
                
            except:
                # print('here')
                pass
                # print(key2, key)
            # pass
    # plt.legend()
    # plt.show()
    plt.savefig('plot_overall')
    # print(scores)

def gradientCalculator (x,y):
    x = np.array(x)
    y = np.array(y)
    gradient, _ = np.polyfit(x, y, 1)
    return gradient




if __name__ == "__main__":
    audits = makeAuditList()        
    # performanceMetricAnalysis (audits, 'unused-javascript', "largest-contentful-paint")
    # performanceMetricAnalysis (audits, 'unused-css-rules', "largest-contentful-paint")
    # performanceMetricAnalysis (audits, 'unused-css-rules', "first-contentful-paint")
    # print(audits)
    overallMetricAnalysis(audits, 'largest-contentful-paint')
    # specificAuditScoreTrend("unused-css-rules", audits)
    # auditScorevsTime(audits)
