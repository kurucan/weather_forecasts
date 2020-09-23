from ftplib import FTP
import pymongo
import csv
from datetime import datetime,timedelta



d = datetime.now()
next_day = d + timedelta(days=1)
d = str(d)
next_day = str(next_day)
d_as_inFtp = d.split(' ')[0]
dFtp = d_as_inFtp.replace('-','')
next_day=next_day.split(' ')[0]


client = pymongo.MongoClient('localhost',27017)
db = client['forecasts']
col = db['meteologica']

ftp = FTP('ftp.meteologica.com')#,user='Wootis_FTP',passwd='UF75-ip2')
ftp.login('Wootis_FTP','UF75-ip2')

a = ftp.retrlines('LIST')

a = a.split('\n')
fordb = {'date':d}
filematch = '*.csv'
for filename in ftp.nlst(filematch):
    if dFtp in filename:

        ergo = filename.split('-')[-1].split('.')[0]

        fhandle=open(filename, 'wb')
        ftp.retrbinary('RETR ' + filename, fhandle.write)
        read = open(filename,'r')
        a = csv.reader(read,delimiter=';')
        up = []
        for row in a:
            try:
                if next_day in row[2]:
                    up.append([row[2],float(row[5])])
            except:
                pass
        fordb[ergo] = up

        fhandle\
            .close()

print(fordb)
col.insert(fordb)
ftp.close()