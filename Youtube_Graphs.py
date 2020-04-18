import pandas as pd
from matplotlib import pyplot as plt
import csv
import mplcursors
import json


name_list=[]

class Youtube_Graphs:

    def scatterPlot(self):


        #for getting list of channels
        csvfile = open('Channel_Names.csv', 'r',encoding="utf8",errors='ignore')

        fieldnames=('Channel Name','Subscribers')
        reader= csv.DictReader(csvfile,fieldnames)


        next(reader)
        for i in reader:
            name_list.append(i['Channel Name'])

        #for getting list of channel name and views for plotting them on x and y axis
        data = pd.read_csv('combined.csv')

        likes2= data['Likes']
        views2= data['View']
        channel_name2= data['Channel_Name']
        tags0= data['HashTags']

        #converting class pandas.core.series into list for plot
        likes=list(likes2)
        views=list(views2)
        channel_name= list(channel_name2)
        labels=list(tags0)


    #below code removes any filler channel names in the channel_name list
        filler_list=[]
        for j in range(len(channel_name)):
            for i,name in enumerate(channel_name):
                if name not in name_list:
                    channel_name.remove(name)
                    filler_list.append(i)   #storing the index number of filler channel names
                else:
                    continue

    #Views belonging to filler channel names
        filler_views=iter(filler_list)

        for i in range(len(filler_list)):
            views.pop(next(filler_views))

        # Likes belonging to filler channel names
        filler_likes=iter(filler_list)

        for i in range(len(filler_list)):
            likes.pop(next(filler_likes))


        #Scatter Plot

        plt.style.use('seaborn')

        t = plt.scatter(channel_name ,views,c=likes,cmap='summer',edgecolors='black',linewidths=1,alpha=0.75)

        plt.title('Youtube Videos')
        plt.xlabel('Channel Names')
        plt.xticks(channel_name, [str(i) for i in channel_name], rotation=90)
        # plt.tick_params(axis='x', which='major')
        plt.ylabel('Views')

        cbar= plt.colorbar()
        cbar.set_label('Likes Gradient')
        plt.tight_layout()  #for padding the labels

        c2 = mplcursors.cursor(t,hover=True)

        @c2.connect("add")
        def _(sel):
            sel.annotation.get_bbox_patch().set(fc="red")
            sel.annotation.arrow_patch.set(arrowstyle='wedge', fc="white", alpha=0.3)  #arrowstyle - simple,wedge,fancy
            # sel.annotation.set_text(data['HashTags'][sel.target.index])
            sel.annotation.set_text(data['HashInfo'][sel.target.index])

        plt.show()



    def piePlot(self):

        jsonfile = open('file.json', 'r', encoding='utf8')
        listOfCat = []
        listOftags = []
        for row in jsonfile:
            data = json.loads(row)

            try:
                listOfCat.append(data['Category'])
            except:
                listOfCat.append(None)
            try:
                listOftags.append(data['HashTags'])
            except:
                listOftags.append(None)

        r = set(listOfCat)
        t = list(r)
        u = {}
        for i in t:
            u[i] = listOfCat.count(i)

        keys = []
        values = []
        # print(u)
        for k, v in u.items():
            keys.append(k)
            values.append(v)

        plt.style.use('fivethirtyeight')

        plt.pie(values, labels=keys, wedgeprops={'edgecolor': 'black'})

        plt.title('Trending Categories')
        plt.tight_layout()

        plt.show()