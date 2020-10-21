import pandas as pd
from sqlalchemy import create_engine
import datetime


def get_actual_and_enfor(edreth_code, date):

    engine = create_engine('postgresql://Michas:wootis!fose@192.168.1.225/RES')

    df = pd.read_sql('SELECT "EDRETH", "Prefix" FROM parks', engine)

    park = df.loc[df['EDRETH'] == edreth_code, 'Prefix'].values[0]

    data = pd.read_sql('SELECT * FROM ' + park, engine, parse_dates=['Date']).set_index('Date')

    data = data.loc[data.index.date == datetime.datetime.strptime(date, '%Y-%m-%d').date()]
    data = data.resample('H').sum()
    data = data.drop(columns=['Availability'])

    data_actual = data['NonValidated Production']
    data_daf = data['Dayahead Forecast']

    return data_actual, data_daf
