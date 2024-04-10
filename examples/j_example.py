from TikTokApi import TikTokApi
import asyncio
import os
import argparse
import json  

 
parser = argparse.ArgumentParser(description="Just an example",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-t", "--token", help="ms_token")
parser.add_argument("-id", "--video-id", help="video ID")
args = parser.parse_args()
config = vars(args)
#print(config)

#storage
comments =[]

#max coworkers to retrieve comments
max = 30

# default garbage
video_id = 7350454864071150890
ms_token = os.environ.get("ms_token", "7XyVQZU4GeiuOJAYlfnIF5P5Ul2Tp59PWlZiPHkHCjLgJD0iFD7ojQ-VB3bsYDyoymOZV2NffA_uyMhj35q9tkXyFGDxjVDrDe1O9UvewlZ9aFuYjuSfcOyfjUFeTWG3Lpo=")

#good sh*t
if args.video_id is not None:
    video_id = args.video_id

if args.token is not None:
    ms_token = os.environ.get("ms_token", args.token )



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
