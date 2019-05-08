import time
import pathlib
import smtplib
import os, os.path
import selenium.webdriver.support.ui as ui

from string import Template
from selenium import webdriver
from urllib.request import Request, urlopen
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

selection = 'new'
mirror = ''

def parseProgram(item):
    newStr = ''
    for i in item:
        if i.isalpha() or i.isdigit():
            newStr += i
        elif i == ' ':
            newStr += '%20'
    return newStr


def readUntilChar(string, stopChar, startIndex, ignores):
    currIndex = startIndex
    reading = True
    try:
        while reading == True:
            if string[currIndex] != stopChar:
                currIndex += 1
            elif string[currIndex] == stopChar:
                if ignores == 0:
                    currIndex += 1
                    reading = False
                else:
                    currIndex += 1
                    ignores = ignores - 1
        return currIndex-1
    except:
        return '404 Error...'


def findLiveMirror(htmlSource):
    prefix = '//vidcloud.icu/streaming.php?id='
    startIndex = htmlSource.find(prefix)
    endIndex = readUntilChar(htmlSource, '"', startIndex, 0)
    try:
        item = str(htmlSource[startIndex:endIndex])
        return item
    except:
        return 404
def clearScreen():
    clear()


def displayList(list):
    count = 1
    for item in list:
        print(str(count) + ') ' + item.text)
        count += 1

def getCurrentPath():
    dir_path = pathlib.PureWindowsPath(os.path.dirname(os.path.realpath(__file__)))
    return dir_path

def findEpisodes(source, startSignal, stopSignal):
    episodeURLs = []
    startSignal = source.find(startSignal)
    stopSignal = source.find(stopSignal)
    currListIndex = startSignal+1
    while currListIndex > startSignal and currListIndex < stopSignal:
        listing = source.find('/videos/', currListIndex)
        endOfLink = readUntilChar(source, '"', listing, 0)
        if endOfLink < stopSignal:
            episodeURLs.append(source[listing: endOfLink])
        currListIndex = listing+1
    return episodeURLs

def displayEpisodes(episodeList):
    episode = len(episodeList)-1
    count = 1
    for i in episodeList:
        print(str(count) + ') ' + episodeList[episode])
        episode = episode - 1
        count += 1

def replaceBackslash(string):
    return str(string.as_posix())

def addExtensions(extensionList, chromeOptions):
    for extension in extensionList:
        chromeOptions.add_extension(str(replaceBackslash(getCurrentPath()))+extension)

def getRawText(file, extension):
    text = ''
    currPath = str(replaceBackslash(getCurrentPath()))
    with open(os.path.join(currPath + '/' + file + extension), 'r') as file:
        readText = file.read(1)
        if readText == '':
            return ''
        else:
            text += readText
            while readText != '':
                readText = file.read(1)
                text += readText
        file.close()
    return text

def getChromeVersion(driver):
    chromeVersion = driver.capabilities['version'][0:2]
    if chromeVersion == '71':
        chromeVersion = '7.1'
    elif chromeVersion == '72':
        chromeVersion = '7.2'
    elif chromeVersion == '73':
        chromeVersion = '7.3'
    elif chromeVersion == '74':
        chromeVersion = '7.4'
    elif chromeVersion == '75':
        chromeVersion = '7.5'
    return chromeVersion

def closeTabs(numTabs, driver):
    while numTabs > 0:
        driver.close()
        numTabs = numTabs - 1

def getSiteSource(URL):
    req = Request(URL, headers={'User-Agent': 'Chrome/'+chromeVersion})
    webpage = urlopen(req).read()
    return webpage

def findRealVideo(stuff):
    pass

#https://redirector.googlevideo.com

def isSafeSite(siteHT, unsafeKeywords):
    siteHT = str(siteHT)
    for word in unsafeKeywords:
        #print(siteHT.find(word))
        if siteHT.find(word) is not -1:
            return False
    return True

def isDriverActive(driver):
    try:
        url = driver.current_url
        return True
    except:
        return False

