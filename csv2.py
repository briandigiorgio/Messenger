#!/usr/bin/env python

import time as t

lp = True
if lp:
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()

if __name__ == '__main__':
    f = '/home/brian/Desktop/Code/Messenger/facebook-briandigiorgio/messages/anniezanger_2ca6e61030/message.html'
    topstr = '<div class="_4t5n" role="main">'
    userstr = '<div class="_3-96 _2pio _2lek _2lel">'
    normaldatestr = '</div><div></div><div></div></div></div><div class="_3-94 _2lem">'
    viddatestr = '</span></div></div></div><div class="_3-94 _2lem">'
    photodatestr = '<div class="_3-94 _2lem">'
    linkdatestr = '</a></div></div></div><div></div></div></div><div class="_3-94 _2lem">'
    reactdatestr = '</li></ul></div></div></div><div class="_3-94 _2lem">' 
    audiodatestr = '</a></audio></div></div></div><div class="_3-94 _2lem">'

    textstr = '</div><div class="_3-96 _2let"><div><div></div><div>'
    endstr = '</div></div><div class="pam _3-95 _2pi0 _2lej uiBoxWhite noborder">'
    videostr = '<span class="_idm">Duration: '
    photostr = '<img src="'
    linkstr = '<a href="'
    reactstr = '</div><div></div><div></div><div><ul class="_tqp"><li>'
    audiostr = '<audio src="'

    messages = open(f).read()
    messages = messages[messages.find(topstr):]
    messages = messages.replace('\n','')
    messages = messages.replace('&#039;',"'")
    messages = messages.replace('&quot;',"'")

    header = 'mtype,user,month,day,year,hour,minute,ampm,time,text'
    if lp:
        header += ',comp,neg,neu,pos'

    out = open('messages22.csv', 'w+')
    out.write(header)

    start=t.time()
    counter = 0
    i = 0
    ilast = 0
    done = False
    while i < len(messages) and not done:
        try:
            message = messages[i:messages.find(endstr,i)]
            if videostr in message:
                datestr = viddatestr
            elif photostr in message:
                datestr = photodatestr
            elif linkstr in message and photostr not in message:
                datestr = linkdatestr
            elif reactstr in message:
                datestr = reactdatestr
            else:
                datestr = normaldatestr

            userstart = messages.find(userstr,i) + len(userstr)
            userend = messages.find(textstr,i)
            user = messages[userstart:userend]

            textstart = messages.find(textstr,i) + len(textstr)
            textend = messages.find(datestr,i)
            text = messages[textstart:textend]
            text = text.replace(',',';')

            if photostr in text:
                text = text[text.find(photostr)+len(photostr):text.find('"')]
            elif linkstr in text and photostr not in text:
                text = text[text.find(linkstr)+len(linkstr):text.find('"')]
            elif audiostr in text and photostr not in text:
                text = text[text.find(audiostr)+len(audiostr):text.find('"')]

            datestart = messages.find(datestr,i) + len(datestr)
            dateend = messages.find(endstr,i)
            date = messages[datestart:dateend]

            month = date[:date.find(' ')]
            day = date[date.find(' ')+1:date.find(',')]
            time = date[date.find(', ')+7:]
            date = date[date.find(',')+2:]
            year = date[:date.find(' ')]

            ampm = time[-2:]
            minute = time[-4:-2]
            hour = int(time[:-5])
            if ampm == 'pm' and hour != 12:
                hour += 12
            if hour == 12 and ampm == 'am':
                hour = 0
            time = t.mktime(t.strptime('%s %s %s %s %s %s' % (hour, minute, ampm, 
                day, month, year), '%H %M %p %d %b %Y'))

            mtype = 'Text'
            if videostr in text:
                mtype = 'Video'
                text = text[text.find(':')+2:]
                if 'sec' in text:
                    text = '0'
                elif 'min' in text:
                    text = text[:text.find(' ')]

            elif photostr in text:
                mtype = 'Image'

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
            i =  messages.find(endstr,i) + len(endstr)

            if i < ilast:
                done = True

            out.write('\n%s,%s,%s,%s,%s,%s,%s,%s,%f,%s'
                    %(mtype,user,month,day,year,hour,minute,ampm,time,text))
            if lp:
                out.write(',%f,%f,%f,%f' % (comp,neg,neu,pos))

            counter += 1
            if counter%1000 == 0:
                print('%g%%' % (100*i/len(messages)), end = '\r')
        except:
            ilast = i
            i = messages.find(endstr,i) + len(endstr)
            if i < ilast:
                done = True
            continue
    print(t.time() - start)
