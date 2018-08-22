#!/usr/bin/env python

import time as t

lp = True
if lp:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()

if __name__ == '__main__':
    #f = '/home/brian/Downloads/facebook-briandigiorgio/messages/25.html'
    f =\
    '/home/brian/Desktop/Code/Messenger/facebook-briandigiorgio/messages/anniezanger_2ca6e61030/message.html'
    messages = open(f).read()[1701:]
    messages = messages.replace('\n','')
    messages = messages.replace('&#039;',"'")
    messages = messages.replace('&quot;','"')

    userstr = '<span class="user">'
    datestr = '</span><span class="meta">'
    textstr = '</span></div></div><p>'
    endstr = '</p>'
    videostr = '<span style="float:right">Duration: '
    photostr = '<img src="'

    header = 'mtype,user,week,month,day,year,hour,minute,ampm,time,text'
    if lp:
        header += ',comp,neg,neu,pos'

    out = open('messages.csv', 'w+')
    out.write(header)

    start=t.time()
    counter = 0
    i = 0
    ilast = 0
    while i < len(messages):
        userstart = messages.find(userstr,i) + len(userstr)
        userend = messages.find(datestr,i)
        user = messages[userstart:userend]

        datestart = messages.find(datestr,i) + len(datestr)
        dateend = messages.find(textstr,i)
        date = messages[datestart:dateend]
        
        week = date[:date.find(',')]
        date = date[date.find(',')+2:]

        month = date[:date.find(' ')]
        date = date[date.find(' ')+1:]

        day = date[:date.find(',')]
        date = date[date.find(',')+2:]

        year = date[:date.find(' ')]
        date = date[date.find(' ')+4:]

        time = date[:date.find(' ')]
        ampm = time[-2:]
        minute = time[-4:-2]
        hour = int(time[:-5])
        if ampm == 'pm' and hour != 12:
            hour += 12
        if hour == 12 and ampm == 'am':
            hour = 0
        time = t.mktime(t.strptime('%s %s %s %s %s %s' % (hour, minute, ampm, 
            day, month, year), '%H %M %p %d %B %Y'))

        textstart = messages.find(textstr,i) + len(textstr)
        textend = messages.find(endstr,i)
        text = messages[textstart:textend]
        text = text.replace(',',';')

        mtype = 'Text'
        if videostr in text:
            mtype = 'Video'
            text = text[text.find(videostr)+len(videostr):text.find('</span>')]
            if 'sec' in text:
                text = '0'
            elif 'min' in text:
                text = text[:text.find(' ')]

        elif photostr in text:
            mtype = 'Image'
            text = text[text.find(photostr)+len(photostr):text.find('"')]

        elif '❤' in text and len(text) == 1:
            mtype = 'Heart'

        if lp:
            if mtype == 'Text':
                ss = sid.polarity_scores(text)
                comp = ss['compound']
                neg = ss['neg']
                neu = ss['neu']
                pos = ss['pos']
            else:
                comp = 0
                neg = 0
                neu = 0
                pos = 0

        ilast = i
        i += textend + len(endstr) + 10 - i

        if i < ilast:
            break

        out.write('\n%s,%s,%s,%s,%s,%s,%s,%s,%s,%f,%s'
                %(mtype,user,week,month,day,year,hour,minute,ampm,time,text))
        if lp:
            out.write(',%f,%f,%f,%f' % (comp,neg,neu,pos))

        counter += 1
    print(t.time() - start)
