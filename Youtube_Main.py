# imports for web scrapping
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

from matplotlib import pyplot as plt
import csv
import re

import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *  # for combobox


from Youtube_API import Youtube_API
from Youtube_Graphs import Youtube_Graphs
from CombinedCSV import CombinedCSV,Csv_json
from Live_Tweetstream import Tweetstream, Tweetgraph
from Sentiment_Bargraph import Sentiment_Bargraph

youtube_api = Youtube_API()
youtube_graph = Youtube_Graphs()
twitter_stream = Tweetstream()
twitter_graph = Tweetgraph()

#imports for threading
import threading
import inspect
import ctypes

import os

# 1
Channel_Name = []
Subscribers = []
Video_ID = []
Video_ChannelID = []

# 2
video_dura = []

# 3
video_title = []
video_info=[]
video_views = []
video_likes = []
video_dislikes = []
video_category=[]
hashtag=[]
hash_info=[]

# 4
video_date = []
link_list = []


#codes for threading
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class Thread(threading.Thread):

    def _get_my_tid(self):
        """determines this (self's) thread id"""
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        raise AssertionError("could not determine the thread's id")

    def raise_exc(self, exctype):
        """raises the given exception type in the context of this thread"""
        _async_raise(self._get_my_tid(), exctype)

    def terminate(self):
        """raises SystemExit in the context of the given thread, which should
        cause the thread to exit silently (unless caught)"""
        self.raise_exc(SystemExit)


