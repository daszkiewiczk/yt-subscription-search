# -*- coding: utf-8 -*-

# Sample Python code for youtube.subscriptions.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import socket
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]

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
    nextPageToken = ''
    while True:
        request = youtube.subscriptions().list(
            part='snippet',
            mine = True,
            maxResults = 50,
            pageToken = nextPageToken
        )
        response = request.execute()
        for item in response['items']:
            subs.append(item['snippet']['resourceId']['channelId'])
        if 'nextPageToken' not in response:
            break
        else:
            nextPageToken = response['nextPageToken']
    
    return subs

def search_in_subs(youtube, subs):
    search_results = []
    for sub in subs:
        request = youtube.search().list(
            part="snippet",
            maxResults=25,
            q="python",
            channelId=sub
        ) 
        response = request.execute()
        for item in response['items']:
            search_results.append(item['snippet']['title'])

    return search_results



if __name__ == "__main__":
    youtube = authenticate()
    subs = fetch_subs(youtube)

    print(len(subs))
    
    search_results = search_in_subs(youtube, subs)
    for result in search_results:
        print(result)