#Author: Shibin George
#This script uses the 3rd - party python library: "BeautifulSoup"
#Please make sure that it is installed in your system

import urllib2
import urllib
from datetime import datetime, date, timedelta
from urllib import FancyURLopener
from bs4 import BeautifulSoup
from random import choice
import os
import zipfile
import operator
import time

def timedDelay(delay, count):
    while(count > 0):
        time.sleep(delay)
        count -= 1

    return

def editDistance(strA, strB):
    str1 = strA.capitalize()
    str2 = strB.capitalize()
    m = len(str1)#.length()
    n = len(str2)#.length()
    Matrix = [[0 for x in xrange(500)] for x in xrange(500)] 
    for i in range(1, m+1):
        Matrix[i][0] = i
    for i in range(1, n+1):
        Matrix[0][i] = i

    for i in range(1, m):
        for j in range(1, n):
            #print "checking  " + str1[i] + " with " + str2[j]
            if(str1[i]==str2[j]):
                Matrix[i][j] = Matrix[i-1][j-1]
            else:
                Matrix[i][j] = min(Matrix[i][j-1] + 1, Matrix[i-1][j] + 1, Matrix[i-1][j-1] + 1)

    #print "ed b/w " + str1 +  " and " + str2 + " is " + str(Matrix[m-1][n-1])
    return Matrix[m-1][n-1]


os.environ['http_proxy']=''
user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]
print "Please Enter the name of the movie: "
movieName = raw_input()

prefix = "http://www.subscene.com"
url = "http://subscene.com/subtitles/title?q="#the+man+from+earth&l="

url += movieName.replace(" ", "+")
print "Searching: " +  url + "&l="
response = urllib2.urlopen(url)
page = response.read()
#print page
index = 0
soup = BeautifulSoup(page)
#print soup
found = True
links = dict([(0, "www.subscene.com/")])
tag = soup.find("div", {"class" : "box"})
for category in tag.find_all("h2"):
    if(category.string=="No results found"):
        found = False
        break
    else:
        print "\nThese are your choices in category: " + category.string
        unorderedList = category.find_next_sibling("ul")
        for choice in unorderedList.find_all("a"):
            index += 1
            links[index] = choice["href"]
            print "\t" + str(index) + ": " +  choice.string


if(found == False):
    print "No matching results were found at www.subscene.com"
else:
    print "\nPlease Enter the index of your choice:"
    index = int(raw_input())
    movieLink = prefix + links[index] + "/"
    print "\nPlease also enter a language of your choice:"
    lang = raw_input()
    movieLink += lang
    print "Fetching data from www.subscene.com/ "
    response = urllib2.urlopen(movieLink)
    page = response.read()
    soup = BeautifulSoup(page)
    tableBody = soup.find('tbody')
    subtitleCount = 0

    fileDict = dict([(" ", " ")])
    for tr in  tableBody.find_all('tr'):
        td = tr.find('td')
        if(found==True):
            if('empty' in td['class']):
                found = False
                print "Sorry, there are no subtitles to show. Try another language."
                break
            else:
                aTag = td.find('a')
                url = prefix + aTag['href']
                span1 = aTag.find('span')
                if('positive-icon' in span1['class']):  #only searching for rated subtitles, the script ignores the unrated ones.
                    span2 = span1.find_next_sibling('span')
                    fileDict[url]  = span2.string.strip()
                    subtitleCount += 1

if(found == True):
    if(subtitleCount==0):
        print "We found no good/rated subtitles. We're pretty sure there are unrated ones."

    else:
        print "We have " + str(subtitleCount) + " subtitles in " + lang + " for you."
        print "Enter the file name of the video, remember to exclude the file-extension"
        fileName = raw_input()
        print "Crunching the data for you"
        timedDelay(0.67, 4)
        print"Done"

        minUrl = ""
        ed = dict([(" ", 99999999999999999999)])

        for url in fileDict:
            i = editDistance(" " + fileName, " " + fileDict[url])
            ed[url] = i

        sortedSubs = sorted(ed.iteritems(), key = operator.itemgetter(1))
        index = 0
        print "The following is the list of files in sorted order(according to similarity in filename), along with the URLs"
        for url in sortedSubs:
            if(url[0] != " "):
                index += 1
                links[index] = url[0]
                print "\t" + str(index) + ") " + fileDict[url[0]] + " :\t" + url[0]

        print "Fetching " + fileDict[links[1]] + " from url: " + links[1]
        timedDelay(0.1, 4)
        print"Done"
        response = urllib2.urlopen(links[1])
        page = response.read()
        soup = BeautifulSoup(page)
        div = soup.find('div', {'class' : 'download'})
        #print div
        aTag = div.find('a')
        fileUrl = prefix + aTag['href']
        print "Fetching the requested file from: " + fileUrl
        timedDelay(0.1, 4)
        print"Done"
        response = urllib2.urlopen(fileUrl)

        outputLocation = "/host/Visuals/" # <= Change this to your desired output location

        subtitleName = outputLocation + fileName
        file = open(subtitleName, "wb")
        file.write(response.read())
        file.close()
        print "Subtitle has been saved in output location."
        print "In case the subtitle found is not suitable, the url of other subtitles(ranked according to closeness) have been extracted."
        print "These files can be manually downloaded easily"

timedDelay(0.67, 3)
print "Thanks for reviewing/using this script."
#fh = open(subtitleName, 'rb')
#z = zipfile.ZipFile(fh)
#print "There are " + str(len(z.namelist())) + " files in the compressed folder."
#nameDiff = False
#if(len(z.namelist()) > 1):
#    nameDiff = True 
#for name in z.namelist():
#    print "Extracting file:" + name
#    #outpath = "C:\\"
#    z.extract(name, outputLocation)
#    os.rename(outputLocation + name, outputLocation + fileName)
#fh.close()
