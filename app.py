import streamlit as st
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
from fontTools.varLib.instancer import verticalMetricsKeptInSync
import helpers  # Import only helper functions, no variables!

import preprocessor  # Custom module to preprocess WhatsApp chat data


st.sidebar.markdown("### 📊 **WhatsApp Chat Analyzer**")
st.sidebar.write("Analyze your WhatsApp chat history. Follow these steps:")
st.sidebar.markdown("1. Export the chat file from WhatsApp.\n"
                    "2. Upload the `.txt` file using the uploader below.\n"
                    "3. Click On Show Analysis."
                    )
uploaded_file = st.sidebar.file_uploader("Upload your chat file (e.g., .txt)", type=['txt'])

if uploaded_file is not None:
    # Read file as bytes
    bytes_data = uploaded_file.getvalue()
    # Convert to string
    data = bytes_data.decode("utf-8")
    # Preprocess data
    df = preprocessor.preprocess(data)
    #st.dataframe(df)

    # Extract User Names
    user_list = df['User'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_User = st.sidebar.selectbox("Show Analysis for Different User", user_list)

    # Display Statistics
    if st.sidebar.button("Show Analysis"):
        num_messages, words, media_count, links = helpers.fetch_stats(selected_User, df)
        st.markdown('<h1 style="color: green; font-size: 36px;">📊 Top Statistics</h1>', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            #st.header("Total_Message")
            st.markdown(
                "<h1>Total_Message</h1>",
                unsafe_allow_html=True
            )
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(media_count)
        with col4:
            st.header("Links Shared")
            st.title(links)

        # Monthly Timeline
        st.markdown('<h1 style="color: blue; font-size: 36px;">📅 Monthly Timeline</h1>', unsafe_allow_html=True)

        timeline = helpers.monthly_timeline(selected_User, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['Message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.markdown('<h1 style="color: teal; font-size: 36px;">🗓️ Daily Timeline</h1>', unsafe_allow_html=True)

        daily_timeline = helpers.daily_timeline(selected_User, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['Message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #Activity map
        st.markdown('<h1 style="color: darkorange; font-size: 36px;">🗺️ Activity Map</h1>', unsafe_allow_html=True)

        col1,col2=st.columns(2)
        with col1:
            st.header("Most Busy Days")
            busy_day=helpers.weak_activity_map(selected_User,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Months")
            busy_month=helpers.month_activity_map(selected_User,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.markdown('<h2 style="color: purple; font-size: 30px;">🌍 Weekly Activity Map</h2>', unsafe_allow_html=True)

        user_heatmap=helpers.activity_heatmap(selected_User,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)














        # Most Busy User Analysis
        if selected_User == "Overall":
            st.markdown('<h1 style="color: crimson; font-size: 36px;">🔥 Most Busy</h1>', unsafe_allow_html=True)

            x, new_df = helpers.most_busy_user(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Word Cloud
        st.markdown('<h1 style="color: navy; font-size: 36px;">☁️ Word Cloud</h1>', unsafe_allow_html=True)

        df_wc = helpers.create_wordcloud(selected_User, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #find most common words
        st.title("Most Common Words")
        most_common_df=helpers.most_common_words(selected_User,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df['Word'],most_common_df['Count'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #emoji Analysis
        st.markdown('<h1 style="color: orange; font-size: 36px;">😊 Most Common Emoji</h1>', unsafe_allow_html=True)

        emoji_df=helpers.emoji_helper(selected_User,df)
        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            # Correctly pass numeric values for the pie chart
            ax.pie(emoji_df[1], labels=emoji_df[0], autopct="%1.1f%%")
            st.pyplot(fig)



import streamlit as st

# Custom CSS for advanced animation and enhanced design
st.markdown(
    """
    <style>
        /* Custom gradient background animation */
        @keyframes gradientBg {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }

        /* Fade and zoom effect for text */
        @keyframes fadeInZoom {
            0% {
                opacity: 0;
                transform: translateY(30px) scale(0.6); /* Start smaller and lower */
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1); /* End normal size */
            }
        }

        /* Pulse effect for the button */
        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.1);
            }
            100% {
                transform: scale(1);
            }
        }

        /* Background Gradient Animation */
        body {
            background: linear-gradient(-45deg, #6a11cb, #2575fc);
            background-size: 400% 400%;
            animation: gradientBg 15s ease infinite;
        }

        /* Animated Text Styling (Neon Effect + Fade Zoom) */
        .animated-text {
            animation: fadeInZoom 3s ease-in-out;
            color: #ff5c8d;
            font-family: 'Roboto', sans-serif;
            font-size: 50px;
            text-align: center;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7), 0 0 25px rgba(255, 0, 255, 1), 0 0 5px rgba(255, 0, 255, 0.7);
        }

        /* Button Styling with Pulse Effect */
        .animated-button {
            background: #ff6f61;
            color: #ffffff;
            font-size: 18px;
            padding: 15px 30px;
            text-align: center;
            border: none;
            border-radius: 50px;
            cursor: pointer;
            box-shadow: 0px 10px 20px rgba(255, 102, 102, 0.4);
            animation: pulse 2s infinite;
            transition: transform 0.2s;
        }

        /* Hover effect for the button */
        .animated-button:hover {
            transform: translateY(-5px); /* Makes the button slightly lift up */
        }

        /* Additional Custom Animation */
        .animated-footer {
            text-align: center;
            margin-top: 20px;
            font-size: 18px;
            color: #fff;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Main Content
st.markdown('<h1 class="animated-text">🚀 Welcome to My New Data Analysis Project!</h1>', unsafe_allow_html=True)

if st.button("Help"):
    st.info(
        "To export a WhatsApp chat:\n1. Open the chat.\n2. Go to Options > More > Export Chat > Without Media."
    )
# Additional footer for added engagement
st.markdown(
    '<div class="animated-footer">Analyse Your Whatsapp Chat With Easy Way!</div>',
    unsafe_allow_html=True
)








