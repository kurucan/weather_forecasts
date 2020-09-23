import meteomatics.api as api
import json
from datetime import datetime,timedelta
from threading import Timer
import pymongo
import time

date = datetime.now()
print(date)
timestr = str(date).split(' ')[1].split('.')[0]
date = str(date).split(' ')[0]

client = pymongo.MongoClient('localhost',27017)
db = client['forecasts']
col = db['meteomatics']

def getdata():
    usrnm = 'joule_michas'
    psw = 'KxN9lBXpbqU67'

    # photovoltaika
    # #prod = api.query_grid()
    ladi = api.query_api(
        f'https://api.meteomatics.com/{date}T00:00:00ZP2D:PT1H/solar_power_installed_capacity_0.5_tracking_type_fixed_orientation_180_tilt_28:MW/41.4773,26.2253/json',
        usrnm, psw)
    ellinochori = api.query_api(
        f'https://api.meteomatics.com/{date}T00:00:00ZP2D:PT1H/solar_power_installed_capacity_0.5_tracking_type_fixed_orientation_180_tilt_28:MW/41.389,26.4878/json',
        usrnm, psw)
    dateT = str(datetime.now() + timedelta(days=1)).split(' ')[0]

    ladi_up = []
    ladi_l = ladi.json()['data'][0]['coordinates'][0]['dates']
    for i in ladi_l:

        d = i['date']
        d = datetime.strptime(d,'%Y-%m-%dT%H:%M:%SZ')
        d = d + timedelta(hours=3)
        d = str(d)
        if dateT in d:
            ladi_up.append([d, 1000 * i['value']])

    ellinochori_up = []
    ellinochori_l = ellinochori.json()['data'][0]['coordinates'][0]['dates']
    for i in ellinochori_l:
        d = i['date']
        d = datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ')
        d = d + timedelta(hours=3)
        d = str(d)
        if dateT in d:
            ellinochori_up.append([d,1000* i['value']])

    up = {
        'ladi': ladi_up,
        'ellinochori': ellinochori_up,

        'time': date + ' ' + timestr
    }
    return up


up = getdata()
print(up)
col.insert_one(up)



########################################
# ammovouno = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/solar_power_installed_capacity_1_tracking_type_azimuth-tracking:MW/41.5554,26.3131/json',
#     usrnm, psw)
#
# isaakio = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/solar_power_installed_capacity_1_tracking_type_azimuth-tracking:MW/41.3606,26.5487/json',
#     usrnm, psw)
# poimeniko = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/solar_power_installed_capacity_0.5_tracking_type_fixed_orientation_180_tilt_28:MW/41.4729,26.379/json',
#     usrnm, psw)
# sterna = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/solar_power_installed_capacity_0.5_tracking_type_fixed_orientation_180_tilt_28:MW/41.555,26.4342/json',
#     usrnm, psw)
# mdoksipara1 = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/solar_power_installed_capacity_0.5_tracking_type_fixed_orientation_180_tilt_28:MW/41.5431,26.2712/json',
#     usrnm, psw)
# mdoksipara2 = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/solar_power_installed_capacity_0.5_tracking_type_fixed_orientation_180_tilt_28:MW/41.5273,26.2612/json',
#     usrnm, psw)
# mdoksipara3 = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/solar_power_installed_capacity_0.5_tracking_type_fixed_orientation_180_tilt_28:MW/41.5506,26.2584/json',
#     usrnm, psw)
# eugeniko = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/solar_power_installed_capacity_0.5_tracking_type_fixed_orientation_180_tilt_28:MW/41.4345,26.3586/json',
#     usrnm, psw)
#
# # aiolika
# bourlari1_6252 = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/wind_power_turbine_nordex_n43_600_hub_height_40m:MW/38.06668565491725,24.37918229547799/json',
#     usrnm, psw)
# bourlari2_6253 = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/wind_power_turbine_nordex_n43_600_hub_height_40m:MW/38.06748779583044,24.378322858785292/json',
#     usrnm, psw)
# bourlari3_6254 = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/wind_power_turbine_nordex_n43_600_hub_height_40m:MW/38.06943585233388,24.378609337682857/json',
#     usrnm, psw)
#
# mawrandoni1_6357 = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/wind_power_turbine_nordex_n43_600_hub_height_50m:MW/38.058320471108345,24.392474916325025/json',
#     usrnm, psw)
# mawrandoni2_6356 = api.query_api(
#     'https://api.meteomatics.com/2020-08-28T00:00:00ZP5D:PT1H/wind_power_turbine_nordex_n43_600_hub_height_50m:MW/38.05917990780104,24.39333435301772/json',
#     usrnm, psw)