def getPlayerStatus(playerClass, statusList):
    for status in statusList:
        if status in playerClass:
            return status

while selection == 'new' or selection == 'return':
    episodeQueue = []
    episodeChoice = None
    chromeVersion = None
    CHROMEDRIVER73_PATH = str(replaceBackslash(getCurrentPath()))+'/Driver73.0.3683.68/chromedriver'
    CHROMEDRIVER74_PATH = str(replaceBackslash(getCurrentPath()))+'/Driver74.0.3729.6/chromedriver'
    CHROMEDRIVER75_PATH = str(replaceBackslash(getCurrentPath()))+'/Driver75.0.3770.8/chromedriver'
    options = Options()
    options.headless = True
    options.add_argument('log-level=3')
    options.add_argument('--disable-infobars')
    clear = lambda: os.system('cls')
    
    try:
        clearScreen()
        driver = webdriver.Chrome(CHROMEDRIVER73_PATH, options=options)
    except:
        print('Version 73 failed, moving to 74.')
    if driver is None:
        try:
            clearScreen()
            driver = webdriver.Chrome(CHROMEDRIVER74_PATH, options=options)
        except:
            print('Version 74 failed, moving to 75.')
    if driver is None:
        try:
            clearScreen()
            driver = webdriver.Chrome(CHROMEDRIVER75_PATH, options=options)
        except:
            clearScreen()
            print('All valid chromedriver versions failed! Update your Chrome!')
            quit()

    tvShow = False

    clearScreen()
    chromeVersion = getChromeVersion(driver)
    print(chromeVersion)
    program = input('What would you like to watch?\n')
    parsedQuery = parseProgram(program)
    driver.get('https://vidcloud.icu/search.html?keyword='+parsedQuery)
    req = Request('https://vidcloud.icu/search.html?keyword='+parsedQuery, headers={'User-Agent': 'Chrome/'+chromeVersion})
    queryResultPage = urlopen(req).read()
    queryResultList = findEpisodes(str(queryResultPage), 'href="/videos', '</html')
    queryResults = driver.find_elements_by_class_name("name")

    clearScreen()
    displayList(queryResults)
    selection = input('Enter the corresponding number of your selection, type "new" to enter a new query, or just return to quit!\n')
    if selection.isdigit():
        #print(selection)
        if (int(selection)-1) <= len(queryResults):
            clearScreen()
            req = Request('https://vidcloud.icu'+queryResultList[int(selection)-1], headers={'User-Agent': 'Chrome/'+chromeVersion})
            webpage = urlopen(req).read()
            streamingLink = findLiveMirror(str(webpage))
            if streamingLink == 404:
                print('404 error...')
                quit()
            else:
                episodes = findEpisodes(str(webpage), 'list_episdoe', 'class="comment"')
                if len(episodes) > 1:
                    tvShow = True
                    print('you have selected a tv show...')
                    print('here are the episodes from ' + queryResults[int(selection)-1].text)
                else:
                    print('Your entertainment experience is loading...')
            if tvShow:
                episodes = findEpisodes(str(webpage), 'list_episdoe', 'class="comment"')
                displayEpisodes(episodes)
                for result in episodes:
                    episodeQueue.append(result)
                episodeSelection = input('Please select an episode, or type "return" to go back...')
                episodeChoice = len(episodes)-int(episodeSelection)
                req = Request('https://vidcloud.icu'+episodes[episodeChoice], headers={'User-Agent': 'Chrome/'+chromeVersion})
                webpage = urlopen(req).read()
                streamingLink = findLiveMirror(str(webpage))
            driver.quit()
            options.headless = False
            options.add_argument("--start-maximized")
            status = ["jw-state-idle","jw-state-playing","jw-state-paused","jw-state-complete"]
            extensions = ['/Extensions/uBlock-Origin_v1.18.8.crx',
                          '/Extensions/Whitelist-Manager_v2.4.0.crx',
            #              '/Extensions/Popup-Blocker-(strict)_v0.5.0.6.crx',
            #              '/Extensions/MINEBLOCK-Block-web-miners-&-crypto-scripts_v1.1.crx',
                          '/Extensions/WebRTC-Network-Limiter_v0.2.1.3.crx',
                          '/Extensions/CsFire_v2.0.7.crx']
            badLinks = ['https://api.vidnode.net/stream.php?type=estream']
            addExtensions(extensions, options)
            #time.sleep(2)
            siteSafety = isSafeSite(getSiteSource('https:'+streamingLink), badLinks)
            if siteSafety is not False:
                if chromeVersion == '7.3':
                    driver2 = webdriver.Chrome(CHROMEDRIVER73_PATH, options=options)
                elif chromeVersion == '7.4':
                    driver2 = webdriver.Chrome(CHROMEDRIVER74_PATH, options=options)
                elif chromeVersion == '7.5':
                    driver2 = webdriver.Chrome(CHROMEDRIVER75_PATH, options=options)
                #driver2.maximize_window()
                driver2.get('https://'+streamingLink)
                clearScreen()
                #video = driver2.find_element_by_id('myVideo').click()
                #time.sleep(0.5)
                #driver2.fullscreen_window()
                #fullscreen = driver2.find_element_by_xpath('//div[@class="jw-icon jw-icon-inline jw-button-color jw-reset jw-icon-fullscreen"]').sendKeys(Keys.F11)
                debounce = False

                #AUTOPLAY FEATURE! More progress to come...
                if tvShow:
                    while isDriverActive(driver2):
                        videoDriver = driver2.find_element_by_id('myVideo')
                        if getPlayerStatus(str(videoDriver.get_attribute('class')),status) == 'jw-state-idle':
                            debounce = False
                            videoDriver.click()
                            driver2.fullscreen_window()
                        elif getPlayerStatus(str(videoDriver.get_attribute('class')),status) == 'jw-state-playing':
                            debounce = False
                        elif getPlayerStatus(str(videoDriver.get_attribute('class')),status) == 'jw-state-complete':
                            if debounce == False:
                                episodeChoice = episodeChoice - 1
                                req = Request('https://vidcloud.icu'+episodes[episodeChoice], headers={'User-Agent': 'Chrome/'+chromeVersion})
                                webpage = urlopen(req).read()
                                streamingLink = findLiveMirror(str(webpage))
                                siteSafety = isSafeSite(getSiteSource('https:'+streamingLink), badLinks)
                                if siteSafety is not False:
                                    driver2.get('https://'+streamingLink)
                                    #clearScreen()
                                    debounce = True
                                else:
                                    episodeChoice = episodeChoice + 1
                                    streamingLink = None
                                    while siteSafety is False:
                                        episodeChoice = episodeChoice - 1
                                        print('inside while loop episode choice is ' + str(episodeChoice))
                                        req = Request('https://vidcloud.icu'+episodes[episodeChoice], headers={'User-Agent': 'Chrome/'+chromeVersion})
                                        webpage = urlopen(req).read()
                                        streamingLink = findLiveMirror(str(webpage))
                                        siteSafety = isSafeSite(getSiteSource('https:'+streamingLink), badLinks)
                                    driver2.get('https://'+streamingLink)
                                    #clearScreen()
                                    episodeChoice = episodeChoice - 1
                                    debounce = True
                        time.sleep(1)
                selection = input('If you would like to watch something else, just type "new"...')
            else:
                #TODO: REDIRECT TO A DIFFERENT MIRROR!!!
                clearScreen()
                selection = input('The link you have selected is not safe, please choose a new link by typing "new"...')
            #driver2.get('https://gomostream.com/show/impractical-jokers/06-18?watching=W54lbvuhNSqXatW6WunzsTyOG')
            #print('https:'+streamingLink)
            #print(replaceBackslash(getCurrentPath()), 'currentPath')
            #selection = input('If you would like to watch something else, just type "new"...')
            if selection == 'new':
                if siteSafety is not False:
                    driver2.quit()
                clearScreen()
            else:
                quit()
    elif selection == 'quit':
        quit()
    