class Scrap():

    def __init__(self):

        os.chdir('C:/Users/vinod salian/Data Science/Youtube_PYProject/Youtube_Documents')
        driver = webdriver.Chrome()

        if trend() != None:
            driver.get(trend())  # opens up main trending youtube page
        else:
            driver.get(categ())  #opens up youtube page according to category selected

        user_data2 = driver.find_elements_by_xpath('//*[@id="video-title"]')  #gets a list of all video links on that pages
        user_data = user_data2[0:int(spin.get())]  #gets only selected no of video links

        # print(user_data)

        if trend() == True:
            source = requests.get(trend()).text
            soup = BeautifulSoup(source, 'lxml')
        else:
            source = requests.get(categ()).text
            soup = BeautifulSoup(source, 'lxml')


        #the below div class contain video title, duration and channel name
        channelList = soup.findAll('div', attrs={'class': "yt-lockup-content"}) #gives list of all video info on that page

        for channel in channelList[0:int(spin.get())]: #gets only required selected no of videos

            #1st Level Scraping
            try:
                duration_span = channel.find('span', attrs={'class': 'accessible-description'})
                duration_box = duration_span.text.strip('- Duration:')

                video_dura.append(duration_box)
            except:
                video_dura.append(None)

        df = pd.DataFrame({'Duration': video_dura})
        df.to_csv('Durations.csv', index=False, encoding='utf-8')

        search_links = []

        for i in user_data: #list of selected video links
            search_links.append(i.get_attribute('href'))   #stores a list of video links

            while None in search_links:
                search_links.remove(None)


        # 2st level Scrapping

        # below code opens up one by one each video link and get all the info pertaining to that video
        for link in search_links:

            source = requests.get(link).text
            soup = BeautifulSoup(source, 'lxml')

            try:
                subs = soup.find('span', attrs={'class': 'yt-subscription-button-subscriber-count-branded-horizontal yt-subscriber-count'}).text.strip()
                Subscribers.append(subs)
            except:
                Subscribers.append(0)

            try:
                info = soup.find('div', attrs={'id': "watch-description-text"}).text.strip()
                info1 = ''.join(re.sub('[€–º™â,"*+;|_.%]*', '', info))
                info2 = ''.join(re.sub('(http://|https://){1}[A-Za-z]+[/]*[.a-zA-Z/]*[:]*', '', info1))
                info3 = ''.join(re.sub(':*', '', info))
                video_info.append(info2)
            except:
                video_info.append(None)

            try:
                title = soup.find('div', attrs={'id': 'watch-headline-title'}).text.strip()
                title1 = ''.join(re.sub('[€–º™â,"*+;|_.%]*', '', title))
                video_title.append(title1)
            except:
                video_title.append(None)

            try:
                views_box = soup.find('div', attrs={'class': 'watch-view-count'}).text.strip('views')
                views = views_box.replace(',', '')
                video_views.append(views)
            except:
                video_views.append(0)

            try:
                likes = soup.find('button', attrs={"title": "I like this"})
                likes2 = likes.text.strip()
                likes3 = likes2.replace(',', '')
                video_likes.append(int(likes3))
            except:
                video_likes.append(0)

            try:
                dislikes = soup.find('button', attrs={"title": "I dislike this"})
                dis = dislikes.text.strip()
                dislikes3 = dis.replace(',', '')
                video_dislikes.append(int(dislikes3))
            except:
                video_dislikes.append(0)


            try:
                date = soup.find('div', attrs={'id': 'watch-uploader-info'})
                date_text = date.text.strip()

                if 'Published on' in date_text:
                    date_box = date_text.strip('Published on')
                elif 'Streamed live on' in date_text:
                    date_not = date_text.strip('Streamed')
                    date_box = date_not.strip('live on')
                elif 'Premiered' in date_text:
                    date_box = date_text.strip('Premiered ')

                video_date.append(date_box)
            except:
                video_date.append(None)

            try:
                ID = soup.find('div', attrs={'class': 'watch-main-col'})
                IDS = ID.find('meta', attrs={'itemprop': "videoId"})
                Video_ID.append(IDS['content'])

            except:
                Video_ID.append(None)

            try:
                f = soup.find('div', attrs={'class': 'watch-main-col'})
                g = f.find('meta', attrs={'itemprop': "channelId"})
                Video_ChannelID.append(g['content'])
            except:
                Video_ChannelID.append(None)

            try:
                for cat in soup.findAll('li', attrs={'class': "watch-meta-item yt-uix-expander-body"}):
                    if cat.h4.text.strip() == 'Category':
                        bat = cat.find('ul', attrs={'class': "content watch-info-tag-list"}).text.strip()
                        # print(bat)
                        video_category.append(bat)
            except:
                video_category.append(None)

            try:
                for hash in soup.findAll('span', attrs={'class': 'standalone-collection-badge-renderer-text'}):
                    for o in hash.findAll('a', attrs={'class': 'yt-uix-sessionlink'}):
                        dat = o.text.strip()
                        hashtag.append(dat)
                    break
                else:
                    hashtag.append(None)
            except:
                hashtag.append(None)


            try:

                desc = soup.find('div', attrs={'id': "watch-description-text"})
                h = []
                for hash in desc.findAll('a', attrs={'class': 'yt-uix-sessionlink'}):
                    g = hash.text.strip()

                    if g[0] == '#':
                        pass
                    else:
                        continue
                    h.append(g)

                hash_info.append(h)
            except:
                hash_info.append(None)


        df = pd.DataFrame({'VideoID': Video_ID})
        df.to_csv('IdsOFvideo.csv', index=False, encoding='utf-8')

        df = pd.DataFrame({'Video Description': video_info})
        df.to_csv('Video_Descriptions.txt', index=False, encoding='utf-8')

        df = pd.DataFrame({'Video Titles': video_title})
        df.to_csv('Video_Titles.txt', index=False, encoding='utf-8')

        df = pd.DataFrame({'Category': video_category})
        df.to_csv('Categories.csv', index=False, encoding='utf-8')

        df = pd.DataFrame({'HashTags': hashtag})
        df.to_csv('Hashtags.csv', index=False, encoding='utf-8')

        df = pd.DataFrame({'HashInfo': hash_info})
        df.to_csv('HashInfo.csv', index=False, encoding='utf-8')


        self.channel_names()

        for i in Channel_Name:
            print(i)

        df = pd.DataFrame({'Channel Name':Channel_Name,'Subscribers': Subscribers})
        df.to_csv('Channel_Names.csv', index=False, encoding='utf-8')

        df = pd.DataFrame({'Channel_Name': Channel_Name, 'Subscribers': Subscribers, 'Video Titles': video_title,
                           'Video Description': video_info, 'Published Date': video_date, \
                           'View': video_views, 'Likes': video_likes, 'Dislikes': video_dislikes})
        df.to_csv('Video_Details.csv', index=False, encoding='utf-8')


        CombinedCSV()
        Csv_json()
        youtube_api.main_api()

        changetext()
        self.hashlist()
        driver.close()



    def channel_names(self):

        global Channel_Name

        for ids in Video_ChannelID:
            k = youtube_api.get_channel_name(ids, q=ids, part='snippet', eventType='completed', type='video')
            Channel_Name.append(k)

    # below code is for creating a list of channel names
    # to be used in combobox
    names = []

    def hashlist(self):
        global names
        csvfile = open('Hashtags.csv', 'r', encoding="utf8", errors='ignore')
        reader = csv.reader(csvfile)
        next(reader)
        for i in reader:
            if i == None:
                continue
            # print(i['Channel Name'])
            names.append(i[0])

