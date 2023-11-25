from facebook_scraper import *
import LinkScraper
from itertools import islice
import requests
from youtube_comment_downloader import *
import xlsxwriter
from bs4 import BeautifulSoup
import TextPreprocessing
import pyfiglet
from apify_client import ApifyClient

def credits():
    print(pyfiglet.figlet_format('                           Credits', width=300))
    time.sleep(1)
    print("                           Program Creator:\n\n                                       Jonas G. Banes\n")
    time.sleep(1)
    print("                           Text Preprocessor & More:\n\n                                       Ignacio Luri, PhD\n")
    time.sleep(1)
    print("                           Facebook Comments Scraper:\n\n                                       Kevin Zúñiga\n")
    time.sleep(1)
    print("                           YouTube Comments Scraper:\n\n                                       Egbert Bouman\n")
    time.sleep(1)
    print("                           Slugify:\n\n                                       The Django Project\n")
    time.sleep(1)
    print("                           Read & Write TXT Files:\n\n                                       Pythontutorial.net\n")
    time.sleep(1)
    print("                           Selenium:\n\n                                       Thoughtworks\n")
    time.sleep(1)
    print("                           Pyfiglet:\n\n                                       Peter Waller\n")
    time.sleep(1)
    print("                           Beautiful Soup:\n\n                                       Leonard Richardson\n")
    time.sleep(1)
    print("                           XLSX Writer:\n\n                                       John McNamara\n")
    time.sleep(1)
    print("                           Requests:\n\n                                       Kenneth Reitz\n")
    time.sleep(1)
    print("                           NLTK:\n\n                                       Steven Bird, Edward Loper, Ewan Klein\n\n")
    time.sleep(1)
    print("                           PyInstaller:\n\n                                       https://pyinstaller.org/en/stable/CREDITS.html\n\n")
    time.sleep(1)
    print("         {")
    print("         Special thanks to Professor Ignacio, my teammates Zuka Mikhelashvili ")
    print("         & Santiago Garcia, Alissa Coronna, my father Jerason, & the ")
    print("         Fall 2023 Text Analytics class. I've been lucky to learn")
    print("         from & alongside you all.")
    print("         }")
    print("\n")

    input("\n\n...Press [ENTER] to return to options menu.")
    print("\n")

def format_comment(c):
    obj = {
        "comment_id": c["comment_id"],
        "commenter_id": c["commenter_id"],
        "commenter_name": c["commenter_name"],
        "comment_text": c["comment_text"],
        "comment_reaction_count": c["comment_reaction_count"] or 0,
        "reply_count": len(c["replies"]) if "replies" in c else 0,
        "comment_time": c["comment_time"],
        "type": "comment"
    }
    if c["comment_reactions"]:
        obj.update(c["comment_reactions"])
    return obj


def format_reply(c):
    obj = {
        "comment_id": c["comment_id"],
        "commenter_id": c["commenter_id"],
        "commenter_name": c["commenter_name"],
        "comment_text": c["comment_text"],
        "comment_reaction_count": c["comment_reaction_count"] or 0,
        "reply_count": len(c["replies"]) if "replies" in c else 0,
        "comment_time": c["comment_time"],
        "type": "reply"
    }
    if c["comment_reactions"]:
        obj.update(c["comment_reactions"])
    return obj

