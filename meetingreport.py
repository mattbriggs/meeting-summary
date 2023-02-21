'''

{ "meeting_title": "",
"meeting_description": "",
"date": "",
"meeting_keywords": "",
"meeting_short_summary": "",
"speaker_summaries": "",
"meeting_attendees": "",
"meeting_agenda": "",
"meeting_action_items": "",
"media_path": ""
}

Save to: meetingdata.json

'''

import os
import shutil
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
import pandas as pd
import pystache as ST
import html
import mod_utilities as CU


def create_report(template_string, rootpath, dbpath, stem):
    try:
        meta_dict = create_report_raw(dbpath, rootpath, stem)
        create_markdown(template_string, rootpath, meta_dict, stem)
    except Exception as e:
        print("meetingreport.create_report: {}".format(e))


def create_markdown(template_string, rootpath, meta_dict, stem):
    '''with the filename stem and metadata create the file'''
    report_file = rootpath + "{}\\meeting-summary-{}.md".format(stem, stem)
    try:
        file_text = ST.render(template_string, meta_dict)
        CU.write_text(file_text, report_file)
    except Exception as e:
        print("meetingreport.create_markdown: {} : {}".format(report_file, e))

def create_report_raw(dbpath, rootpath, stem):
    ''' '''

    meeting_data = {}

    graphicpath = rootpath + "{}\\media\\".format(stem)
    if os.path.exists(graphicpath):
        shutil.rmtree(graphicpath)
    os.makedirs(graphicpath)
    graphic = "{}meetingsentiment.png".format(graphicpath)
    meeting_data["media_path"] = "./media/meetingsentiment.png"

    ## Meeting context

    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    m_raw = list(cur.execute('SELECT * From meeting;'))
    cur.close()

    meeting_data["meeting_title"] = m_raw[0][1]
    meeting_data["date"] = m_raw[0][2]
    meeting_data["meeting_attendees"] = m_raw[0][3]
    meeting_data["meeting_agenda"] = m_raw[0][4]
    meeting_data["meeting_action_items"] = m_raw[0][5]

    ## list of speakers

    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    speaker_raw = list(cur.execute('SELECT * From speaker_list;'))
    cur.close()

    speaker_list = []
    for i in speaker_raw:
        speaker_list.append(i[0])

    ## Create sentiment graph over time

    plt.style.use('seaborn')

    conn = sqlite3.connect(dbpath)
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

    conn = sqlite3.connect(dbpath)
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

    meeting_data["meeting_keywords"] = liststring

    ## get summaries

    summaries = {}
    for i in speaker_list:
        conn = sqlite3.connect(dbpath)
        cur = conn.cursor()
        sums = list(cur.execute('SELECT ShortSummary, LongSummary FROM summary WHERE Speaker="{}";'.format(i)))
        speakersum = {}
        speakersum["short"] = sums[0][0]
        speakersum["long"] = sums[0][1]
        cur.close()
        conn.close()

        summaries[i] = speakersum

    ## get tables

    tables = {}
    for i in speaker_list:
        conn = sqlite3.connect(dbpath)
        cur = conn.cursor()
        kwic = list(cur.execute('SELECT Entity, TStamp, Speaker, Verbatim, Sentiment FROM KWIC WHERE Speaker="{}";'.format(i)))
        tables[i] = kwic
        cur.close()
        conn.close()

        table = "\n\n| Entity | TStamp | Speaker | Verbatim | Sentiment |\n| --- | --- | --- | --- | --- |\n"
        for j in kwic:
            table += "| {} | {} | {} | {} | {} |\n".format(j[0], j[1], j[2], html.unescape(j[3]), j[4])

        tables[i] = table

    ## Create summaries

    speaker_summaries_text = ""
    meeting_short_summary_text = ""

    for i in speaker_list:
        meeting_short_summary_text += "\n\n### {}\n{}\n".format(i, summaries[i]["short"])
        speaker_summaries_text += "\n### {}\n\n#### Summary\n{}\n\n#### Keywords\n{}\n".format(i, summaries[i]["long"], tables[i])

    meeting_data["meeting_short_summary"] = meeting_short_summary_text
    meeting_data["speaker_summaries"] = speaker_summaries_text

    return meeting_data

def main():
    '''This is a module to create the data used for the report and the sentiment graph.'''
    print("This is a module for logic.")


if __name__ == "__main__":
    main()