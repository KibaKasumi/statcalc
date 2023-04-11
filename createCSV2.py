'''
Делаю .csv список из .json по нужному час.поясу + корректирую задвоение записаей
'''
import csv
import time
import os
import json

def calculate_rest(payCards, payCash, checkCount, spendMoney):
#Функция для корекции баага с акцией
    Rest = payCash + payCards - spendMoney
    k = spendMoney / (payCash + payCards)

    if (k < 0.9 or k > 1.05) and spendMoney > 0:
        payCards = payCards // 2
        payCash = payCash // 2
        checkCount = checkCount // 2

    return [payCards, payCash, checkCount]

def process_data(payData, progData):
#Функция подчсета платежей и трат за сеанс
    payCards = 0
    payCash = 0
    checkCount = 0
    spendMoney = 0

    for i in payData:
        if i["type"] == "term":
            payCards += int(i["count"])
        if i["type"] == "cash":
            payCash += int(i["count"])
        checkCount += 1

    for i in progData:
        spendMoney += i["spend-money"]

    return [payCards, payCash, checkCount, spendMoney]


#Непостредственно задаем местный часовой пояс
os.environ['TZ'] = 'Asia/Barnaul'
time.tzset()

Path="./statistics/" #рабочая папка

dirList = os.listdir(Path) #список файлов в папке в массив
for d in dirList:
    if not d.endswith(".csv"): #Проверка типа файла чтобы не открывать свои же .csv
        with open(Path+d+'_list.csv', 'w', newline='') as csvfile: #Создать рабочий .csv
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['Date', 'Time', 'UTC', 'Terminal', 'Checks', 'Cash', 'Cards', 'Spend']) #Записать заголовок
            fileList = os.listdir(Path + d + "/sessions/") #Перейти в папку с исходными .json
            serviceCount = 0 #Обнулить счетчики
            correctCount=0
            correctSumm=0
            for i in fileList: #Проход по всем файлам в папке. Извлекаем время из названия
                filePath = Path + d + "/sessions/" + i
                fileStats = os.stat(filePath)
                ctime = fileStats.st_ctime
                fTime = i.split(".")
                fTimeInt = int(fTime[0])  #парсит время
                fTimeFloat = float(fTime[0])
                #fileTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fTimeInt))
                fileDate=time.localtime(fTimeFloat) #Получаем кортеж даты из UNIX time файла
                if fileDate[0]==2023:   #Проверка года чтобы далее в файл не попала лишняя запись
                    strTime = time.strftime('%H:%M:%S', fileDate) #строка со временем платежа
                    strDate = time.strftime('%d.%m.%Y', fileDate) #строка с датой платежа
                    #print(filePath)
                    try:
                        with open(filePath) as json_file:   #читаем файл как json если его возможно открыть
                            data = json.load(json_file)
                            payData = data["pays"]
                            progData = data["programs"]

                            result = process_data(payData, progData)

                            #result2 = calculate_rest(result)

                            payCards = result[0]
                            payCash = result[1]
                            checkCount = result[2]
                            spendMoney = result[3]

                            correctCount+=checkCount
                            correctSumm+=payCards+payCash

                            writer.writerow([strDate, strTime, fTimeInt, d, checkCount, payCash, payCards, spendMoney])


                    except:
                        print(filePath, " Error") #если файл не читается как json
            #Вывод отчета работы программы. Число сервисных чеков; Исправлено чеков, на сумму
            print(d, " service =", serviceCount, correctCount, correctSumm)