def facebookWriteToXlsx(xlsxfilename, fb_comments, link):
    workbook = xlsxwriter.Workbook(xlsxfilename+'.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "comment_id:")
    worksheet.write(0, 1, "commenter_id:")
    worksheet.write(0, 2, "commenter_name:")
    worksheet.write(0, 3, "comment_text:")
    worksheet.write(0, 4, "comment_reaction_count:")
    worksheet.write(0, 5, "reply_count:")
    worksheet.write(0, 6, "comment_time:")
    worksheet.write(0, 7, "type:")
    worksheet.write(0,8, "link:")

    row = 1

    for x in fb_comments:
        worksheet.write(row, 0, x["comment_id"])
        worksheet.write(row, 1, x["commenter_id"])
        worksheet.write(row, 2, x["commenter_name"])
        worksheet.write(row, 3, (TextPreprocessing.TEXT_PREPROCESS(str.join(" ", x["comment_text"].splitlines()))))
        worksheet.write(row, 4, x["comment_reaction_count"])
        worksheet.write(row, 5, x["reply_count"])
        worksheet.write(row, 6, x["comment_time"])
        worksheet.write(row, 7, x["type"])
        worksheet.write(row, 8, link)
        row += 1
    workbook.close()

def youtubeWriteToXlsx(youtubevideo_filename, link, comments):
    workbook = xlsxwriter.Workbook(youtubevideo_filename)
    worksheet = workbook.add_worksheet()

    row=1

    worksheet.write(0, 0, "text")
    worksheet.write(0, 1, "time")
    worksheet.write(0, 2, "votes")
    worksheet.write(0, 3, "reply")
    worksheet.write(0, 3, "link")

    for comment in islice(comments, 10000000):
        worksheet.write(row, 0, TextPreprocessing.TEXT_PREPROCESS(comment["text"]))
        worksheet.write(row, 1, comment["time"])
        worksheet.write(row, 2, comment["votes"])
        worksheet.write(row, 3, comment["reply"])
        worksheet.write(row, 3, link)
        row += 1
    workbook.close()

def tiktokWriteToXlsx(client, run, xlsxfilename):
    print("\n{Comment Scraper} Scraping finished, creating XLSX file.")
    xlsxfilename = TextPreprocessing.slugify(xlsxfilename)
    if not xlsxfilename.lower().endswith('.xlsx'):
        xlsxfilename += ".xlsx"
    workbook = xlsxwriter.Workbook(xlsxfilename)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "videoWebUrl:")
    worksheet.write(0, 1, "cid:")
    worksheet.write(0, 2, "createTime:")
    worksheet.write(0, 3, "createTimeISO:")
    worksheet.write(0, 4, "text:")
    worksheet.write(0, 5, "likes:")
    worksheet.write(0, 6, "replyCommentTotal:")
    worksheet.write(0, 7, "repliesToId:")
    worksheet.write(0, 8, "uid:")
    worksheet.write(0, 9, "uniqueId:")
    row = 1

    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        worksheet.write(row, 0, item['videoWebUrl'])
        worksheet.write(row, 1, item['cid'])
        worksheet.write(row, 2, item["createTime"])
        worksheet.write(row, 3, item["createTimeISO"])
        worksheet.write(row, 4, TextPreprocessing.TEXT_PREPROCESS(item["text"]))
        worksheet.write(row, 5, item["diggCount"])
        worksheet.write(row, 6, item["replyCommentTotal"])
        worksheet.write(row, 7, item["repliesToId"])
        worksheet.write(row, 8, item["uid"])
        worksheet.write(row, 9, item["uniqueId"])
        row += 1

    workbook.close()
    return(xlsxfilename)

def fileNameCreator(link):
    filename = TextPreprocessing.slugify(link)
    return (filename)

def useTXTFileOrScrape(option):
    while (True):
        lookfortxtfile = str(input(
            '\n\n\nWould you like to use an existing TXT file of links? Otherwise we can scrape new links from a channel or search page.\n\nType [y] to use an existing list.\nType [n] to scrape new links.\n\n[y] or [n]: ')).lower()
        if (lookfortxtfile == 'y') or (lookfortxtfile == 'n'):
            break
        else:
            print('\nWe expected [y] or [n], instead we recieved [' + lookfortxtfile + '], please try again.')
            time.sleep(3)

    if lookfortxtfile == ('y'):
        while (True):
            filename = input('\n\n\nWhat TXT file should be used for links?\n\nFile name: ')

            if not filename.lower().endswith('.txt'):
                filename += ".txt"

            if os.path.exists(filename):
                print("\nTXT file of links found! Loading into memory....")
                linkslist = txtToList(filename)
                break

            else:
                print(
                    '\n' + filename + " was not found. Confirm it is a '.txt' file and in the same folder as this program.")
                time.sleep(3)

    if lookfortxtfile == ('n'):
        if int(option) == 1:
            linkslist = LinkScraper.FaceBookLinksToTXT(option)
            continueOn = continueToScraping()
            if continueOn == 'n':
                input("\n\n...Press [ENTER] to close the program.")
                quit()
        if int(option) == 2:
            linkslist = LinkScraper.YouTubeLinksToTXT(option)
            continueOn = continueToScraping()
            if continueOn == 'n':
                input("\n\n...Press [ENTER] to close the program.")
                quit()
        if int(option) == 3:
            linkslist = LinkScraper.TikTokLinkScraper(option)
            continueOn = continueToScraping()
            if continueOn == 'n':
                input("\n\n...Press [ENTER] to close the program.")
                quit()



    return(linkslist)

def continueToScraping():
    while(True):
        continueOn = str(input(
            '\n\n\nYour links have been scraped. Continue on to scraping comments or resume using the file of links later?\n\nType [y] to continue on to scraping comments.\nType [n] to resume later with the created TXT file list.\n\n[y] or [n]: ')).lower()
        if (continueOn == 'y') or (continueOn == 'n'):
            return (continueOn)
        else:
            print('\nWe expected [y] or [n], instead we recieved [' + continueOn + '], please try again.')
            time.sleep(3)
def txtToList(filename):
    linkslist = []
    with open(filename) as file:
        for line in file:
            linkslist.append(line)
    file.close()
    return (linkslist)

def YOUTUBE_TITLE(string):
    r = requests.get(string)
    soup = BeautifulSoup(r.text, "html.parser")
    link = soup.find_all(name="title")[0]
    title = str(link)
    title = title.replace("<title>","")
    title = title.replace("</title>","")
    return(title)

