import pymysql
import csv
connection = pymysql.connect(host='localhost',user='root',passwd='213xuxianzhe213',db='nba',port=3306,charset='utf8')
cs=connection.cursor()
with open("F:/nbaStatCsv/18-19resultPrediction.csv","r") as fileReader:
    fr = csv.reader(fileReader)
    header = next(fr)
    for row in fr:
        myList = []
        for i in range(len(header)):
            if i == 3:
                myList.append(row[i][:-3])
            elif i == 2:
                myList.append(row[i])
            else:
                myList.append(row[i])
        # print(myList)
        sqlInsert = '''insert into ResultPrediction values(%s,%s,%s)'''
        cs.execute(sqlInsert,myList)
    connection.commit()
connection.close()