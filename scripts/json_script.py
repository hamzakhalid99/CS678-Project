import json
import os
import csv
import matplotlib.pyplot as plt
import random
import pprint
import numpy as np

def makeAuditList ():
    '''
    MAKES THE AUDIT DICTIONARY
    '''
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
        for key2, value2 in value['numeric_score_audits'].items():
            if "overallSavingsMs" in value2:
                scorePoints.append(value2['score'])
                savingsPoints.append(value2['overallSavingsMs'])
    plotGraph(scorePoints, savingsPoints, 'Score vs time_savings', 'score', 'potential saved time in ms', 'score-vs-overallSavingsMs')

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

def scoreList_MetricNumericVals (auditName, metric, numeric_or_binary):
    scores = {}
    numericValues = []
    
    performanceScoreMakers = ['first-contentful-paint', 'largest-contentful-paint', 'speed-index', 'total-blocking-time', 'time-to-interactive', 'cummulative-layout-shift']
    for websites, websiteData in audits.items():
        for valueTypes, valueData in websiteData.items():
            if valueTypes == 'numeric_score_audits' or valueTypes == numeric_or_binary +'_score_audits':
                for metricInJson, metricData in valueData.items():
                    if 'score' in metricData and valueData not in performanceScoreMakers:
                        scores[metricInJson] = []
                    if metricInJson == metric:
                        numericValues.append(metricData['numericValue'])

 
    for key, value in audits.items():
        for key2, value2 in value[numeric_or_binary + '_score_audits'].items():
            if 'score' in value2 and key2 not in performanceScoreMakers:
                scores[key2].append(value2['score'])
            else:
                pass
    return scores, numericValues


    # FINDING PLOTS AND GRADIENTS FOR NUMERIC SCORES AND DATA FOR GRADIENTS
def overallNumericMetricAnalysis (audits, metric, top_n): #top_n = top (most steep) gradients to return 
    scores, numericValues = scoreList_MetricNumericVals(audits, metric, 'numeric')
    performanceScoreMakers = ['first-contentful-paint', 'largest-contentful-paint', 'speed-index', 'total-blocking-time', 'time-to-interactive', 'cummulative-layout-shift']
    # print(scores, numericValues)
    gradients = {}
    top_n_gradients = {}

    for key, value in audits.items():
        for key2, value2 in value['numeric_score_audits'].items():
            try:
                # plotGraph(scores[key2], numericValues, metric + " numeric Value vs diagnostic results scores", 'score' ,  metric \
                    # + " numeric Values", 'effect of different diagnostics on ' + metric)
                gradients = gradientCalculator(gradients, key2, scores[key2], numericValues)                
            except:
                pass
    # plt.savefig('plot_overall')
    gradients = dict(sorted(gradients.items(), key=lambda item: item[1])) #sorts dictionary by value
    top_n_counter = 0
    for key, value in gradients.items():
        if top_n_counter > top_n:
            return top_n_gradients
        else:
            top_n_gradients[key] = value
            top_n_counter += 1
    return top_n_gradients


def gradientCalculator (dictionary, metric, x,y):
    x = np.array(x)
    y = np.array(y)
    gradient, _ = np.polyfit(x, y, 1)
    dictionary[metric] = gradient
    return dictionary


def readWriteJson (file_name, mode, fileToWrite):
    '''
    FILE_NAME: FILE TO OPEN TO READ, OR TO WRITE TO
    FILETOWRITE: ONLY USED WHEN WRITING, WHEN READING IT MUST BE NONE
    MODE: W OR R
    '''
    with open (file_name, mode) as json_file:
        if mode == 'r':
            return json.load(json_file)
        elif mode == 'w':
            json.dump(fileToWrite, json_file)

