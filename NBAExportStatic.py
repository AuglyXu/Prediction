import pymysql
import csv
connection = pymysql.connect(host='localhost',user='root',password='213xuxianzhe213',db='nba',port=3306,charset='utf8')
cs = connection.cursor()
# 获取表中数据并存入csv
teamPerSqlGet = '''select * from TeamPerGameStats'''
with open("F:/nbaStatCsv/TeamPerGameStats.csv","w",newline="") as fileWriter:
    fw = csv.writer(fileWriter)
    header = ["Rk","Team","G","MP","FG","FGA","FG%"	,"3P","3PA","3P%","2P","2PA","2P%","FT","FTA","FT%","ORB","DRB","TRB","AST","STL","BLK","TOV","PF"	,"PTS"]
    fw.writerow(header)
    cs.execute(teamPerSqlGet)
    rows = cs.fetchall()
    for i in rows:
        fw.writerow(i)

oppoPerSqlGet = '''select * from opponentpergamestats'''
with open("F:/nbaStatCsv/OpponentPerGameStats.csv","w",newline="") as fileWriter:
    fw = csv.writer(fileWriter)
    header = ["Rk","Team","G","MP","FG","FGA","FG%"	,"3P","3PA","3P%","2P","2PA","2P%","FT","FTA","FT%","ORB","DRB","TRB","AST","STL","BLK","TOV","PF"	,"PTS"]
    fw.writerow(header)
    cs.execute(oppoPerSqlGet)
    rows = cs.fetchall()
    for i in rows:
        fw.writerow(i)

miscellPerSqlGet = '''select * from miscellaneousstats'''
with open("F:/nbaStatCsv/MiscellaneousStats.csv","w",newline="") as fileWriter:
    fw = csv.writer(fileWriter)
    header = ["Rk","Team","Age","W","L","PW","PL","MOV","SOS","SRS","ORtg",	"DRtg","NRtg","Pace","FTr",	"3PAr","TS%","eFG%","TOV%","ORB%","FT/FGA","eFG%","TOV%","DRB%","FT/FGA","Arena","Attend.","Attend./G"]
    fw.writerow(header)
    cs.execute(miscellPerSqlGet)
    rows = cs.fetchall()
    for i in rows:
        print(i)
        fw.writerow(i)

lastSeasonResult = '''select * from lastseasonresult'''
with open("F:/nbaStatCsv/17-18result.csv","w",newline="") as fileWriter:
    fw = csv.writer(fileWriter)
    header = ["VTEAM","HTEAM","WTEAM"]
    fw.writerow(header)
    cs.execute(lastSeasonResult)
    rows = cs.fetchall()
    for i in rows:
        print(i)
        fw.writerow(i)

thisSeasonSch = '''select * from thisseasonsch'''
with open("F:/nbaStatCsv/18-19sch.csv","w",newline="") as fileWriter:
    fw = csv.writer(fileWriter)
    header = ["VTEAM","HTEAM"]
    fw.writerow(header)
    cs.execute(thisSeasonSch)
    rows = cs.fetchall()
    for i in rows:
        print(i)
        fw.writerow(i)


