import streamlit as st
import pandas as pd
import webbrowser


st.set_page_config(layout="wide",
                   page_icon='⚽️',
                   page_title='FIFA 2023')

#data preparation
df_data = pd.read_csv('fifa23_cleaned.csv')

df_data_col_contract_Valid_Until = df_data["Contract Valid Until"].fillna(0).astype(int)
df_data["Contract Valid Until"] = df_data_col_contract_Valid_Until
df_data = df_data[df_data["Contract Valid Until"] >= 2023]
df_data = df_data.sort_values(by="Overall", ascending=False)

st.title("⚽️ FIFA 2023")
players_display = str
with st.sidebar:
    clubs_index = df_data['Club'].value_counts().index
    clubs_display = st.selectbox('Club',options=clubs_index)
    df_clubs = df_data[df_data["Club"]== clubs_display]
    
    df_players = df_data[df_data["Club"] == clubs_display]
    players = df_players["Name"].value_counts().index
    players_display = st.selectbox('Players',options=players)
    player = players_display
    player_stats = df_data[df_data["Name"] == player].iloc[0]
    
tab1, tab2 = st.tabs(["⚽️ ***Squad*** ", "🏃🏼‍♂️ ***Player***"])

with tab1:
    st.image(df_clubs['Club Logo'].iloc[0], width=50)
    st.header(df_clubs["Club"].iloc[0])
    columns = ["Name","Age","Nationality","Photo","Flag","Overall","Value","Wage","Height","Weight"]
    df_clubs_filtered = df_clubs[columns]
    st.data_editor(
        df_clubs_filtered,
        column_config={
            "Overall": st.column_config.ProgressColumn("Overall", min_value=0, max_value=100),
            "Photo": st.column_config.ImageColumn(),
            "Flag": st.column_config.ImageColumn()},
        hide_index=True,
    )

with tab2:
    st.image(player_stats["Photo"], width=80)
    st.title(f"{player_stats['Name']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"**Club:** {player_stats['Club']}")
        st.markdown(f"**Age:** {player_stats['Age']}")
    with col2:
        st.markdown(f"**Nationality:** {player_stats['Nationality']} <img src='{player_stats['Flag']}' width='20'>",
        unsafe_allow_html=True)
        st.markdown(f"**Height:** {player_stats['Height']}")
    with col3:
        st.markdown(f"**Preferred Foot:** {player_stats['Preferred Foot']}")
        st.markdown(f"**Weight:** {player_stats['Weight']}")
    st.markdown('---')
    st.subheader(f"Overall {player_stats['Overall']}")
    st.progress(int(player_stats['Overall']))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label='Market Value',value=player_stats['Value'])
    with col2:
        st.metric(label='Weekly Wage', value=player_stats['Wage'])
    with col3:
        st.metric(label='Release Clause', value=player_stats['Release Clause'])



#st.markdown("Developed by [RapidCanvas](https://www.rapidcanvas.ai/) | [Kaggle Dataset](https://www.kaggle.com/datasets/bryanb/fifa-player-stats-database?select=FIFA23_official_data.csv)")
