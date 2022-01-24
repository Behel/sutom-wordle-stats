import pandas as pd
import tweepy, datetime, os

BEGIN_TWEET_SCRAP = datetime.datetime.now() - datetime.timedelta(days=2)

# WORDLEFR :
# (GAME_NAME, ID_GAME, DEAD_STR) = ("Le Mot \(\@WordleFR\)".upper(), str((datetime.date.today() - datetime.date(2022, 1, 10)).days) ,"💀")
# (HISTO, HISTO_MAX) = ("🟨", "🟩")
# (TWEET_GAME_NAME, TWEET_ORNAMENTS_1, TWEET_ORNAMENTS_2) = ("Le Mot (@WordleFR)", "🟩", "🟨")

# SUTOM : 
(GAME_NAME, ID_GAME, DEAD_STR) = ("SUTOM", str((datetime.date.today() - datetime.date(2022, 1, 8)).days) ,"-")
(HISTO, HISTO_MAX) = ("🟦", "🟥")
(TWEET_GAME_NAME, TWEET_ORNAMENTS_1, TWEET_ORNAMENTS_2) = ("SUTOM", "🟥", "🟡")

def get_df_tweets() : 
    """Look for tweets that include the string listed above. Using a Dev Twitter Bearer token

    Returns:
        DataFrame: DataFrame with tweets
    """
    client_get = tweepy.Client(bearer_token=os.getenv('BEARER_TOKEN'))

    tweets = []
    for tweet in tweepy.Paginator(client_get.search_recent_tweets, query = "\"" + GAME_NAME + " #" + ID_GAME +"\"", start_time = BEGIN_TWEET_SCRAP.strftime("%Y-%m-%dT%H:%M:%SZ"), tweet_fields = 'referenced_tweets' ,max_results = 100).flatten():
        try : 
            if tweet.referenced_tweets[0].type == 'retweeted' : 
                None
            else :
                tweets.append(tweet.text) 
        except TypeError:
            tweets.append(tweet.text)
    df = pd.DataFrame()
    df['tweet'] = pd.Series(tweets)
    return df

def send_tweet(tweet_to_send) : 
    """Send a tweet, using OAuth1.0a tokens

    Args:
        tweet_to_send (String): Just a text to tweet.
    """
    client = tweepy.Client(consumer_key=os.getenv('API_KEY'),
                       consumer_secret=os.getenv('API_SECRET'),
                       access_token=os.getenv('ACCESS_TOKEN'),
                       access_token_secret=os.getenv('ACCESS_SECRET'))

    client.create_tweet(text=tweet_to_send)

