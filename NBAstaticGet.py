import requests
import lxml.html
etree = lxml.html.etree
import time
import pymysql
connection = pymysql.connect(host='localhost',user='root',password='213xuxianzhe213',db='nba',port=3306,charset='utf8')
cs = connection.cursor()

headers = {
    'User-Agent':'"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"',
    'Content-Type': 'text/plain',
    'Origin': 'https://www.basketball-reference.com',
    'Referer': 'https://www.basketball-reference.com/leagues/NBA_2019.html'
}

url = 'https://www.basketball-reference.com/leagues/NBA_2019.html'
data = requests.get(url,headers=headers).text
data_new = data.replace('<!--',' ')
data_new2 = data_new.replace('-->',' ')
allSta = etree.HTML(data_new2)
teamPerGameStat = allSta.xpath('//*[@id="team-stats-per_game"]/tbody/tr')
oppoPerGameStat = allSta.xpath('//*[@id="opponent-stats-per_game"]/tbody/tr')
miscellaneousStat = allSta.xpath('//*[@id="div_misc_stats"]//tbody/tr')
time.sleep(3)
# 导入自己队伍的数据
for tr in teamPerGameStat:
    # 将数据插入到List中
    myList = []
    # 输出表中一列的数据
    for td in tr:
        stat = td.xpath('./text()')
        if len(stat) == 0:
            teamName = td.xpath('./a/text()')[0]
            myList.append(teamName)
        else:
            myList.append(stat[0])
        # print(myList)
    sqInsert = '''insert into TeamPerGameStats values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    cs.execute(sqInsert, myList)
    connection.commit()
# 导入对手的数据
for tr in oppoPerGameStat:
    # 将数据插入到List中
    myList = []
    # 输出表中一列的数据
    for td in tr:
        stat = td.xpath('./text()')
        if len(stat) == 0:
            teamName = td.xpath('./a/text()')[0]
            myList.append(teamName)
        else:
            myList.append(stat[0])
        # print(myList)
    sqInsert = '''insert into OpponentPerGameStats values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    cs.execute(sqInsert, myList)
    connection.commit()

# 导入其他复杂数据
for tr in miscellaneousStat:
    # 将数据插入到List中
    myList = []
    # 输出表中一列的数据
    for td in tr:
        stat = td.xpath('./text()')
        if len(stat) == 0:
            teamName = td.xpath('./a/text()')[0]
            myList.append(teamName)
        else:
            myList.append(str(stat[0]))
        # print(myList)
    sqInsert = '''insert into MiscellaneousStats values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    cs.execute(sqInsert, myList)
    connection.commit()

# 导入主客队和获胜球队
month = ['october','november','december','january','february','march']
for i in range(0, len(month)):
    url2 = 'https://www.basketball-reference.com/leagues/NBA_2018_games-{}.html'.format(month[i])
    data = requests.get(url2,headers=headers).text
    data_new = data.replace('<!--',' ')
    data_new2 = data_new.replace('-->',' ')
    allSta = etree.HTML(data_new2)
    schedule = allSta.xpath('//*[@id="schedule"]/tbody/tr')
    for tr in schedule:
        myList = []
        # 输出表中一列的数据
        new_tr_vis = tr.xpath('./*[@data-stat="visitor_team_name"]')
        new_tr_home = tr.xpath('./*[@data-stat="home_team_name"]')
        new_tr_visitor_pts = tr.xpath('./*[@data-stat="visitor_pts"]')
        new_tr_home_pts = tr.xpath('./*[@data-stat="home_pts"]')
        # 爬客队
        for td in new_tr_vis:
            visitorName = td.xpath('./a/text()')
            myList.append(visitorName[0])
        #  爬客队成绩
        for td in new_tr_visitor_pts:
            visitor_pts = td.xpath('./text()')
            myList.append(visitor_pts[0])
        # 爬主队
        for td in new_tr_home:
            homeName = td.xpath('./a/text()')
            myList.append(homeName[0])
        # 爬主队成绩
        for td in new_tr_home_pts:
            home_pts = td.xpath('./text()')
            myList.append(home_pts[0])
        if myList[1] < myList[3]:
            str = 'W'
            myList.pop(1)
            myList.pop(2)
            myList.append(str)
        elif myList[1] > myList[3]:
            str = 'V'
            myList.pop(1)
            myList.pop(2)
            myList.append(str)
        # print(myList)
        sqInsert = '''insert into LastSeasonResult values (%s,%s,%s)'''
        cs.execute(sqInsert,myList)
        connection.commit()

#  爬18-19赛季赛程表
    url3 = 'https://www.basketball-reference.com/leagues/NBA_2019_games-{}.html'.format(month[i])
    data = requests.get(url3,headers=headers).text
    data_new = data.replace('<!--',' ')
    data_new2 = data_new.replace('-->',' ')
    allSta = etree.HTML(data_new2)
    schedule = allSta.xpath('//*[@id="schedule"]/tbody/tr')
    for tr in schedule:
        myList = []
        # 输出表中一列的数据
        new_tr_vis = tr.xpath('./*[@data-stat="visitor_team_name"]')
        new_tr_home = tr.xpath('./*[@data-stat="home_team_name"]')
        new_tr_visitor_pts = tr.xpath('./*[@data-stat="visitor_pts"]')
        new_tr_home_pts = tr.xpath('./*[@data-stat="home_pts"]')
        # 爬客队
        for td in new_tr_vis:
            visitorName = td.xpath('./a/text()')
            myList.append(visitorName[0])
        # 爬主队
        for td in new_tr_home:
            homeName = td.xpath('./a/text()')
            myList.append(homeName[0])
        # print(myList)
        sqInsert = '''insert into thisseasonsch values (%s,%s)'''
        cs.execute(sqInsert,myList)
        connection.commit()
connection.close()