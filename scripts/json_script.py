import json
import os
import matplotlib.pyplot as plt


def makeAuditList ():
    audit_obj = {}
    for file_name in os.listdir("../data/json_files"):
        file_name = file_name.split('.')[0].lower()
        audit_obj[file_name] = {
            "numeric_score_audits": {},
            "binary_score_audits": {},
            "null_score_audits": []
        }
    for file_name in sorted(os.listdir("../data/json_files"), key=lambda x: int(x.partition('-')[0])):
        print(file_name)
        with open("../data/json_files/" + file_name) as json_file:
            file_name = file_name.split('.')[0].lower()
            json_file_obj = json.load(json_file)
            audits = json_file_obj["audits"]
            for key, value in audits.items():
                if value["scoreDisplayMode"] == "numeric":
                    if "details" in value:
                        if "overallSavingsMs" in value["details"]:
                            audit_obj[file_name]['numeric_score_audits'].update({\
                                    value["id"]: {
                                        "score": value["score"],
                                        "overallSavingsMs": value["details"]["overallSavingsMs"]
                                    }})
                    else:
                        audit_obj[file_name]['numeric_score_audits'].update({\
                                value["id"]: {
                                    "score": value["score"]
                                }})
                elif value["scoreDisplayMode"] == "binary":
                    audit_obj[file_name]['binary_score_audits'].update({\
                            value["id"]: {
                                "score": value["score"]
                            }})
                if value["score"] == None:
                    audit_obj[file_name]["null_score_audits"].append(value["id"])
    return audit_obj

def plotGraph (x, y, title_, xlabel_, ylabel_, name):
    plt.plot(x, y, 'o')
    plt.title(title_)
    plt.xlabel(xlabel_)
    plt.ylabel(ylabel_)
    plt.show()
    plt.savefig(name)

def auditScorevsTime (audits):
    scorePoints = []
    savingsPoints = []
    # print(audits)
    for key, value in audits.items():
        for key2, value2 in value['numeric_score_audits'].items():
            if "overallSavingsMs" in value2:
                scorePoints.append(value2['score'])
                savingsPoints.append(value2['overallSavingsMs'])
    plt.plot(scorePoints, savingsPoints, 'o')
    plt.title('Score vs time_savings')
    plt.xlabel('score')
    plt.ylabel('potential saved time in ms')
    plt.show()
    plt.savefig('score-vs-overallSavingsMs')

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


if __name__ == "__main__":
    audits = makeAuditList()
    print(audits['20-netflix'])
    specificAuditScoreTrend("unused-javascript", audits)
    # print(audits['google']['numeric_score_audits'])
    # auditScorevsTime(audits)
    # print(audits)
