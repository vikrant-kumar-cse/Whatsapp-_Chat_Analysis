from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
extractor = URLExtract()  # Create a URL extractor instance


# Function to fetch statistics
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    # Total number of messages
    num_messages = df.shape[0]

    # Total number of words
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # Number of media messages
    num_media_messages = df[df['Message'] == '<Media omitted>\n'].shape[0]

    # Number of links shared
    links = []
    for message in df['Message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)


# Function to find the most busy users
def most_busy_user(df):
    user_counts = df['User'].value_counts().head()
    percentage_df = (
        (df['User'].value_counts() / df.shape[0]) * 100
    ).reset_index().rename(columns={'index': 'name', 'User': 'percent'})
    return user_counts, percentage_df


# Function to create a WordCloud
def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=19, background_color='white')
    df_wc = wc.generate(df['Message'].str.cat(sep=" "))
    return df_wc


# Function to find most common words
def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']

    words = []
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    emojis=[]
    for Message in df['Message']:
        emojis.extend([c for c in Message if c in emoji.EMOJI_DATA])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['Message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+ "-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    daily_timeline=df.groupby('only_date').count()['Message'].reset_index()

    return daily_timeline

def weak_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Message', aggfunc='count').fillna(0)
    return user_heatmap







'''
    if selected_User=='Overall':
        #1.Total Number Of Message
        num_messege=df.shape[0]

        #2.Total Number Of Word
        words=[]
        for Message in df['Message']:
            words.extend(Message.split())
        return num_messege,len(words)

    else:
        new_df=df[df['User']==selected_User]
        num_messege = new_df.shape[0]

        words = []
        for Message in new_df['Message']:
            words.extend(Message.split())

        return num_messege, len(words)
'''