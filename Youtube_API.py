import csv
import os
import pickle


from google.auth.transport.requests import Request
import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

k=0
title = None
class_name =None

class Youtube_API:

    # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
    # the OAuth 2.0 information for this application, including its client_id and
    # client_secret.
    CLIENT_SECRETS_FILE = "client_secret.json"

    # This OAuth 2.0 access scope allows for full read/write access to the
    # authenticated user's account and requires requests to use an SSL connection.
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'



    def get_authenticated_service(self):

        credentials = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)
        #  Check if the credentials are invalid or do not exist
        if not credentials or not credentials.valid:
            # Check if the credentials have expired
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, self.SCOPES)
                credentials = flow.run_console()

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)

        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials = credentials)




    def get_channel_name(self, videoid, **kwargs):

        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        service = self.get_authenticated_service()

        global title
        results = service.search().list(**kwargs).execute()
        final_result = []
        for item in results:
            # title = item['snippet']['title']
            # video_id = item['id']['videoId']
            names = service.channels().list(part='snippet, contentDetails, statistics', id=videoid).execute()
            # make a tuple consisting of the video id, title, comment and add the result to
            # channel_list = names[item]  #this will give a list of tuples
            # print(names)
            for i in names['items']:
                title = i['snippet']['title']

        return title



    def get_video_comments(self,service, **kwargs):
        comments = []
        results = service.commentThreads().list(**kwargs).execute()
        # service.channel().list.execute()
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        return comments


    def write_to_csv(self,comments):
        global k

        with open('comments.csv', 'a+',encoding='utf8') as comments_file:
            comments_writer = csv.writer(comments_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if k==0:
                comments_writer.writerow(['Video ID','Comment'])
            commentlist = []
            k +=1

            for row in comments:

                if row[1] in commentlist:
                    continue

                commentlist.append(row[1])

                # convert the tuple to a list and write to the output file
                comments_writer.writerow(list(row))



    def search_videos_by_keyword(self,service,videoid,**kwargs):
        results = service.search().list(**kwargs).execute()
        final_result = []
        for item in results:

            comments = self.get_video_comments(service, part='snippet', videoId=videoid, textFormat='plainText',order='relevance',maxResults = 10)
            # make a tuple consisting of the video id, title, comment and add the result to
            final_result.extend([(videoid,comment) for comment in comments])  #this will give a list of tuples

        self.write_to_csv(final_result)


# if __name__ == '__main__':
#     # When running locally, disable OAuthlib's HTTPs verification. When
#     # running in production *do not* leave this option enabled.
    def main_api(self):

        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        service = self.get_authenticated_service()
        # keyword = input('Enter a keyword:')
        video_id = []
        d = open("IdsOFvideo.csv")
        reader = csv.reader(d)

        for row in reader:
            # print(row[0])
            video_id.append(row[0])

        if '' in video_id:
            video_id.remove('')


        for i in video_id[1:]:
            idchannel = i
            # print(i)
            self.search_videos_by_keyword(service,idchannel, q=idchannel, part='snippet', eventType='completed', type='video')
