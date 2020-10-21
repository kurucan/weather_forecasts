import pymongo
import pandas as pd
import re
from numpy import genfromtxt
from sqlalchemy import create_engine


cl = pymongo.MongoClient('localhost',27017)
db = cl['forecasts']
meteologica = db['meteologica']
meteomatics = db['meteomatics']

print('mongo ready')
d = meteologica.find()
#{'date':r'/2020-09-23'})
dates = []
while True:
    cond = input('Do you want to exit? If no press no. ')
    if cond == 'no':
    	break
    y = input('Year:')
    m = input('Month: ')
    d = input('Day: ')
    dates.append([y,m,d])
	
	
dates = [['2020','09','23'],['2020','10','01'],['2020','10','16'],['2020','10','17'],['2020','10','18']]
# These are the date to search in the db. The data are forecasts for the next day. +1 day for the files in Desktop


# This should be transformed to get the data from the sql db
def get_hourly_from_csv(day):
    i = day
    path = '/home/kaith/Desktop/'
    day = int(i[2]) + 1
    if day < 10:
        day = '0' + str(day)
    else:
        day = str(day)

    my_data = genfromtxt(path + str(i[0])+ str(i[1])+ day +'_WOOTIS.csv', delimiter=';',encoding = 'iso-8859-7')
    my_data = my_data[1:]
    my_data = my_data[:192]
    ellinochori = []
    ladi = []
    num = 4*24
    sumi = 0
    for i in range(num):
        sumi += my_data[i][6]
        if (i+1) % 4 == 0:
            ellinochori.append(sumi)
            sumi = 0
    my_data = my_data[num:]
    sumi = 0
    for i in range(len(my_data)):
        sumi += my_data[i][6]
        if (i+1) % 4 == 0:
            ladi.append(sumi)
            
            sumi = 0
    return ellinochori,ladi


def get_meteologica_data(date,):
    i = date
    day = i[0]+'-'+ i[1]+'-'+ i[2]
    data = meteologica.find()
    for i in data:
        if day in i['date']:
            print('FOUND')
            break 
    data = i
    ret = []
    ladi = []
    ellinochori = []
    for i in data['Ladi']:
        ladi.append(i[1])
    for i in data['Ellinochori']:
        ellinochori.append(i[1])
    return ladi,ellinochori


def get_meteomatics_data(date):
    i = date
    day = i[0]+'-'+ i[1]+'-'+ i[2]
    
    data = meteomatics.find()
    for i in data:
        if day in i['time']:
            break
    
    data = i
    ret = []
    ladi = []
    ellinochori = []
    for i in data['ladi']:
        ladi.append(i[1])
    for i in data['ellinochori']:
        ellinochori.append(i[1])
    return ladi,ellinochori


def rmse(l1,l2):
    sumi = 0
    for i in range(len(l1)):
        sumi += (l1[i]-l2[i])**2
    sumi /= len(l1)
    sumi = sumi**0.5
    return sumi

def mean_per(l1,l2):
    sumi = 0
    c = 0
    for i in range(len(l1)):
        if l1[i]!=0:
            c += 1
            sumi +=( (l1[i]-l2[i])**2 ) **0.5 
    mean_prod = sumi/c
    mean = sumi/len(l1)
    
    return mean_prod,mean

d1 = dates[:2]
for i in d1:
    
    ellinochori_actual, ladi_actual = get_hourly_from_csv(i)
    
    day = i[0]+'-'+ i[1]+'-'+ i[2]
     
    ladi_meteologica,ellinochori_meteologica = get_meteologica_data(i)
    ladi_meteomatics,ellinochori_meteomatics = get_meteomatics_data(i)

    ladi_logica_rmse = rmse(ladi_actual,ladi_meteologica)
    ladi_matics_rmse = rmse(ladi_actual,ladi_meteomatics)
    ellinochori_logica_rmse = rmse(ellinochori_actual,ellinochori_meteologica)
    ellinochori_matics_rmse = rmse(ellinochori_actual,ellinochori_meteomatics)
    
    ladi_logica_mean = mean_per(ladi_actual,ladi_meteologica)
    ladi_matics_mean = mean_per(ladi_actual,ladi_meteomatics)
    ellinochori_logica_mean = mean_per(ellinochori_actual,ellinochori_meteologica)
    ellinochori_matics_mean = mean_per(ellinochori_actual,ellinochori_meteomatics)
    
    print('METEOLOGICA')
    print('     LADI :')
    print('         RMSE:',ladi_logica_rmse)
    print('         MEAN:',ladi_logica_mean)
    print('     ELLINOCHORI :')
    print('         RMSE:',ellinochori_logica_rmse)
    print('         MEAN:',ellinochori_logica_mean)

    print('METEOMATICS')
    print('     LADI :')
    print('         RMSE:',ladi_matics_rmse)
    print('         MEAN:',ladi_matics_mean)
    print('     ELLINOCHORI :')
    print('         RMSE:',ellinochori_matics_rmse)
    print('         MEAN:',ellinochori_matics_mean)





