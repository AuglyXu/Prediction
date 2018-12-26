# -*- coding:utf-8 -*-
import pandas as pd
import math
import csv
import random
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
# from sklearn.linear_model import stochastic_gradient
base_elo = 1600
team_elos = {}
team_stats = {}
X = []
y = []
rootCsv = 'F:/nbaStatCsv'

# 修改等级分(类似于排位),通过等级分公式计算出球队获胜的概率,等级分越低,当前k值越高,也就是说,段位越低,加的分越高
# 加分的计算公式为 基础等级分 + (差值)*k 值
def calc_elo(win_team, lose_team):
    winner_rank = get_elo(win_team)
    loser_rank = get_elo(lose_team)
    # 计算每个球队的elo值
    rank_diff = winner_rank - loser_rank
    exp = (rank_diff  * -1) / 400
    odds = 1 / (1 + math.pow(10, exp))
    # 根据rank级别修改K值
    if winner_rank < 2100:
        k = 32
    elif winner_rank >= 2100 and winner_rank < 2400:
        k = 24
    else:
        k = 16
    new_winner_rank = round(winner_rank + (k * (1 - odds)))
    new_rank_diff = new_winner_rank - winner_rank
    new_loser_rank = loser_rank - new_rank_diff

    return new_winner_rank, new_loser_rank

# 根据每支队伍的Miscellaneous Opponent，Team统计数据csv文件进行初始化
def initialize_data(Mstat, Ostat, Tstat):
    # drop函数用于过滤不必要的项,加axis表示删除列
    new_Mstat = Mstat.drop(['Rk', 'Arena','Attend.','Attend./G'], axis=1)
    new_Ostat = Ostat.drop(['Rk', 'G', 'MP'], axis=1)
    new_Tstat = Tstat.drop(['Rk', 'G', 'MP'], axis=1)

    # merge用于数据合并(类似于数据库创建视图),按Team键连接,按左连接, new_Mstat取全部，new_Ostat取部分，没有值则用NaN填充
    team_stats1 = pd.merge(new_Mstat, new_Ostat, how='left', on='Team')
    team_stats1 = pd.merge(team_stats1, new_Tstat, how='left', on='Team')

    # 返回头信息
    print(team_stats1.info())
    # 返回 新索引 inplace=False对数据进行修改，创建并返回新的对象承载其修改结果 drop=True：在原有的索引列重置索引，不再另外添加新列
    return team_stats1.set_index('Team', inplace=False, drop=True)

def get_elo(team):
    try:
        return team_elos[team]
    except:
        # 当最初没有elo时，给每个队伍最初赋base_elo
        team_elos[team] = base_elo
        return team_elos[team]

# 建立对应2017~2018年常规赛和季后赛中每场比赛的数据集
def  build_dataSet(all_data):
    print("Building data set..")
    # iterrows返回index row的元组
    for index, row in all_data.iterrows():
        Wteam = row['VTEAM']
        Lteam = row['HTEAM']
        # 获取最初的elo或是每个队伍最初的elo值
        team1_elo = get_elo(Wteam)
        team2_elo = get_elo(Lteam)

        # 给主场比赛的队伍加上100的elo值
        if row['WTEAM'] == 'W':
            team1_elo += 100
        else:
            team2_elo += 100

        # 把elo当为评价每个队伍的第一个特征值
        team1_features = [team1_elo]
        team2_features = [team2_elo]

        # 添加从basketball reference.com获得的每个队伍的统计信息
        # iteritems是把python字典数据按迭代器的实验返回,提供一个指针,好处是可以遍历复杂数据类型
        for key, value in team_stats.loc[Wteam].iteritems():
            team1_features.append(value)
        for key, value in team_stats.loc[Lteam].iteritems():
            team2_features.append(value)

        # 将两支队伍的特征值随机的分配在每场比赛数据的左右两侧
        # 并将对应的0/1赋给y值
        if random.random() > 0.5:
            X.append(team1_features + team2_features)
            y.append(0)
        else:
            X.append(team2_features + team1_features)
            y.append(1)

        # 根据这场比赛的数据更新队伍的elo值
        new_winner_rank, new_loser_rank = calc_elo(Wteam, Lteam)
        team_elos[Wteam] = new_winner_rank
        team_elos[Lteam] = new_loser_rank
    # 返回nan_to_num操作过的类数组
    return np.nan_to_num(X), np.array(y)

def predict_winner(team_1, team_2, model):
    features = []

    # team 1，客场队伍
    features.append(get_elo(team_1))
    # iteritems是把python字典数据按迭代器的实验返回,提供一个指针,好处是可以遍历复杂数据类型
    for key, value in team_stats.loc[team_1].iteritems():
        features.append(value)

    # team 2，主场队伍
    features.append(get_elo(team_2) + 100)
    for key, value in team_stats.loc[team_2].iteritems():
        features.append(value)

    features = np.nan_to_num(features)
    # 返回的是一个n行k列的数组，第i行第j列上的数值是模型预测第i个预测样本的标签为j的概率
    return model.predict_proba([features])

# 在main函数中调用这些数据处理函数，使用sklearn的Logistic Regression方法建立回归模型：
if __name__ == '__main__':
    # 需要爬数据的部分
    # 1.1 从网页中爬取csv展示的数据存储到csv中
    # 1.2 将爬取的数据存储到数据库中
    Mstat = pd.read_csv(rootCsv + '/MiscellaneousStats.csv')
    # 所遇到的对手平均每场比赛的统计信息，所包含的统计数据与Team Per Game Stats中的一致，只是代表的该球队对应的对手的
    Ostat = pd.read_csv(rootCsv + '/OpponentPerGameStats.csv')
    # 每支队伍平均每场比赛的表现统计
    Tstat = pd.read_csv(rootCsv + '/TeamPerGameStats.csv')

    team_stats = initialize_data(Mstat, Ostat, Tstat)

    result_data = pd.read_csv(rootCsv + '/17-18result.csv')
    X, y = build_dataSet(result_data)
    # 训练网络模型
    # print("Fitting on %d game samples.." % len(X))

    # 线性回归
    model = LogisticRegression()
    # model = stochastic_gradient.SGDClassifier()
    # 接收两个类数组进行模型的回归计算
    # 这是训练过的模型,返回模型自身
    model.fit(X, y)

    # # 利用10折交叉验证计算训练正确率
    print("Doing cross-validation..")
    print(cross_val_score(model, X, y, cv = 10, scoring='accuracy', n_jobs=-1).mean())

    # 利用训练好的model在18-19年的比赛中进行预测
    print('Predicting on new schedule..')
    schedule1819 = pd.read_csv(rootCsv + '/18-19sch.csv')
    result = []
    for index, row in schedule1819.iterrows():
        team1 = row['VTEAM']
        team2 = row['HTEAM']
        pred = predict_winner(team1, team2, model)
        prob = pred[0][0]
        if prob > 0.5:
            winner = team1
            loser = team2
            result.append([winner, loser, prob])
        else:
            winner = team2
            loser = team1
            result.append([winner, loser, 1 - prob])

    with open('F:/nbaStatCsv/18-19resultPrediction.csv', 'w',newline="") as f:
        writer = csv.writer(f)
        writer.writerow(['win', 'lose', 'probability'])
        writer.writerows(result)
