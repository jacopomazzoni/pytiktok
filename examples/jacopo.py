from TikTokApi import TikTokApi
import asyncio
import os
import argparse
import json  
import requests

# this comment is for github
url='https://www.tiktok.com/en'
url2='https://www.tiktok.com/api/recommend/item_list/?aid=1988&app_language=en&app_name=tiktok_web&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Linux%20x86_64&browser_version=5.0%20%28X11%29&channel=tiktok_web&cookie_enabled=true&count=30&device_id=7163916748088903169&device_platform=web_pc&focus_state=false&from_page=fyp&history_len=5&is_fullscreen=false&is_page_visible=true&os=linux&priority_region=&referer=&region=TW&root_referer=https%3A%2F%2Fwww.google.com%2F&screen_height=1080&screen_width=1920&tz_name=Asia%2FTokyo&webcast_language=en&msToken=1dCRzRecIKwoXXt2XNqL659r22i24Rgw-bYYogQujt_fYsxRQDEvUBkmtztQsiWd_OSZUrBvA054t1YNdYSJJxeFtZKaEjDjFjIKMEyesmkprTD-8CLIdIU4TUjrVyPQlntww4jIoWIZ0g==&X-Bogus=DFSzsIVL-isANHNDS0CN4aL1Xb7j&_signature=_02B4Z6wo00001p5YTDQAAIDDDHa3p8mTTUqeWUiAAMUJc3'

header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
          'Host': 'www.tiktok.com',
'Referer': 'https://www.tiktok.com/foryou?is_copy_url=1&is_from_webapp=v1',
'Connection': 'keep-alive'}

 
parser = argparse.ArgumentParser(description="Just an example",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument("-t", "--token", help="ms_token")
parser.add_argument("-id", "--video-id", help="video ID")
args = parser.parse_args()
config = vars(args)

#storage
comments =[]

#max coworkers to retrieve comments
max = 30

# default garbage
#video_id = 7350454864071150890
#ms_token = os.environ.get("ms_token", "7XyVQZU4GeiuOJAYlfnIF5P5Ul2Tp59PWlZiPHkHCjLgJD0iFD7ojQ-VB3bsYDyoymOZV2NffA_uyMhj35q9tkXyFGDxjVDrDe1O9UvewlZ9aFuYjuSfcOyfjUFeTWG3Lpo=")

#good sh*t
if args.video_id is not None:
    video_id = args.video_id

#if args.token is not None:
#    ms_token = os.environ.get("ms_token", args.token )

r = requests.get(url2, headers=header)
if r.status_code == 200:
    for c in r.cookies:
        if c.name=='msToken':
            ms_token = c.value
            print(ms_token) 
else:
    print("merda")

async def get_comments():
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(id=video_id)
        count = 0
        async for comment in video.comments(count=max):
            tmp = comment.as_dict
            tmp["text"]=comment.text
            json_object = json.dumps(tmp, indent = 4)
            comments.append(json_object)
         


if __name__ == "__main__":
    asyncio.run(get_comments())
    # do the json stuff here outside of the async part
    print("{ \"comments\": [")
    counter = 0
    Ncom = len(comments) 
    for comment in comments:
        counter+=1
        print(comment)
        if counter < Ncom:
            print(",")
    print("]}")
