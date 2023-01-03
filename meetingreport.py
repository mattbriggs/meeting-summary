'''

{ "meeting_title": "",
"meeting_description": "",
"date": "",
"meeting_summary": "",
"meeting_attendees": "",
"meeting_agenda": "",
"meeting_action_items": "",
"media_path": "",
"speaker-summaries": ""
}

Save to: meetingdata.json

'''



import os
import sqlite3
import yaml
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
import pandas as pd

import pystache as ST
import mod_utilities as MU

database = "wordsample/summary.db"
out_folder= "wordsample//"
graphic = "{}meetingsentiment.png".format(out_folder)

## list of speakers

conn = sqlite3.connect(database)
cur = conn.cursor()
speaker_raw = list(cur.execute('SELECT * From speaker_list;'))
cur.close()

speaker_list = []
for i in speaker_raw:
    speaker_list.append(i[0])

## Meeting context

meeting_title = ""
attendees = ""
agenda = '''

'''

action_items = '''

'''

## Create sentiment graph over time

plt.style.use('seaborn')

conn = sqlite3.connect(database)
data = pd.read_sql("SELECT * from line", con=conn)
conn.close()

data['Time'] = pd.to_datetime(data['TStamp'])
data.sort_values('Time', inplace=True)
sent_time = data['Time']
sent = data['Sentiment']
plt.plot_date(sent_time, sent, linestyle='solid')
plt.gcf().autofmt_xdate()
date_format = mpl_dates.DateFormatter('%H:%M:%S')
plt.gca().xaxis.set_major_formatter(date_format)
plt.tight_layout()
plt.title('Meeting Sentiment')
plt.xlabel('Time')
plt.ylabel('Sentiment')

plt.savefig(graphic)


## Top keywords

conn = sqlite3.connect(database)
cur = conn.cursor()
top_keywords = list(cur.execute('Select Entity, Score FROM Ranks ORDER BY Score Desc LIMIT 20;'))
cur.close()
conn.close()

liststring = "**Top keywords**:  "
no = len(top_keywords)
for indx, i in enumerate(top_keywords):
    if indx+1 < no:
        liststring += "{} ({}), ".format(i[0], i[1])
    else:
        liststring += "{} ({})\n".format(i[0], i[1])

# print(liststring)


## get summaries

summaries = {}
for i in speaker_list:
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    sums = list(cur.execute('SELECT ShortSummary, LongSummary FROM summary WHERE Speaker="{}";'.format(i)))
    #print(sums)
    speakersum = {}
    speakersum["short"] = sums[0][0]
    speakersum["long"] = sums[0][1]
    summaries[i] = speakersum
    cur.close()
    conn.close()

# print(speakersum)

## get tables

tables = {}
for i in speaker_list:
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    kwic = list(cur.execute('SELECT Entity, TStamp, Speaker, Verbatim, Sentiment FROM KWIC WHERE Speaker="{}";'.format(i)))
    tables[i] = kwic
    cur.close()
    conn.close()

# print(tables)


