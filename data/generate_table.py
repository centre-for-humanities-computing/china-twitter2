"""
Generates table for README.md with information about the data
"""
import pandas as pd
from pathlib import Path
import pandas as pd 
import numpy as np
import datetime


def subset_dates(df, filter_dates=True):
    """
    Subsets the dataframe to only include dates between 2019-11-01 and 2022-04-30
    """

    df["created_at"] = pd.to_datetime(df["created_at"]).dt.tz_convert(None)  # Convert to timezone-naive datetime

    if filter_dates:
        start_date = pd.to_datetime(datetime.datetime(2019, 11, 1)).tz_localize(None)  # Convert start date to timezone-naive
        end_date = pd.to_datetime(datetime.datetime(2022, 4, 30)).tz_localize(None)  # Convert end date to timezone-naive

        df = df[
            (df["created_at"] >= start_date) &
            (df["created_at"] <= end_date)
        ]


    return df

def unique_users(df):
    """
    Finds the unique users in the dataframe both media and diplomats
    """

    diplomats = df[df["category"] == "Diplomat"]["username"].unique()
    media = df[df["category"] == "Media"]["username"].unique()

    diplomats.sort()
    media.sort()

    return diplomats, media


def get_information_user(user, df, user_description_dict):

    # Subset to only include the user
    user_df = df[df["username"] == user]

    # Get the number of original tweets
    original_tweets = user_df[user_df["retweet"] != "retweeted"]

    # Original tweets in English
    original_tweets_en = original_tweets[original_tweets["lang"] == "en"]

    # Retweets
    retweets = user_df[user_df["retweet"] == "retweeted"]

    # Retweets in English
    retweets_en = retweets[retweets["lang"] == "en"]

    # create dataframe with information
    information = pd.DataFrame(
        {
            "User": [user], 
            "Description": [user_description_dict[user]],
            "Original tweets": [len(original_tweets)],
            "Original tweets in English": [len(original_tweets_en)],
            "Retweets": [len(retweets)],
            "Retweets in English": [len(retweets_en)],
            "Total": [len(user_df)]
        }
    )

    return information


def generate_table(users, user_description_dict, df):
    table = pd.DataFrame()
    
    for user in users:
        information = get_information_user(user, df, user_description_dict)
        table = pd.concat([table, information])

    return table

