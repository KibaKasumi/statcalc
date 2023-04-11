import csv
import time
import os

Path="./statistics/"
daysPeriod=90

fileList = os.listdir(Path)
for i in fileList:
    if i.endswith(".csv"):
        with open(Path + i, "r", newline='') as inputcsv:
            reader = csv.DictReader(inputcsv, delimiter=';')
            checkCountY=0
            currentDate=["00.00.0000"]*daysPeriod
            tempTime=1672531200 #01.01.2023 utime
            #tempTime=1640995200 #01.01.2022 utime, 86400
            for yday in range(daysPeriod):
                currentDate[yday]=time.strftime('%d.%m.%Y', time.gmtime(tempTime))
                tempTime+=86400
            payCash=[0]*daysPeriod
            payCards=[0]*daysPeriod
            checkCount=[0]*daysPeriod
            for row in reader:  #1 строка - 1 транзкация
                #print(row)
                rowDate = time.strptime(row['Date'], '%d.%m.%Y')
                if rowDate[0]==2023: # and rowDate[1]==2: #проверка на год
                    yday=rowDate[7]-1
                    currentDate[yday]=row['Date']
                    payCash[yday]+=int(row['Cash'])
                    payCards[yday]+=int(row['Cards'])
                    checkCount[yday]+=1 #здесь считаю уже не купюры а сессии
                    checkCountY+=1

            if checkCountY>0:
                with open(Path + "bydays_"+i, "w", newline='') as outcsv:
                    writer = csv.writer(outcsv, delimiter=';')
                    writer.writerow(['Дата', 'Терминал', 'Чеков', 'Наличными', 'Картой'])
                    for yday in range(daysPeriod):
                        writer.writerow([currentDate[yday], i, checkCount[yday], payCash[yday], payCards[yday]])
                    print(i, " complete!", checkCountY)
