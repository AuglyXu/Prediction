# Prediction
一个最简单的回归模型的训练和NBA比赛结果的预测\n
1.从https://www.basketball-reference.com/上爬取数据并写入数据库(NBAstaticGet.py)
2.从数据库将数据写入CSV文件进行操作(NBAExportStatic.py)
3.处理数据并将预测好的结果写入CSV文件(NBAPrediction和nbaCsvToMySQL.py)
4.在web上简单展示
