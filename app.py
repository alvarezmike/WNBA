from pathlib import Path
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt


# For more emojis code https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="WNBA Stats", page_icon=":basketball:")

# displaying image
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    img_to_bytes("WNBA_header.png")
)
st.markdown(
    header_html, unsafe_allow_html=True,
)

# description of web app
st.title('WNBA Player Stats Explorer')

st.markdown("""
This app performs webscraping of WNBA player stats data per game
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/)
""")

st.sidebar.header('Select Criteria Below')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1997,2022))))

# Web scraping of WNBA player stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/wnba/years/" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.G == 'G'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['G'], axis=1)
    return playerstats
playerstats = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Team.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = ['C','F','G','F-G','C-F']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)


# Filtering data
df_selected_team = playerstats[(playerstats.Team.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s) and Position(s)')
st.markdown("""
** 👈 You can change criteria on the left side menu** 
""")
st.info('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
# st.dataframe(df_selected_team)
test = df_selected_team.astype(str)
st.dataframe(test)

# container with side by side columns
col1, col2 = st.columns([3,2])

# column 1
# adding pie chart
with col1:
    st.subheader("Top 5 Points per game stats for the current selected team(s)👇")
    pts_column= test.loc[:,"PTS"].astype(float)
    large5 = pts_column.nlargest(5, keep= "all")
    fig1, ax1 = plt.subplots()
    ax1.pie(large5, autopct= lambda x: '{:1.1f}'.format(x*large5.sum()/100),
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

# column 2
# testing player  and pts stats dataframe
with col2:
    player_and_pts_stats = test[["Player","PTS"]]
    st.caption("PPG Dataframe")
    st.dataframe(player_and_pts_stats)


# Download WNBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
# def filedownload(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
#     href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
#     return href


# st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)



