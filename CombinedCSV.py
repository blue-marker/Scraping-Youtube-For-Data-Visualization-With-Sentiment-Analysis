import csv
import json

class CombinedCSV:

   def __init__(self):

      with open('Video_Details.csv', 'r', encoding = "utf8") as a:
         reader = csv.reader(a, delimiter=",")
         # print(reader)
         videos = list(reader)     #this is a list of lists
         # print(videos)

      with open('Durations.csv', 'r', encoding = "utf8") as b:
         reader = csv.reader(b, delimiter = ",")
         duration = list(reader)  #this is a list of lists


      with open('Categories.csv', 'r', encoding = "utf8") as c:
         reader = csv.reader(c, delimiter = ",")
         des= list(reader)      #this is a list of lists

      with open('Hashtags.csv', 'r', encoding = "utf8") as c:
         reader = csv.reader(c, delimiter = ",")
         tags= list(reader)

      with open('HashInfo.csv', 'r', encoding = "utf8") as c:
         reader = csv.reader(c, delimiter = ",")
         infotags= list(reader)

      #since Video_Details & Durations scrapped separately
      #it may happen that both may not align properly to combine

      with open('combined.csv', 'w',encoding = "utf8") as f:  #combined csv file

         writer = csv.writer(f, delimiter = ",")

         for i in range(0,len(videos)):
            temp_list = []
            try:
               temp_list.extend(videos[i])
            except:
               temp_list.append(None)
            try:
               temp_list.extend(duration[i])
            except:
               temp_list.append(None)
            try:
               temp_list.extend(des[i])
            except:
               temp_list.append(None)
            try:
               temp_list.extend(tags[i])
            except:
               temp_list.append(None)
            try:
               temp_list.extend(infotags[i])
            except:
               temp_list.append(None)

            writer.writerow(temp_list)


#For converting csv to json
class Csv_json():

   def __init__(self):
      csvfile = open('combined.csv', 'r', encoding="utf8")
      jsonfile = open('file.json', 'w', encoding="utf8")

      fieldnames = (
      'Channel_Name', 'Subscribers', 'Video Titles', 'Video Description', 'Published Date', 'Views', 'Likes',
      'Dislikes', 'Duration', 'Category', 'HashTags', 'HashInfo')
      reader = csv.DictReader(csvfile, fieldnames)

      next(reader)  # ignores the first line
      for row in reader:
         json.dump(row, jsonfile)
         jsonfile.write('\n')

      csvfile.close()
      jsonfile.close()

