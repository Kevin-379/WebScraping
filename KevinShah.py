import requests
from bs4 import BeautifulSoup
import os  # to get path for making folder year/month

input = open("input.txt", "r")
data = input.readlines()
input.close()

if len(data) == 3:
    start = data[0].strip().split()
    stop = data[1].strip().split()
    authors = data[2].strip().split()

    num = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
           'september': 9, 'october': 10, 'november': 11, 'december': 12}  # converts month to number
    mon = {n: m for m, n in num.items()}  # converts number to month

    s1 = num[start[0]]  # start month
    s2 = start[1]  # start year
    s3 = num[stop[0]]  # end month
    s4 = stop[1]  # end year
    j = s1
    i = int(s2)
    download = []  # list containing urls of comics that satisfy given condition
    # iterating from start month to end month
    while i <= int(s4):
        while j <= 12:
            URL1 = "http://explosm.net/comics/archive/" + s2 + "/" + str(s1)
            r1 = requests.get(URL1)
            soup1 = BeautifulSoup(r1.content, 'html5lib')
            table1 = soup1.findAll('div', {'class': 'small-12 medium-12 large-12 columns'})  # div containing url
            author = soup1.findAll('div', {'id': 'comic-author'})  # div containing author details
            for t in range(len(author)):
                auth = author[t].text.split()
                if auth[2] in authors:  # auth[2] is author's first name
                    download.append([table1[t + 3].div.div.div.a['href'], auth])  # +3 since first few did not contain comics
            os.makedirs(str(i) + '/' + mon[j])  # making folder year/month
            j += 1
        j = 1  # resetting to january after end of year
        i += 1

    # iterating to download required comics
    for link in download:
        URL2 = 'http://explosm.net' + link[0]
        r2 = requests.get(URL2)
        soup2 = BeautifulSoup(r2.content, 'html5lib')
        img = soup2.find('img', {'id': 'main-comic'})
        imglink = 'http:' + img['src']  # link of .png file
        imgname = os.getcwd() + '/' + link[1][0][:4] + '/' + mon[int(link[1][0][5:7])] + '/' + link[1][0] + '-' + link[1][
            2] + '.png'  # img file name with path
        r3 = requests.get(imglink)
        with open(imgname, 'wb') as f:
            f.write(r3.content)

elif data[0] == 'Random':
    os.makedirs('random')
    URL4 = 'http://explosm.net/rcg'
    r4 = requests.get(URL4)
    soup4 = BeautifulSoup(r4.content, 'html5lib')
    frame = soup4.findAll('img')
    framename1 = os.getcwd() + '/' + 'Random' + '/' + 'frame1.png'
    framename2 = os.getcwd() + '/' + 'Random' + '/' + 'frame2.png'
    framename3 = os.getcwd() + '/' + 'Random' + '/' + 'frame3.png'
    framename = [framename1, framename2, framename3]
    for i in range(3):
        r = requests.get(frame[i+1]['src'])
        with open(framename[i], 'wb') as f:
            f.write(r.content)

else:
    os.makedirs('latest')
    N = int(data[0].strip().split()[1])  # number of comics to be downloaded
    URL = "http://explosm.net/comics/archive/"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    latest = soup.find('div', {'class': 'small-3 medium-3 large-3 columns'})
    num = int(latest.a['href'][-5:-1])
    i = 0
    while i < N:
        URL = 'http://explosm.net/comics/' + str(num) + '/'
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html5lib')
        img = soup.find('img', {'id': 'main-comic'})
        imglink = 'http:' + img['src']
        auth = soup.find('div', {'id': 'comic-author'})
        author = auth.text.strip().split()
        img = os.getcwd() + '/' + 'latest' + '/' + author[0] + '-' + author[2] + '.png'
        r = requests.get(imglink)
        with open(img, 'wb') as f:
            f.write(r.content)
        num -= 1
        i += 1
