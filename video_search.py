# -*- coding: utf-8 -*-
"""
Created on Sat Mar 18 12:18:39 2017

@author: spnichol
"""

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

DEVELOPER_KEY = "AIzaSyCT4EuraOI5P-MhirDygPskAWHnMK2GYcM"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"




def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    type="video",
    pageToken=options.page_token,
    location=options.location,
    locationRadius=options.location_radius,
    order = options.order,
    part="id,snippet",
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []
  search_videos = []
  nexttok = search_response["nextPageToken"]


  print "Next page token: %s :" % (nexttok) 

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("[ TITLE: %s DATE :%s VIDID:%s]" % (search_result["snippet"]["title"],
      search_result["snippet"]["publishedAt"], search_result["id"]["videoId"]))
      search_videos.append(search_result["id"]["videoId"])
      video_ids = ",".join(search_videos)


    elif search_result["id"]["kind"] == "youtube#channel":
      channels.append("%s (%s)" % (search_result["snippet"]["title"],
                                   search_result["id"]["channelId"]))
    elif search_result["id"]["kind"] == "youtube#playlist":
      playlists.append("%s (%s)" % (search_result["snippet"]["title"],
                                    search_result["id"]["playlistId"]))

  
  video_response = youtube.videos().list(
    id=video_ids,
    part='snippet, recordingDetails'
  ).execute()

  videos_loc = []

  # Add each result to the list, and then display the list of matching videos.
  for video_result in video_response.get("items", []):
    videos_loc.append("[TITLE: %s DATE : %s CHANID: %s  VIDID: %s LAT: %s LONG : %s]" % (video_result["snippet"]["title"],
                              video_result["snippet"]["publishedAt"], video_result["snippet"]["channelId"], video_result["id"], video_result["recordingDetails"]["location"]["latitude"],
                              video_result["recordingDetails"]["location"]["longitude"]))

  #video_result["publishedAt"]
  #video_result["id"],
  print "Videos:\n", "\n".join(videos_loc).encode('utf-8'), "\n"
  #print "Video_Meta:\n", "\n".join(videos).encode('utf-8'), "\n"

if __name__ == "__main__":

  argparser.add_argument("--q", help="Search term", default="Google")
  argparser.add_argument("--max-results", help="Max results", default=50)
  argparser.add_argument("--location", help="Location", default="37.42307,-122.08427")
  argparser.add_argument("--location-radius", help="Location radius", default="100km")
  argparser.add_argument("--page-token", help="Page token")
  argparser.add_argument("--order", help="Order", default="date")
  args = argparser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)