def facebookCommentScraper(linkslist):
    linknumber=0
    for link in (linkslist):
        linknumber+=1
        if (link.find("facebook.com")==-1) and (link.find("fb.com")==-1 and (link.find("fb.me")==-1)):
            print("\n{Comment Scraper} Link number (" + str(linknumber) + ") [" + link.strip() + "] does not seem to be a Facebook link...skipping.")
            continue

        link = LinkScraper.httpsConfirm(link)

        post_id = [link.strip()]
        filename = fileNameCreator(link)

        if os.path.exists(filename + '.xlsx'):
            print("\n{Comment Scraper} A XLSX file already exists for " + link.strip() + " trying next link, if one exists!")
        else:
            fb_comments = []

            post = next(get_posts(post_urls=post_id, options={"comments": True, "progress": True, "comment_reactors": True}))

            for comment in post["comments_full"]:
                fb_comments.append(format_comment(comment))

                for reply in comment["replies"]:
                    fb_comments.append(format_reply(reply))

            facebookWriteToXlsx(fileNameCreator(filename), fb_comments, link)

    print("\n{Comment Scraper} Accessible comments from all links provided have been scraped successfully.\n\nGood luck on your analysis!\n")

def youtubeCommentScraper(linkslist):

    linknumber=0
    for link in linkslist:
        downloader = YoutubeCommentDownloader()
        linknumber += 1
        if ((link.find("youtube.com")==-1) and (link.find("youtu.be")==-1)) or (link.find("/watch")==-1):
            print("\n{Comment Scraper} Link number (" + str(linknumber) + ") [" + link.strip() + "] does not seem to be a YouTube video link...skipping.")
            continue

        link = LinkScraper.httpsConfirm(link)

        youtubevideo_filename = TextPreprocessing.slugify(YOUTUBE_TITLE(link.strip())) + '.xlsx'

        if os.path.exists(youtubevideo_filename):
            print("\n{Comment Scraper} A XLSX file already exists for " + link.strip() + " trying the next link, if one exists!")
        else:
            comments = downloader.get_comments_from_url(link, sort_by=SORT_BY_POPULAR)
            youtubeWriteToXlsx(youtubevideo_filename, link, comments)
            print("{Comment Scraper} Comments from " + link + " have been scraped and stored in " + youtubevideo_filename + "!\n\nMoving on to the next link, if one exists!")

    print("\n{Comment Scraper} Accessible comments from all links provided have been scraped successfully.\n\nGood luck on your analysis!\n")

def tiktokCommentScraper(linkslist):
    xlsxfilename = str(input("\n\n\nWhat should your Xlsx file of comments be called? (This will include all videos sorted by ID.)\n\nFile name: "))

    apikey = str(input("\n\n\nPlease provide your API key found at [https://console.apify.com/account/integrations] to continue.\n\nAPI Key: "))

    client = ApifyClient(apikey)

    linkslistfixed = []
    linknumber=0

    for link in linkslist:
        linknumber +=1
        if (link.find("tiktok.com")==-1):
            print("\n{PRE-SCRAPE INFO} Link number (" + str(linknumber) + ") [" + link.strip() + "] does not seem to be a TikTok video link...skipping when scraping starts.")
            continue
        else:
            linkslistfixed.append(LinkScraper.httpsConfirm(link.strip()))


    run_input = {
        "postURLs": linkslistfixed,
        "commentsPerPost": 1000000,
        "maxRepliesPerComment": 1000000,
    }


    print("\n\n\n\n\n\n\n{Comment Scraper} Scraping has been started. \nPlease go to [https://console.apify.com/actors/runs] to see progress in realtime.\n\n{Comment Scraper} Please do not close the program while scraping is occurring!\n\n{Comment Scraper} If you want to stop and export comments, \ngo to [https://console.apify.com/actors/runs] and click [ABORT] on this run.")

    run = client.actor("BDec00yAmCm1QbMEI").call(run_input=run_input)

    xlsxfilename = tiktokWriteToXlsx(client, run, xlsxfilename)

    print("\n{Comment Scraper} Accessible comments from the links provided have been scraped successfully.")
    print("\n\nComments can be read in ["+xlsxfilename+"] or at [https://console.apify.com/actors/runs].")
    print("\n\n\n\n\nGood luck on your analysis!\n")


#program starts here!

while(True):
    option = 0
    print(pyfiglet.figlet_format('   Text     Analytics\n  Comment   Scraper', width=300, font='rectangles'))
    option = input('Type [0] for credits....\n\n\n                   What platform would you like to scrape?\n\n                   Type [1] for Facebook\n                   Type [2] for YouTube\n                   Type [3] for TikTok\n\n\nSelection: ')
    if not option.isdigit() or not 4>int(option)>-1:
        print("\n[" + option + "] was not an expected response...please try again.\n\n\n")
        continue
    if int(option) == 0:                         #credits
        credits()
        continue
    if int(option) == 1:                         #Facebook
        linkslist = useTXTFileOrScrape(option)
        facebookCommentScraper(linkslist)
        break

    if int(option) == 2:                         #YouTube
        linkslist = useTXTFileOrScrape(option)
        youtubeCommentScraper(linkslist)
        break

    if int(option) == 3:                         #TikTok
        linkslist = useTXTFileOrScrape(option)
        tiktokCommentScraper(linkslist)
        break

input('\n\n...Press [ENTER] to close the program.')