# Changes Text on Scrap Button after Scrap
def changetext():
    button1['text'] = ' Scrapped ! '
    messagebox.showinfo('Scrapped', "Your data is scrapped !")

# below code is for naming & saving plots
q = 0
def save():
    os.chdir('C:/Users/vinod salian/Data Science/Youtube_PYProject/Youtube_Graphs')
    global q
    q += 1

    plt.savefig('Channel_Analysis%d.png' % (q))
    plt.close()
    os.chdir('C:/Users/vinod salian/Data Science/Youtube_PYProject/Youtube_Documents')

# Select By Trending
def trend():
    if btn1.get():
        throw = str(btn1.get())
        return throw
    else:
        return None

# Select By Category
def categ():
    search = str(combo0.get())
    http = 'https://www.youtube.com/results?search_query=' + search

    return http



stop_threads = False

def live_stream():
    while True:
        g = str(combo.get())
        twitter_stream.twitty(g.strip('#'))
        global stop_threads
        if stop_threads:
            break

def live_graph():
    while True:
        twitter_graph.livegraph()
        global stop_threads
        if stop_threads:
            break

t1 = None
t2 = None

def parallel():
    global stop_threads
    global t1
    global t2

    stop_threads = False
    y = open('tweets.csv', 'w')
    t1 = Thread(target=live_stream)
    t2 = Thread(target=live_graph)
    t1.start()
    t2.start()

def kill():
    global stop_threads
    stop_threads = True
    t1.terminate()
    t1.join()
    t2.terminate()
    t2.join()
    plt.close()


#Main GUI Code
window = tk.Tk()
window.title('YouTube Scrap')
window.geometry("600x800")
window.config(cursor="hand2")

# Main Youtube Image
icon = tk.PhotoImage(file="C:/Users/vinod salian/Data Science/experimental_programs/web_Scrapping/images/youtube.png")
label0 = tk.Label(window, image=icon, height=200, width=600)
label0.pack()
label0.grid(column=1, row=0)

# Headline
label1 = tk.Label(text='Welcome to Youtube Videos Analysis', font=("Arial", 20))
label1.place(x=70, y=220)
btn1 = tk.StringVar()

# trending image
icon1 = tk.PhotoImage(file="C:/Users/vinod salian/Data Science/experimental_programs/web_Scrapping/images/fire.png")

# Radio Buttons For Trending Videos
rad1 = Radiobutton(window, text='Trending', value='https://www.youtube.com/feed/trending', variable=btn1, image=icon1,
                   compound="left")