user_description_dict = {
    'AmbCina': 'Embassy of the P.R.C. in Rome, Italy',
    'AmbCuiTiankai': 'CUI Tiankai, former Chinese Ambassador to the U.S. (2013-2021)',
    'AmbKongXuanyou': 'KONG Xuanyou, Chinese Ambassador to Japan (2019-2023)',
    'AmbLiJunhua': 'LI Junhua, Ambassador Extraordinary and Plenipotentiary of China to Italy and San Marino (2019-2022)',
    'AmbLiuXiaoMing': 'LIU Xiaoming, Chinese Ambassador to the U.K. (2010-2021)',
    'AmbQinGang': 'QIN Gang, Chinese ambassador to the US (2021-2023)',
    'AmbZhengZeguang': 'ZHENG Zeguang Chinese Ambassador to the UK (2021-)',
    'Amb_ChenXu': 'CHEN Xu, Ambassador, Permanent Representative of the P.R.C. to the U.N. office in Geneva, Switzerland (2019-)',
    'AmbassadeChine': 'Embassy of the P.R.C. in Paris, France',
    'CCGBelfast': 'Consulate General of the P.R.C. in Belfast, U.K.',
    'CGHuangPingNY': 'HUANG Ping, Chinese Consul General in New York (2018-)',
    'CGMeifangZhang': 'ZHANG Meifang, Consul General of China in Belfast (2022-)',
    'CGZhangPingLA': 'ZHANG Ping, Consul General of the People\'s Republic of China in Los Angeles (2017-2022)',
    'CHN_UN_NY': 'Spokesperson of Mission of the P.R.C. to the U.N.',
    'Cao_Li_CHN': 'Cao Li, Counsellor, Information Department, MFA, China (2021-)',
    'ChinaAmbUN': 'ZHANG Jun, Ambassador, Permanent Representative of the P.R.C. to the U.N. (2019-)',
    'ChinaCGCalgary': 'Consulate General of the P.R.C. in Calgary, Canada',
    'ChinaCGMTL': 'Consulate General of the P.R.C. in Montreal, Canada',
    'ChinaCG_Ffm': 'Consulate General of the People\'s Republic of China in Frankfurt am Main',
    'ChinaCG_HH': 'Consulate General of the People\'s Republic of China in Hamburg',
    'ChinaCG_Muc': 'Chinese Consulate General in Munich',
    'ChinaCG_NYC': 'Consulate General of the PRC  in New York',
    'ChinaConSydney': 'Consulate General of the P.R.C. in Sydney, Australia',
    'ChinaConsulate': 'Consulate General of the P.R.C. in Chicago, U.S.',
    'ChinaEUMission': 'Mission of the P.R.C. to the E.U.',
    'ChinaEmbEsp': 'Chinese Embassy in Spain',
    'ChinaEmbGermany': 'Embassy of the P.R.C. in Berlin, Germany',
    'ChinaEmbOttawa': 'Embassy of the P.R.C. in Ottawa, Canada',
    'ChinaInDenmark': 'Embassy of the P.R.C. in Copenhagen, Denmark',
    'ChinaMissionGva': 'Mission of the P.R.C. to the U.N. office in Geneva, Switzerland',
    'ChinaMissionVie': 'Mission of the P.R.C. to the U.N. office in Vienna, Austria',
    'China_Lyon': 'Consulate General of the P.R.C. in Lyon, France',
    'China_Ukraine_': 'Chinese Embassy in Ukraine',
    'ChinainVan': 'Consulate General of the P.R.C. in Vancouver, Canada',
    'Chinamission2un': 'Mission of the P.R.C. to the U.N.',
    'ChineseCon_Mel': 'Chinese Consulate-General in Melbourne',
    'ChineseEmbinRus': 'Chinese Embassy in Russia',
    'ChineseEmbinUK': 'Embassy of the P.R.C. in London, U.K.',
    'ChineseEmbinUS': 'Embassy of the P.R.C. in Washington, D.C., U.S.',
    'ChnConsul_osaka': 'Consulate General of the P.R.C. in Osaka, Japan',
    'ChnConsulateFuk': 'Consulate-General of the P. R. C. in Fukuoka',
    'ChnConsulateNag': 'Consulate-General of the P. R. C. in Nagasaki',
    'ChnConsulateNgo': 'Consulate-General of the P. R. C. in Nagoya',
    'ChnConsulateNgt': 'Consulate-General of the P. R. C. in Niigata',
    'ChnEmbassy_jp': 'Embassy of the P.R.C. in Tokyo, Japan',
    'ChnMission': 'LIU Yuyin, Spokesperson, Permanent Representative of the P.R.C. to the U.N. office in Geneva, Switzerland (2019-)',
    'ConsulChinaBcn': 'Consulate General of China in Barcelona',
    'ConsulateSan': 'Chinese Consulate General in San Francisco',
    'DIOC_MFA_China': 'Department of International Organizations and Conferences, MFA, China',
    'FuCong17': 'Fu Cong, Chinese Ambassador to the EU (2022-)',
    'FukLyuGuijun': 'Consul General of the P. R. C. in Fukuoka (2020-)',
    'GeneralkonsulDu': 'DU Xiaohui, Consul General, Consulate General of the P.R.C. to Hamburg, Germany',
    'Li_Yang_China': 'Li Yang, Counsellor of Department of Information, MFA, China. (2021-)',
    'MFA_China': 'Ministry of Foreign Affairs, Beijing, P.R.C.',
    'SpokespersonCHN': 'HUA Chunying, Spokesperson & Director General, Information Department, Ministry of Foreign Affairs, Beijing, P.R.C. (2019-2021). Assistant Minister of Foreign Affairs (2021-).',
    'SpokespersonHZM': 'HU Zhaoming, Spokesperson & Director General, Bureau of Public Information and Communication, International Department, CPC Central Committee (2019-)',
    'SpoxCHNinUS': 'Liu Pengyu, Spokesperson of Chinese Embassy in the U.S. (2021-)',
    'WangLutongMFA': 'Wang Lutong, Director General for European Affairs, MFA, China (2019-)',
    'WuPeng_MFAChina': 'Wu Peng, Director-General, Department of African Affairs, MFA, China (2020-)',
    'XIEYongjun_CHN': 'Xie Yongjun, Head of Division, Info Dept, MFA, China',
    'Zhou_Li_CHN': 'Zhou Li, Counsellor, Information Department of Foreign Ministry, China (2002-)',
    'chinacgedi': 'Consulate General of the P.R.C. in Edinburgh, U.K.',
    'chinascio': 'State Council Information Office of the P.R.C.',
    'consulat_de': 'Consulate General of the P.R.C. in Strasbourg, France',
    'xuejianosaka': 'Xue Jian, Consul General of P.R.C  in Osaka (2021-)',
    'zhaobaogang2011': 'Zhao Baogang, African Affairs Department of Chinese Foreign Ministry (2021-2023)',
    'zhu_jingyang': 'Zhu Jingyang, Consul General of P.R.C  in Barcelona (2021-)',
    'zlj517': 'ZHAO Lijian, Spokesperson & Deputy Director General, Information Department, Ministry of Foreign Affairs, Beijing, P.R.C. (2019-2023). Deputy Director-General of the Department of Boundary and Ocean Affairs of China (2023-).'

}


def main():
    path = Path(__file__)
    data_path = path.parents[0] / "raw_data.csv"

    df = pd.read_csv(data_path)

    df = subset_dates(df)

    diplo_users, media_users = unique_users(df)
    print(media_users)
        
    print(f"Number of unique users: {len(diplo_users) + len(media_users)}")
    print(f"Number of unique diplomats: {len(diplo_users)}")
    print(f"Number of unique media: {len(media_users)}")

    for user_list, filename in zip([diplo_users, media_users], ["diplo_table.csv", "media_table.csv"]):
        table = generate_table(user_list, user_description_dict, df)
        save_path = path.parents[0] / filename
        table.to_csv(save_path, index=False)

        # print markdown table
        print(table.to_markdown(index=False))



    

if __name__ == "__main__":

    main()