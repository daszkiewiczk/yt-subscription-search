# -*- coding: utf-8 -*-

# Sample Python code for youtube.subscriptions.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def authenticate():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    return youtube;

def fetch_subs(youtube):
    subs = []
    
    request = youtube.subscriptions().list(
        part="id",
        mine = True,
        maxResults = 50,

        # channelId="UC_x5XG1OV2P6uZZ5FSM9Ttw"
    )
    response = request.execute()

    # print(response['items'])
    for item in response['items']:
        subs.append(item['id'])
    return subs

# def search_in_subs(youtube, subs):
#     request = youtube.search().list(
#         part="snippet",
#         maxResults=25,
#         q="surfing",
#         channelId=subs[0]
#     ) 
#     response = request.execute()
#     print(response)



if __name__ == "__main__":
    youtube = authenticate()
    subs = fetch_subs(youtube)
    # print(subs[0])
    # search_in_subs(youtube, subs)