def get_stats(Tweets_df) : 
    """Generate a tweet with aggregated stats from a dataframe of tweets

    Args:
        Tweets_df (DataFrame): All the tweets

    Returns:
        String: A Tweet ready to be sent
    """
    nb_parties = len(Tweets_df)

    Tweets_df['tweet'] = Tweets_df['tweet'].str.upper()
    Tweets_df['tweet'] = Tweets_df['tweet'].str.replace('\n', ' ',regex=True)
    Tweets_df['tweet'] = Tweets_df['tweet'].str.replace(' +', ' ',regex=True)

    zero = len(Tweets_df.loc[Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" "+DEAD_STR+"/6") | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" "+DEAD_STR+"/6")])
    un = len(Tweets_df.loc[Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 1/6") | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 1/6")])
    deux = len(Tweets_df.loc[Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 2/6") | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 2/6")])
    trois = len(Tweets_df.loc[Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 3/6") | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 3/6")])
    quatre = len(Tweets_df.loc[Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 4/6") | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 4/6")])
    cinq = len(Tweets_df.loc[Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 5/6") | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 5/6")])
    six = len(Tweets_df.loc[Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 6/6") | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 6/6")])

    total = zero+un+deux+trois+quatre+cinq+six

    top_un = round(un*100 / total)
    top_deux = round((un+deux)*100 / total)
    top_trois = round((un+deux+trois)*100 / total)
    top_quatre = round((un+deux+trois+quatre)*100 / total)
    top_cinq = round((un+deux+trois+quatre+cinq)*100 / total)
    top_six = round((un+deux+trois+quatre+cinq+six)*100 / total)

    pct_un = round(un*100 / total)
    pct_deux = round((deux)*100 / total)
    pct_trois = round(trois*100 / total)
    pct_quatre = round((quatre)*100 / total)
    pct_cinq = round((cinq)*100 / total)
    pct_six = round((six)*100 / total)
    pct_zero = round((zero)*100 / total)

    smi_un = HISTO_MAX * round(pct_un/5) if un == max(zero,un,deux,trois,quatre,cinq,six) else HISTO * round(pct_un/5)
    smi_deux = HISTO_MAX * round(pct_deux/5)  if deux == max(zero,un,deux,trois,quatre,cinq,six) else HISTO * round(pct_deux/5)
    smi_trois = HISTO_MAX * round(pct_trois/5)  if trois == max(zero,un,deux,trois,quatre,cinq,six) else HISTO * round(pct_trois/5)
    smi_quatre = HISTO_MAX * round(pct_quatre/5)  if quatre == max(zero,un,deux,trois,quatre,cinq,six) else HISTO * round(pct_quatre/5)
    smi_cinq = HISTO_MAX * round(pct_cinq/5) if cinq == max(zero,un,deux,trois,quatre,cinq,six) else HISTO * round(pct_cinq/5)
    smi_six = HISTO_MAX * round(pct_six/5) if six == max(zero,un,deux,trois,quatre,cinq,six) else HISTO * round(pct_six/5)
    smi_zero = HISTO_MAX * round(pct_zero/5) if zero == max(zero,un,deux,trois,quatre,cinq,six) else HISTO * round(pct_zero/5)

    ok_tweets = Tweets_df.loc[
            Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 1/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 2/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 3/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 4/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 5/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" 6/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " #"+ ID_GAME +" "+DEAD_STR+"/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 1/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 2/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 3/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 4/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 5/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" 6/6")
            | Tweets_df['tweet'].str.contains(GAME_NAME + " "+ ID_GAME +" "+DEAD_STR+"/6")
            ]

    tweet_to_send = ""
    tweet_to_send += TWEET_ORNAMENTS_1 + TWEET_ORNAMENTS_2 + " " + TWEET_GAME_NAME + " #" + ID_GAME + " - " + str(total) + " parties " + TWEET_ORNAMENTS_2 + TWEET_ORNAMENTS_1+ "\n\n"
    tweet_to_send += "1/6 - "+ smi_un + " " + str(un) + " (Top "+ str(top_un)+"%)\n"
    tweet_to_send += "2/6 - "+ smi_deux + " " + str(deux) + " (Top "+ str(top_deux)+"%)\n"
    tweet_to_send += "3/6 - "+ smi_trois + " " + str(trois) + " (Top "+ str(top_trois)+"%)\n"
    tweet_to_send += "4/6 - "+ smi_quatre + " " + str(quatre) + " (Top "+ str(top_quatre)+"%)\n"
    tweet_to_send += "5/6 - "+ smi_cinq + " " + str(cinq) + " (Top "+ str(top_cinq)+"%)\n"
    tweet_to_send += "6/6 - "+ smi_six + " " + str(six) + " (Top "+ str(top_six)+"%)\n"
    tweet_to_send += DEAD_STR+"/6 - "+ smi_zero + " " + str(zero) + "\n\n"
    tweet_to_send += "Moyenne : " + str(round((un+deux*2+trois*3+quatre*4+cinq*5+six*6+zero*6)/total,2)).replace('.',',') + "\n"

    return tweet_to_send

Tweets_df = get_df_tweets()
tweet_to_send = get_stats(Tweets_df)

print(tweet_to_send)
send_tweet(tweet_to_send)
