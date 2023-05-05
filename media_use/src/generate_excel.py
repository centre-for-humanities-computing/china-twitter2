import pandas as pd
import openpyxl
import os
from pathlib import Path


def main():
    path = Path(__file__)
    data_path = path.parents[2] / "data" / "media_info.csv"
    out_path = path.parents[1] / "excel"

    df = pd.read_csv(data_path)

    # split the data into the media and the diplomats
    media = df[df['category'] == 'Media'].reset_index(drop=True)
    data = df[df['category'] == 'Diplomat'].reset_index(drop=True)


    # DIPLOMATS
    # images
    photo = data[data['photo'] > 0].reset_index(drop=True)
    photo = photo.drop(columns = ['video', 'tweetID', 'listed_count'])
    photo_org = photo[photo['retweet'] != 'retweeted'].reset_index(drop=True)
    photo_org = photo_org.sort_values('retweet_count', ascending = False)
    photo_org[:1000].to_excel(out_path / 'most_retweeted_orginal_diplomat_photos.xlsx', index=False)
    photo_org_en = photo_org[photo_org['lang'] == 'en']
    photo_org_en[:1000].to_excel(out_path / 'most_retweeted_orginal_diplomat_photos_en.xlsx', index=False)

    # videos
    video = data[data['video'] > 0].reset_index(drop=True)
    video = video.drop(columns = ['photo', 'url', 'tweetID', 'listed_count'])
    video_org = video[video['retweet'] != 'retweeted'].reset_index(drop=True)
    video_org = video_org.sort_values('retweet_count', ascending = False)
    video_org[:1000].to_excel(out_path / 'most_retweeted_orginal_diplomat_videos.xlsx', index=False)
    video_org_en = video_org[video_org['lang'] == 'en']
    video_org_en[:1000].to_excel(out_path / 'most_retweeted_orginal_diplomat_videos_en.xlsx', index=False)

    # no photos or videos
    no_media = data[(data['photo'] == 0) & (data['video'] == 0)].reset_index(drop=True)
    no_media_org = no_media[no_media['retweet'] != 'retweeted'].reset_index(drop=True)
    no_media_org = no_media_org.sort_values('retweet_count', ascending = False)
    no_media_org[:1000].to_excel(out_path / 'most_retweeted_orginal_diplomat_no_media.xlsx', index=False)
    no_media_org_en = no_media_org[no_media_org['lang'] == 'en']
    no_media_org_en[:1000].to_excel(out_path / 'most_retweeted_orginal_diplomat_no_media_en.xlsx', index=False)


    # MEDIA
    # images
    photo = media[media['photo'] > 0].reset_index(drop=True)
    photo = photo.drop(columns = ['video', 'tweetID', 'listed_count'])
    photo_org = photo[photo['retweet'] != 'retweeted'].reset_index(drop=True)
    photo_org = photo_org.sort_values('retweet_count', ascending = False)
    photo_org[:1000].to_excel(out_path / 'most_retweeted_orginal_media_photos.xlsx', index=False)
    photo_org_en = photo_org[photo_org['lang'] == 'en']
    photo_org_en[:1000].to_excel(out_path / 'most_retweeted_orginal_media_photos_en.xlsx', index=False)


    # videos
    video = media[media['video'] > 0].reset_index(drop=True)
    video = video.drop(columns = ['photo', 'url', 'tweetID', 'listed_count'])
    video_org = video[video['retweet'] != 'retweeted'].reset_index(drop=True)
    video_org = video_org.sort_values('retweet_count', ascending = False)
    video_org[:1000].to_excel(out_path / 'most_retweeted_orginal_media_videos.xlsx', index=False)
    video_org_en = video_org[video_org['lang'] == 'en']
    video_org_en[:1000].to_excel(out_path /'most_retweeted_orginal_media_videos_en.xlsx', index=False)

if __name__ == '__main__':
    main()