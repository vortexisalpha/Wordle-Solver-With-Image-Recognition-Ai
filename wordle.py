from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from GetColourOfImage import *
import random
from wordListFile import *

width = 2400
height = 1696
windowDimentions = (width,height) 

top = 305
left = 865
sideLength = 135

#sets up chrome driver
PATH = "/usr/local/bin/chromedriver"
driver = webdriver.Chrome(PATH)


#gets the word list in a python list from the file
wordList = wordList[0]
#gets onto website

driver.get("https://www.nytimes.com/games/wordle/index.html")
driver.find_element_by_xpath('//*[@id="pz-gdpr-btn-accept"]').click()
elem = driver.find_element_by_xpath('/html/body')
action_chains = ActionChains(driver)
action_chains.move_to_element_with_offset(elem, 660, 420).perform()
action_chains.click().perform()

def inputWord(driver, word):
    actions = ActionChains(driver)
    actions.send_keys(str(word))
    actions.send_keys(Keys.ENTER)
    actions.perform()

def getColours(name,repeatedLetter,wordList):
    colour = outputColour(str(name))
    if colour[:3] == '3a3'or colour[:3] == '393' or  (colour[0] == '7' and colour[2] == '7'): #black (for not in the word)
        for i in range(len(wordList)-1):
            
            if wordList[i] == repeatedLetter:
                firstOne = True
                break
        if not firstOne:
            return 'b'
    elif colour[:3] == 'b09' or  (colour[0] == 'c' and colour[2] == 'b'): #yellow (for in the word but not in the right place)
        return 'y'
    elif colour[:3] == '618' or (colour[0] == '7' and colour[2] == 'a') or (colour[0] == 'f' and colour[3] == 'f') or (colour[0] == 'd' and colour[3] == 'd'): #green (in the word, in the right place)
        return 'g'

def removeWords(colourArray,wordList,wordForInput):
    wordsToRemove = []
    for i in range(len(colourArray)):
        #if the couour is yellow take all words out that have the letter in that spot
        if colourArray[i] == 'y':
            for word in wordList:
                if word[i] == wordForInput[i]:
                    wordsToRemove.append(word)
                if wordForInput[i] not in word:
                    wordsToRemove.append(word)
        if colourArray[i] == 'b':
            for word in wordList:
                for letter in word:
                    if letter == wordForInput[i]:
                        if word in wordList:
                            wordsToRemove.append(word)
        if colourArray[i] == 'g':
            for word in wordList:
                if word[i] != wordForInput[i]:
                    wordsToRemove.append(word)

    for i in range(len(wordList)-1,-1,-1):
        if wordList[i] in wordsToRemove:
            print(wordList[i])
            wordList.remove(wordList[i])
    return wordList


wordForInput = 'shake'
k = 0
colourArray = []
while colourArray!= ['g','g','g','g','g']or k<5:
    
    time.sleep(1)
    inputWord(driver,wordForInput)
    wordList.remove(wordForInput)
    time.sleep(2)
    repeatedLetter = ''
    for i in range(len(wordForInput)-1):
        for j in range(len(wordForInput)-1):
            if wordForInput[i] == wordForInput[j]:
                repeatedLetter = wordForInput[i]
    element = driver.find_element_by_xpath('/html/body')
    nameArray = ['11','12','13','14','15']
    colourArray = []
    for i in range(5):   
        getImage(driver, element,left+ sideLength*i,top +sideLength*k ,nameArray[i])
        colourArray.append(getColours(nameArray[i],repeatedLetter,wordForInput))

    print(colourArray)
    wordList = removeWords(colourArray,wordList,wordForInput)
    if len(wordList) > 1:
        wordForInput = wordList[random.randint(0,len(wordList)-1)]
    else:
        print(wordList)
        wordForInput = wordList[0]
    k+=1
    print(wordList)
driver.quit()
print('done')