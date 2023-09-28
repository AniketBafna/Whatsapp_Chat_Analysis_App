import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import plotly.graph_objects as go

def model():
    st.set_option('deprecation.showPyplotGlobalUse', False)

    st.sidebar.title("Whatsapp Chat Analyzer")

    uploaded_file = st.sidebar.file_uploader("Choose a file:")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode("utf-8")
        #st.text(data)

        df = preprocessor.preprocess(data)

        #st.dataframe(df)

        # fetch unique users
        user_list = df['user'].unique().tolist()
        if user_list == 'group_notification':
            user_list.remove('group_notification')
        else:
            user_list.remove('group_notification')
        #user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0,'Overall')

        selected_user = st.sidebar.selectbox("User: ", user_list)

        if st.sidebar.button("Show Analysis"):

            num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)
            st.title("Top Statistics :point_left: ")
            col1, col2, col3, col4 = st.columns(4)
        
            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            with col2:
                st.header("Total Words")
                st.title(words)
            with col3:
                st.header("Media Shared")
                st.title(num_media_messages)
            with col4:
                st.header("Links Shared")
                st.title(links)

            st.title("-----------------------------------------------------------")

            ## Monthly Timelne
            st.title("Monthly Timeline :point_left: ")

            col1, col2 = st.columns(2)
            timeline = helper.monthly_timeline(selected_user,df)
            with col1:
                st.dataframe(timeline[['Month-Year','Message Frequency']])
            with col2:
                fig,ax = plt.subplots()
                ax.plot(timeline['Month-Year'], timeline['Message Frequency'],color='black')
                plt.xticks(rotation=45)
                st.pyplot(fig)
        

            st.title("-----------------------------------------------------------")

            ## Daily Timeline
            st.title("Daily Timeline :point_left: ")
            daily_timeline = helper.daily_timeline(selected_user, df)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(daily_timeline)
            with col2:
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['Date'], daily_timeline['Message Frequency'], color='black')
                plt.xticks(rotation=45)
                st.pyplot(fig)
        

            st.title("-----------------------------------------------------------")

            # Weekly Activity Map 
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(busy_day)
            with col2:
                fig,ax = plt.subplots()
                a = ax.bar(busy_day.index,busy_day.values,color='grey',label=busy_day.values)
                ax.bar_label(a, label_type='center')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
        
            st.title("-----------------------------------------------------------")

            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)    
            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(busy_month)
            with col2:    
                fig, ax = plt.subplots()
                b = ax.bar(busy_month.index, busy_month.values,color='orange', label=busy_month.values)
                ax.bar_label(b, label_type='center')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.title("-----------------------------------------------------------")

            # Finding the busiest users in the group
            if selected_user == 'Overall':
                st.title('Most Busy Users :point_left: ')
                x, new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    st.dataframe(new_df)
                with col2:
                    c = ax.bar(x.index, x.values, label=x.values)
                    ax.bar_label(c, label_type='center')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)

                st.title("-----------------------------------------------------------")

            # Most Common Words
            st.title("Most Common Words Used in the Chat :point_left: ")
            most_common_df = helper.most_common_words(selected_user, df)

            col1, col2 = st.columns(2)
            with col1:
                st.dataframe(most_common_df)
            with col2:
                fig,ax = plt.subplots()
                d = ax.bar(most_common_df['Word'],most_common_df['Frequency'], label=most_common_df['Frequency'], color='pink')
                ax.bar_label(d, label_type='center')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            st.title("-----------------------------------------------------------")

            # emoji analysis
            emoji_df = helper.emoji_helper(selected_user, df)
            st.title("Most Frequently used Emoji in the Chat :point_left: ")

            if emoji_df.empty:
                st.write("No Emoji to Show!")
            else:
                col1, col2 = st.columns(2)

                with col1:
                    st.dataframe(emoji_df)
                with col2:
                    fig, ax = plt.subplots()
                    ax.pie(emoji_df['Frequency'].head(), labels=emoji_df['Emoji'].head(),autopct="%0.2f")
                    st.pyplot(fig)

            st.title("-----------------------------------------------------------")

            st.title("Weekly Activity Map :point_left: ")
            user_heatmap = helper.activity_heatmap(selected_user,df)
            fig,ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)

            st.title("-----------------------------------------------------------")

            # workCloud
            st.title("Wordcloud :point_left: ")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)