rad1.place(x=45, y=276)

rad2 = Radiobutton(window, text='Music_Trend',
                   value='https://www.youtube.com/feed/trending?bp=4gIuCggvbS8wNHJsZhIiUExGZ3F1TG5MNTlha3czbTFWa1JnalJQSTlkZlpMVnpYTA%3D%3D',
                   variable=btn1, image=icon1, compound="left")
rad2.place(x=180, y=276)

rad3 = Radiobutton(window, text='News_Trend',
                   value='https://www.youtube.com/feed/trending?bp=4gIuCggvbS8wNWpoZxIiUEwzWlE1Q3BOdWxRa0tTSWpjcjNuV1k1RW95c0dfeFdpbg%3D%3D',
                   variable=btn1, image=icon1, compound="left")
rad3.place(x=325, y=276)

rad4 = Radiobutton(window, text='Movies_Trend',
                   value='https://www.youtube.com/feed/trending?bp=4gIuCggvbS8wMnZ4bhIiUExuUzZNOHZRRmtkSXUyWDZyb3RCZ3pIT1c3ZzRxTjh6Vw%3D%3D',
                   variable=btn1, image=icon1, compound="left")
rad4.place(x=465, y=276)

# Category Select
categories = ['Python Tutorial', 'Science Experiments', 'Music Videos', 'Food & Travel', 'Siraj Raval']
combo0 = Combobox(window, values=categories, postcommand=lambda: combo0.configure(values=categories))
combo0.place(x=238, y=320)

# No of videos
spin = tk.Spinbox(window, from_=0, to=10, width=5)
spin.place(x=288, y=355)


# Scrap Button
icon2 = tk.PhotoImage(file="C:/Users/vinod salian/Data Science/experimental_programs/web_Scrapping/images/We2.png")
button1 = tk.Button(text=' Go Scrap ! ', image=icon2, compound="left", relief='raised', font=("Arial 12 bold"),
                    borderwidth=2, command=Scrap)
button1.place(x=241, y=400)

# Scatter Plot button
icon3 = tk.PhotoImage(
    file="C:/Users/vinod salian/Data Science/experimental_programs/web_Scrapping/images/darkgraph.png")
button2 = tk.Button(text=' Scatter Plot ', relief='raised', font=("Arial 12 bold"), image=icon3, compound="left",
                    borderwidth=2, command=youtube_graph.scatterPlot)
button2.place(x=247, y=450)

names = []
# Hashtag Selection
combo = Combobox(window, values=names, postcommand=lambda: combo.configure(values=names))
combo.place(x=241, y=500)

# Scatter plot button for individual channel
button3 = tk.Button(text='Category Pie', font=('Arial 11 bold'), command=youtube_graph.piePlot)
button3.place(x=258, y=537)

# Save Button
icon4 = tk.PhotoImage(file="C:/Users/vinod salian/Data Science/experimental_programs/web_Scrapping/images/bell0.png")
button4 = tk.Button(text='Save Plot ', font=("Arial 9 bold"), image=icon4, compound="left", command=save)
button4.place(x=268, y=740)

icon5 = tk.PhotoImage(
    file="C:/Users/vinod salian/Data Science/experimental_programs/web_Scrapping/images/darkgraph.png")
button5 = tk.Button(text=' Senitment Graph ', relief='raised', font=("Arial 12 bold"), compound="left",
                    borderwidth=2, command=Sentiment_Bargraph)
button5.place(x=240, y=575)

button6 = tk.Button(text=' Live Tweet ', relief='raised', font=("Arial 12 bold"), compound="left",
                    borderwidth=2, command=parallel)
button6.place(x=258, y=640)

button7 = tk.Button(text=' Stop Tweet ', relief='raised', font=("Arial 8 "), compound="left",
                    borderwidth=2, command=kill)
button7.place(x=272, y=676)

window.mainloop()


