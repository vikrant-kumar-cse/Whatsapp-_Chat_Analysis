import re,pandas as pd
def preprocess(data):
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}\s?(?:AM|PM) - "
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'User_message': message, 'Message_Dates': dates})
    # Clean 'Message_Dates' by removing " - "
    df['Message_Dates'] = df['Message_Dates'].str.replace(" - ", "")
    # Convert to datetime
    df['Message_Dates'] = pd.to_datetime(df['Message_Dates'], format='%m/%d/%y, %I:%M %p')


    Users = []
    Messages = []
    for message in df['User_message']:
        # Use raw string to avoid SyntaxWarning
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # User name present
            Users.append(entry[1])  # Append the username
            Messages.append(" ".join(entry[2:]))  # Append the actual message
        else:  # If no username (e.g., system message)
            Users.append('group_notification')
            Messages.append(entry[0])

    df['User'] = Users
    df['Message'] = Messages
    df.drop(columns=['User_message'], inplace=True)



    df['only_date'] = df['Message_Dates'].dt.date
    df['year'] = df['Message_Dates'].dt.year
    df['month_num'] = df['Message_Dates'].dt.month
    df['month'] = df['Message_Dates'].dt.month_name()
    df['day'] = df['Message_Dates'].dt.day
    df['day_name'] = df['Message_Dates'].dt.day_name()
    df['hour'] = df['Message_Dates'].dt.hour
    df['minute'] = df['Message_Dates'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
