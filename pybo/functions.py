
import json

from sqlalchemy import func


def predict_price(filepath, column):
    meat_sum = 0
    with open(filepath, 'r') as file:
        data = json.load(file)

    for i in range(7):
        meat_sum += data[i][column]
    meat_price = int(meat_sum/7)
    return meat_price


# 조류독감 밯병 갯수
def GetAiCnt(model):
    data = model.query.filter(model.date >= func.ADDDATE(func.NOW(), -30)).filter(model.ds_nm.like('고병원성%')).count()
    
    return data

# 조류독감 발병현황
def GetAiData(model):
    data = model.query.filter(model.ds_nm.like('고병원성%')).filter(model.date >= func.ADDDATE(func.NOW(), -30)).order_by(model.date.desc()).limit(5)
    return data

# 소, 돼지 발병 갯수
def GetCnt(model, keyword):
    data = model.query.filter(model.date >= func.ADDDATE(func.NOW(), -30)).filter(model.animal.like(f'{keyword}%')).count()
    
    return data

# 소, 돼지 발병현황
def GetData(model, keyword):
    data = model.query.filter(model.animal.like(f'{keyword}%')).filter(model.date >= func.ADDDATE(func.NOW(), -30)).order_by(model.date.desc()).limit(5)
    return data

# 닭고기 가격 테이블
def predict_price_all(filepath, column):
    meat_sum = []
    meat_list = []
    meat_avg = 0

    with open(filepath, 'r') as file:
        data = json.load(file)

    for i in range(28):
        if column == 'p5_6':
            meat_sum.append(data[i][column])
            meat_avg += meat_sum[i]

            if (i+1) % 7 == 0:
                meat_avg = int(meat_avg/7)
                meat_list.append(format(meat_avg, ',d'))
                meat_avg = 0
        
        if column == 'p7_8':
            meat_sum.append(data[i][column])
            meat_avg += meat_sum[i]

            if (i+1) % 7 == 0:
                meat_avg = int(meat_avg/7)
                meat_list.append(format(meat_avg, ',d'))
                meat_avg = 0

        if column == 'p9_10':
            meat_sum.append(data[i][column])
            meat_avg += meat_sum[i]

            if (i+1) % 7 == 0:
                meat_avg = int(meat_avg/7)
                meat_list.append(format(meat_avg, ',d'))
                meat_avg = 0

        if column == 'p11':
            meat_sum.append(data[i][column])
            meat_avg += meat_sum[i]

            if (i+1) % 7 == 0:
                meat_avg = int(meat_avg/7)
                meat_list.append(format(meat_avg, ',d'))
                meat_avg = 0

        if column == 'p12':
            meat_sum.append(data[i][column])
            meat_avg += meat_sum[i]

            if (i+1) % 7 == 0:
                meat_avg = int(meat_avg/7)
                meat_list.append(format(meat_avg, ',d'))
                meat_avg = 0

        if column == 'p13_16':
            meat_sum.append(data[i][column])
            meat_avg += meat_sum[i]

            if (i+1) % 7 == 0:
                meat_avg = int(meat_avg/7)
                meat_list.append(format(meat_avg, ',d'))
                meat_avg = 0

        if column == 'yhat':
            meat_sum.append(data[i][column])
            meat_avg += meat_sum[i]

            if (i+1) % 7 == 0:
                meat_avg = int(meat_avg/7)
                meat_list.append(format(meat_avg, ',d'))
                meat_avg = 0
    return meat_list