def barPlot (gradients, figName):
    x_axis = []
    y_axis = []
    for key, value in gradients.items():
        x_axis.append(key)
        y_axis.append(value)

    plt.figure(figsize=(20, 6))
    # ax = fig.add_axes([0,0,1,1])
    plt.bar(x_axis, y_axis)
    # ax.bar(x_axis, y_axis)
    plt.xlabel('Metrics')
    plt.ylabel('gradients (Time Savings in Ms (numeric value) / score)')
    plt.title('Top 10 metrics ranked according to gradients (Time Savings in Ms (numeric value) / score) for the performance metric ' + figName)
    # plt.show()
    plt.savefig(figName)

def imageAnalysis (audits, metric):
    #implemented for metric: offscreen-images
    overall_savings = {}
    time_to_interactive = {}
    percent_impact = {}
    lists_values = []
    for key, value in audits.items():
        for key2, value2 in value['numeric_score_audits'].items():
            if key2 == 'offscreen-images':
                overall_savings[key]= value2['overallSavingsMs']
                # return
            elif key2 == 'interactive':
                time_to_interactive[key] = value2['numericValue']
                # break
    
    for key, value in time_to_interactive.items():
        difference = time_to_interactive[key] - overall_savings[key]     #new time after fixing this metric
        percentage_difference = ((time_to_interactive[key] / difference) * 100) - 100  # (old/new)*100 -> shows the percentage impact of this metric
        percent_impact[key] = percentage_difference
        lists_values = percentage_difference
    
    x_axis = list(range(1, 51))
    y_axis = lists_values

    rgb = (random.random(), random.random(), random.random())
    plt.plot(x_axis, y_axis, c=rgb)
    plt.title("percentage effect of off-screen images on top n websites")
    plt.xlabel("Rank of wesbite")
    # plt.set_label(legend_)
    plt.ylabel(ylabel_)


    return percent_impact

def overallBinaryMetricAnalysis (audits, metric): 
    scores, numericValues = scoreList_MetricNumericVals(audits, metric, 'numeric')
    performanceScoreMakers = ['first-contentful-paint', 'largest-contentful-paint', 'speed-index', 'total-blocking-time', 'time-to-interactive', 'cummulative-layout-shift']
    print(scores, numericValues)

if __name__ == "__main__":
    audits = readWriteJson('audits.json', 'r', None)
    # performanceScoreMakers = ['first-contentful-paint', 'largest-contentful-paint', 'speed-index', 'total-blocking-time', 'time-to-interactive', 'cummulative-layout-shift']

    imageAnalysis(audits, 'offscreen-images')
    
    '''
        BINARY METRIC ANALYSIS

    '''
    # overallBinaryMetricAnalysis(audits, 'largest-contentful-paint')






    
        # CODE TO MAKE BAR PLOTS AND JSON FILES OF GRADIENTS

    # for analysisMetric in performanceScoreMakers:
    #     top_ten_gradients = overallNumericMetricAnalysis(audits, analysisMetric, 10)
    #     # print("keys:", top_ten_gradients.keys())
    #     barPlot(top_ten_gradients, analysisMetric)
    #     readWriteJson('Top10-' + analysisMetric + '.json', 'w', top_ten_gradients)

    




    # print(top_ten_gradients)
    # specificAuditScoreTrend("unused-css-rules", audits)
    # auditScorevsTime(audits)
    # performanceMetricAnalysis (audits, 'unused-javascript', "largest-contentful-paint")
    # performanceMetricAnalysis (audits, 'unused-css-rules', "largest-contentful-paint")
    # performanceMetricAnalysis (audits, 'unused-css-rules', "first-contentful-paint")
# top 10 steepest negative gradient: 

# {'legacy-javascript': -14043.578622601302, 'largest-contentful-paint': -11221.938893915014, 'uses-rel-preload': -8842.824150138487, 'uses-text-compression': -8828.938928514646, 'uses-rel-preconnect': -8315.192135421938, 'speed-index': -8053.583359710491, 'first-cpu-idle': -7681.1980949724275, 'interactive': -7615.4962044971535, 'first-contentful-paint': -7516.682157360925, 'first-meaningful-paint': -7338.075874881044, 'uses-responsive-images': -6131.695812780516}
