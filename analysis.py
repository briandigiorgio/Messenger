#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
from PIL import Image

if __name__ == '__main__':
    messages = np.genfromtxt('messages22.csv', delimiter = ',', names = True,
            dtype = None, comments = 'tfasdfasfhasgdfgeewrewfv')
    tot = np.rec.array(messages)
    j17 = 1496275200
    j18 = 1527811200
    cut = tot[(tot.time > j17) * (tot.time < j18)]
    vids = cut[cut.mtype == 'Video']
    texts = cut[cut.mtype == 'Text']
    hearts = cut[cut.mtype == 'Heart']
    months = ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 
            'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May']
    monlen = [30,31,31,30,31,30,31,31,28,31,30,31]
    dayssince = np.cumsum(monlen)
    #stopwords = set(stopwords.words('english'))
    stopwords = set(STOPWORDS)
    commonwords = np.genfromtxt('1-1000.txt', max_rows = 1000, dtype = str)
    for i in commonwords:
        stopwords.add(i)
    for i in ('YEAH', 'IT', 'THINGS', 'GOING', 'STUFF', 'REALLY'):
        stopwords.add(i)

    bm = tot[(tot.user == 'Brian DiGiorgio') * (tot.mtype == 'Text')]
    am = tot[(tot.user == 'Annie Zanger') * (tot.mtype == 'Text')]
    tm = tot[(tot.mtype == 'Text')]
    print('Total Messages: %d' % len(cut))
    print('Fraction Brian: %g' % (len(bm)/len(tm)))
    print('Fraction Annie: %g' % (len(am)/len(tm)))
    print()

    bq = 0
    for i in range(len(bm)):
        if '?' in bm.text[i]:
            bq += 1
    print('Brian question fraction: %g' % (bq/len(bm)))

    aq = 0
    for i in range(len(am)):
        if '?' in am.text[i]:
            aq += 1
    print('Annie question fraction: %g' % (aq/len(am)))

    be = 0
    for i in range(len(bm)):
        if '!' in bm.text[i]:
            be += 1
    print('Brian ! fraction: %g' % (be/len(bm)))

    ae = 0
    for i in range(len(am)):
        if '!' in am.text[i]:
            ae += 1
    print('Annie ! fraction: %g' % (ae/len(am)))
    print()

    plt.hist(cut.hour, bins = 24)
    plt.title('Messages by Hour (PST)')
    plt.xlabel('Hour')
    plt.ylabel('Messages')
    plt.show()

    plt.hist((cut.time-j17)/86400, bins = 365)
    plt.title('Messages per Day')
    plt.xlabel('Day')
    plt.ylabel('Messages')
    plt.xlim((0,365))
    plt.xticks(dayssince, months[1:])
    plt.axhline(len(cut)/365, c = 'r', ls = '--')
    plt.show()

    tl = 0
    for i in range(len(tm)):
        tl += len(tm.text[i])

    bl = 0
    for i in range(len(bm)):
        bl += len(bm.text[i])
    print("Brian character count fraction: %f" % (bl/tl))
    print("Brian average message length: %g" % (bl/len(bm)))

    al = 0
    for i in range(len(am)):
        al += len(am.text[i])
    print("Annie character count fraction: %f" % (al/tl))
    print("Annie average message length: %g" % (al/len(am)))

    vidlen = np.zeros(len(months))
    for i in range(len(months)):
        vidlen[i] = np.sum(vids[vids.month == months[i]].text.astype(int))
    plt.plot(vidlen/60)
    plt.title('Video Call Length by Month')
    plt.xticks(np.arange(12), months)
    plt.xlabel('Month')
    plt.ylabel('Total Hours of Videocall')
    plt.ylim(ymin=0)
    plt.axhline(np.mean(vidlen)/60, c = 'r', ls = '--')
    plt.show()

    tbm = np.zeros(len(months))
    for i in range(len(months)):
        tbm[i] = np.sum(len(texts[texts.month == months[i]].text))
    plt.plot(tbm)
    plt.title('Total Messages by Month')
    plt.xticks(np.arange(12), months)
    plt.xlabel('Month')
    plt.ylabel('Total Messages')
    plt.ylim(ymin=0)
    plt.axhline(np.mean(tbm), c = 'r', ls = '--')
    plt.show()

    plt.hist(cut.day, bins = 31)
    plt.title('Messages by Day of Month')
    plt.xticks(np.arange(1,31,3))
    plt.xlabel('Day')
    plt.ylabel('Total Messages')
    plt.axhline(len(cut)/31, c = 'r', ls = '--')
    plt.show()

    hbm = np.zeros(len(months))
    for i in range(len(months)):
        hbm[i] = np.sum(hearts.month == months[i])
    plt.plot(hbm, 'r-')
    plt.scatter(np.arange(12), hbm, c = 'r', s = 200, marker = r'$\heartsuit$')
    plt.title('Total Hearts by Month')
    plt.xticks(np.arange(12), months)
    plt.xlabel('Month')
    plt.ylabel('Total Hearts')
    plt.ylim(ymin=0)
    plt.axhline(np.mean(hbm), c = 'k', ls = '--')
    plt.show()

    sid = SentimentIntensityAnalyzer()
    acomp = np.zeros(len(months))
    aneg = np.zeros(len(months))
    aneu = np.zeros(len(months))
    apos = np.zeros(len(months))
    bcomp = np.zeros(len(months))
    bneg = np.zeros(len(months))
    bneu = np.zeros(len(months))
    bpos = np.zeros(len(months))
    for i in range(len(months)):
        amcut = am[am.month == months[i]]
        bmcut = bm[bm.month == months[i]]
        
        acomp[i] = np.sum(amcut.comp < 0)/len(amcut)
        aneg[i] = np.sum(amcut.neg > 0)/len(amcut)
        aneu[i] = np.sum(amcut.neu > 0)/len(amcut)
        apos[i] = np.sum(amcut.pos > 0)/len(amcut)

        bcomp[i] = np.sum(bmcut.comp < 0)/len(bmcut)
        bneg[i] = np.sum(bmcut.neg > 0)/len(bmcut)
        bneu[i] = np.sum(bmcut.neu > 0)/len(bmcut)
        bpos[i] = np.sum(bmcut.pos > 0)/len(bmcut)

    plt.figure(figsize = (8,4))
    plt.subplot(121)
    plt.plot(acomp, 'k', label = 'Overall')
    plt.plot(aneu, 'b', label = 'Neutral')
    plt.plot(aneg, 'r', label = 'Negative')
    plt.plot(apos, 'g', label = 'Positive')
    plt.title('Annie Sentiments')
    plt.xticks(np.arange(12), months)
    plt.xlabel('Month')
    plt.ylim((0,1))
    plt.legend()

    plt.subplot(122)
    plt.plot(bcomp, 'k', label = 'Overall')
    plt.plot(bneu, 'b', label = 'Neutral')
    plt.plot(bneg, 'r', label = 'Negative')
    plt.plot(bpos, 'g', label = 'Positive')
    plt.title('Brian Sentiments')
    plt.xticks(np.arange(12), months)
    plt.xlabel('Month')
    plt.ylim((0,1))
    plt.legend()
    plt.tight_layout()
    plt.show()

    btext = ''
    for i in range(len(bm)):
        btext += bm.text[i].upper()

    atext = ''
    for i in range(len(am)):
        atext += am.text[i].upper()

    bwords = nltk.word_tokenize(btext)
    bwords = [word for word in bwords if word not in stopwords and word not in
            commonwords and len(word) > 2 and "'" not in word]
    bfreq = nltk.FreqDist(bwords)
    #for word, freq in bfreq.most_common(100):
    #    print('%s: %g' % (word, freq))

    awords = nltk.word_tokenize(atext)
    awords = [word for word in awords if word not in stopwords and word not in
            commonwords and len(word) > 2 and "'" not in word]
    afreq = nltk.FreqDist(awords)
    #for word, freq in afreq.most_common(100):
    #    print('%s: %g' % (word, freq))

    cloud = np.array(Image.open('cloud.jpg'))
    bwc = WordCloud(background_color='white', stopwords = stopwords, width
            = 500, height = 500, mask = cloud, max_words = 1000).generate(btext)
    awc = WordCloud(background_color='white', stopwords = stopwords, width
            = 500, height = 500, mask = cloud, max_words = 1000).generate(atext)

    plt.imshow(bwc.recolor(colormap='viridis'), interpolation = 'bilinear')
    plt.title('Brian')
    ax = plt.gca()
    ax.axis('off')
    plt.tight_layout()
    plt.show()

    plt.imshow(awc.recolor(colormap='winter'), interpolation = 'bilinear')
    plt.title('Annie')
    ax = plt.gca()
    ax.axis('off')
    plt.tight_layout()
    plt.show()
