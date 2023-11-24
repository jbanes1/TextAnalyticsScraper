import re
import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import TextPreprocessing


def scrollToBottom(links, driver, option):
    if int(option) == 3: #Tiktok handler
        retryattempts = 0
        last_height = -1
        links_appended = addLinksToList(links, driver)
        while True:
            # Scroll down to bottom
            links_appended = addLinksToList(links_appended, driver)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

            # Wait to load page
            time.sleep(3)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)
            links_appended = addLinksToList(links_appended, driver)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(3)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if (new_height == last_height):
                time.sleep(2)
                retryattempts += 1
                print("\nRetrying scrolling down further...")
            if retryattempts > 2:
                print("\nCannot scroll any further, returning list of links!")
                return (links_appended)
            last_height = new_height
    else:                                                #other platform handler
        time.sleep(2)
        stopheight = -1
        retryattempts = 0
        links_appended = addLinksToList(links, driver)
        while (True):
            time.sleep(3)
            height = driver.execute_script("return document.body.scrollHeight")
            links_appended = addLinksToList(links_appended, driver)
            pageDown(driver)

            if (int(option) != 2 and (int(height) == 0 or height == stopheight)):
                time.sleep(2)
                retryattempts += 1
                print("\nRetrying scrolling down further...")
            if retryattempts > 2:
                print("\nCannot scroll any further, returning list of links!")
                return (links_appended)
            stopheight = height


def pageDown(driver):
    time.sleep(2)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

def pageUp(driver):
    time.sleep(2)
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_UP)

def httpsConfirm(link):
    if not (link.startswith("https://") or link.startswith("http://")):
        link = "https://" + link
    return(link)

def addLinksToList(links, driver):
    time.sleep(2)
    links_appended = links
    elements = driver.find_elements(By.XPATH, "//a[@href]")
    for i in elements:
        item = i.get_attribute('href')
        if re.search(r'/photos/|/photo.php|fbid=|/watch|/video/', str(item)):
            if re.search(r'comment_id=',str(item)):
                continue
            else:
                links_appended.append(item)
        else:
            continue
    return(links_appended)

def removeduplicate(data):
    countdict = {}
    for element in data:
        if element in countdict.keys():
            countdict[element] += 1
        else:
            countdict[element] = 1
    data.clear()
    for key in countdict.keys():
        data.append(key)
    return(data)

def removeDuplicateYoutubeID(links):
    temp = ['I am nessesary to the FOR loop below (Jonas did not figure out a better way.) If you are curious, try removing me and seeing how the result changes']
    for x in links:
        if x not in temp:
            for tempid in temp:
                id = str.split(x, '=')[1]
                if any(id in s for s in temp):
                    break
                else:
                    if x.endswith('s'):
                        break
                    else:
                        temp.append(x)
    del temp[0]
    return(temp)
def listToTXT(filename, links):
    with open(filename, 'w') as fp:
        for item in links:
            # write each item on a new line
            fp.write("%s\n" % (str(item)))
        print('\nLinks were stored in ' + filename + ', moving on to scraping comments from these links!\n')

def txtFileNamer():
    txtFileName = str(input('\n\n\nWhat should we call the .txt file of links? \n\nFile name: '))
    txtFileName= txtFileName.replace('.txt','')
    txtFileName = (TextPreprocessing.slugify(txtFileName.strip()) + ".txt")
    print("\nCreating " + txtFileName + " now!")
    return(txtFileName)

def scrollOption():
        while (True):
            pagedownorscrollbottom = str(input(
                '\n\n\nWould you like to specify number of [Page Down]s to scrape, or try to scrape to the end of the page?\n\nType [p] to specify page count.\nType [b] to attempt scrolling to the bottom.\n\n(If improperly utilized, option [b] could result in an infinite loop.)\n\n[p] or [b]: ')).lower()
            if (pagedownorscrollbottom == 'p') or (pagedownorscrollbottom == 'b'):
                return (pagedownorscrollbottom)
            else:
                print(
                    '\nWe expected [p] or [b], instead we recieved [' + pagedownorscrollbottom + '], please try again.')
                time.sleep(3)

def numberPagesToScroll():
    while (True):
        pages = input('\n\n\nHow many times should we press [Page Down] to load more links? \n\nPages: ')
        if not pages.isdigit():
            print("\n[" + pages + "] does not seem to be a number...please try again.")
            continue
        else:
            break
    return(pages)

