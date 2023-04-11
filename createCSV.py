'''
Делаю .csv список из .json по нужному час.поясу + корректирую задвоение записаей
'''
import csv
import time
import os
import json

os.environ['TZ'] = 'Asia/Barnaul'
time.tzset()

Path="./statistics/"

dirList = os.listdir(Path) #список файлов в папке в массив
for d in dirList:
    if not d.endswith(".csv"):
        with open(Path+d+'_list.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            serviceCount = 0
            writer.writerow(['Date', 'Time', 'UTC', 'Terminal', 'Checks', 'Cash', 'Cards', 'Spend'])
            fileList = os.listdir(Path + d + "/sessions/")
            correctCount=0
            correctSumm=0
            for i in fileList:
                filePath = Path + d + "/sessions/" + i
                fileStats = os.stat(filePath)
                ctime = fileStats.st_ctime
                fTime = i.split(".")
                fTimeInt = int(fTime[0])
                fTimeFloat = float(fTime[0]) #парсит время
                #fileTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fTimeInt))
                fileDate=time.localtime(fTimeFloat)
                if fileDate[0]==2023:
                    strTime = time.strftime('%H:%M:%S', fileDate)
                    strDate = time.strftime('%d.%m.%Y', fileDate) #строка с датой платежа
                    #print(filePath)
                    try:
                        with open(filePath) as json_file:   #читаем файл как json
                            data = json.load(json_file)
                            try:
                                payCash=0
                                payCards=0
                                checkCount=0
                                spendMoney=0
                                payData = data["pays"]
                                progData = data["programs"]

                                for i in payData:
                                    #print(i)
                                    if i["type"] == "term":
                                        payCards += int(i["count"])
                                    if i["type"] == "cash":
                                        payCash += int(i["count"])
                                    checkCount+=1

                                for i in progData:
                                    #print(i)
                                    spendMoney+=i["spend-money"]

                                Rest=payCash+payCards-spendMoney
                                k=spendMoney / (payCash+payCards)

                                if (k < 0.9 or k > 1.05) and spendMoney>0: #коррекция бага с акцией
                                    payCards = payCards//2
                                    payCash = payCash//2
                                    checkCount = checkCount//2
                                    correctCount+=1
                                    correctSumm+=payCash+payCards

                                writer.writerow([strDate, strTime, fTimeInt, d, checkCount, payCash, payCards, spendMoney])

                            except:
                                #print(filePath + " нет данных!")
                                serviceCount += 1
                    except:
                        print(filePath, " Error")
            print(d, " service =", serviceCount, correctCount, correctSumm)