def pageToLinkScrape(option):
    if (int(option) == 1): #Facebook
        while (True):
            pagetoscrape = (input('\n\n\nProvide a Facebook profile /photos/ page to scrape photo posts for comments on.\n(e.g. https://www.facebook.com/McDonalds/photos)\n\nLink: '))
            if (pagetoscrape.lower().find("facebook.com") == -1) and (pagetoscrape.lower().find("fb.com") == -1 and (pagetoscrape.lower().find("fb.me") == -1)) or ((pagetoscrape.lower().startswith('https://') is False) and ((pagetoscrape.lower().startswith('http://') is False) and (pagetoscrape.lower().startswith('www.f')is False))):
                print("\n[" + pagetoscrape + "] does not seem to be a Facebook link...please try again.")
                continue
            if ((pagetoscrape.lower()).find("photos") == -1):
                while (True):
                    yesorno = str(input("\n\n\n[" + pagetoscrape + "] does not seem to be a /photos/ Facebook page.\n\nType [y] to attempt scraping anyway (behavior not tested.)\nType [n] to input a different link.\n\n[y] or [n]: "))
                    if (yesorno == 'y'):
                        return(pagetoscrape)
                    if (yesorno == 'n'):
                        continue
                    else:
                        print(
                            '\nWe expected [y] or [n], instead we recieved [' + yesorno + '], please try again.')
                        time.sleep(3)
            else:
                return (pagetoscrape)

    if (int(option) == 2): #YouTube
        while (True):
            pagetoscrape = (str(input(
                '\n\n\nProvide a YouTube profile or search page to scrape links for comments on.\n(e.g. https://www.youtube.com/results?search_query=mcdonalds)\n\nLink: ')))
            if ((pagetoscrape.lower().find("youtube.com") == -1) and (pagetoscrape.lower().find("youtu.be") == -1)) or ((pagetoscrape.lower().startswith('https://') is False) and ((pagetoscrape.lower().startswith('http://') is False) and (pagetoscrape.lower().startswith('www.y')is False))):
                print("\n[" + pagetoscrape + "] does not seem to be a YouTube link...please try again.")
                continue
            else:
                return(pagetoscrape)

    if (int(option) == 3): #TikTok
        while (True):
            pagetoscrape = (str(input(
                '\n\n\nProvide a TikTok profile or search page to scrape links for comments on.\n(e.g. https://www.tiktok.com/@mcdonalds?lang=en)\n\nLink: ')))
            if (pagetoscrape.lower().find("tiktok.com") == -1) or ((pagetoscrape.lower().startswith('https://') is False) and ((pagetoscrape.lower().startswith('http://') is False) and (pagetoscrape.lower().startswith('www.t')is False))):
                print("\n[" + pagetoscrape + "] does not seem to be a TikTok link...please try again.")
                continue
            else:
                return(pagetoscrape)

def FaceBookLinksToTXT(option):
    links = []

    pagetoscrape = httpsConfirm(pageToLinkScrape(option)).strip()
    pagedownorscrollbottom = scrollOption()

    if (pagedownorscrollbottom =='p'):
        pages = numberPagesToScroll()

    txtFileName = txtFileNamer()

    driver = webdriver.Chrome()
    driver.get(pagetoscrape)
    time.sleep(3)

    driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]").click() #Closes login window.
    time.sleep(3)

    if (pagedownorscrollbottom == 'b'): #Scroll to bottom then remove duplicates from the list
        links = removeduplicate(scrollToBottom(links, driver, option))

    if (pagedownorscrollbottom == 'p'): #Page down using [PAGE DOWN] key; each operation pause 1 second before adding links to list.
        for i in range(int(pages)):
            time.sleep(1)
            links = addLinksToList(links, driver)
            pageDown(driver)
        links = removeduplicate(links)

    driver.close() #Close browser

    listToTXT(txtFileName, links)

    return (links)

def YouTubeLinksToTXT(option):
    links = []
    pagetoscrape = httpsConfirm(pageToLinkScrape(option))
    pages = numberPagesToScroll()
    txtFileName = txtFileNamer()


    driver = webdriver.Chrome()
    driver.get(pagetoscrape)
    time.sleep(3)

    for i in range(int(pages)):
        links = addLinksToList(links, driver)
        pageDown(driver)
        time.sleep(1)
    links = removeDuplicateYoutubeID(removeduplicate(links))

    driver.close()

    listToTXT(txtFileName, links)

    return (links)

def TikTokLinkScraper(option):
    links = []

    pagetoscrape = httpsConfirm(pageToLinkScrape(option)) #What page to scrape links from; does it start with HTTPS? (Selenium requirement...)
    pagedownorscrollbottom = scrollOption() #Option for profile pages to be scrolled to bottom or pages of search results.

    if (pagedownorscrollbottom == 'p'):
        pages=numberPagesToScroll() #If using pages, not scroll to bottom, how many pages?

    txtFileName = txtFileNamer() #Name your TXT file of links (the TXT file is for tracing your work or resuming paused scraping.)


    driver = webdriver.Chrome() #Open browser
    driver.get(pagetoscrape)
    time.sleep(5)

    if (pagedownorscrollbottom == 'b'): #Scroll to bottom then remove duplicates from the list
        links = removeduplicate(scrollToBottom(links, driver, option))

    if (pagedownorscrollbottom == 'p'): #Page down using [PAGE DOWN] key; each operation pause 1 second before adding links to list.
        for i in range(int(pages)):
            time.sleep(1)
            links = addLinksToList(links, driver)
            pageDown(driver)
        links = removeduplicate(links)

    driver.close() #Close browser

    listToTXT(txtFileName, links)

    return (links)




