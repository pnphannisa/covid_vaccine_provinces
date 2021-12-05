import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import datetime
st.set_page_config (page_title='ผู้ติดเชื้อสะสม vs ผู้ได้รับวัคซีนสะสม')
st.header('ผู้ติดเชื้อสะสม vs ผู้ได้รับวัคซีนสะสม')

#load data
df = pd.read_csv('data/davidj_joined_new.csv')
df['ymd'] = df.Date.map(lambda x: f'{x.split("/")[2].zfill(2)}-{x.split("/")[0].zfill(2)}-{x.split("/")[1].zfill(2)}')
	
#sidebar
# st.sidebar.write('### เลือกจังหวัดและช่วงเวลา')
all_provinces = df.Province.unique().tolist()
province = st.sidebar.selectbox('จังหวัด', all_provinces, index=all_provinces.index('Nakhon Nayok'))
date_begin = st.sidebar.date_input('ตั้งแต่วันที่', value=datetime.date(2021, 1, 1), 
	min_value=datetime.date(2020, 3, 1), 
	max_value=datetime.date(2021, 11, 26))
date_begin = str(date_begin)
date_end = st.sidebar.date_input('ถึงวันที่', value=datetime.date(2021, 11, 25), 
	min_value=datetime.date(2020, 3, 1), 
	max_value=datetime.date(2021, 11, 25))
date_end = str(date_end)

#prep data
df_m = df[df.Province==province][['ymd','Province','case_cum_percap','1vacpercap','2vacpercap']]\
        .melt(id_vars=['ymd','Province'])
x = df_m[(df_m.ymd>=date_begin)&(df_m.ymd<=date_end)&(df_m.variable=='case_cum_percap')].ymd
case_y = df_m[(df_m.ymd>=date_begin)&(df_m.ymd<=date_end)&(df_m.variable=='case_cum_percap')].value
vaccine1_y = df_m[(df_m.ymd>=date_begin)&(df_m.ymd<=date_end)&(df_m.variable=='1vacpercap')].value
vaccine2_y = df_m[(df_m.ymd>=date_begin)&(df_m.ymd<=date_end)&(df_m.variable=='2vacpercap')].value

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=x, y=case_y, name="จำนวนผู้ติดเชื้อสะสม / จำนวนประชากร",line_color='red',),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=x, y=vaccine1_y, name="จำนวนผู้ได้รับวัคซีน 1 เข็มสะสม / จำนวนประชากร",line_color='gold',),
    secondary_y=True,
)

fig.add_trace(
    go.Scatter(x=x, y=vaccine2_y, name="จำนวนผู้ได้รับวัคซีน 2 เข็มสะสม / จำนวนประชากร",line_color='green',),
    secondary_y=True,
)

# Set x-axis title
fig.update_xaxes(title_text="")

# Set y-axes titles
fig.update_yaxes(title_text="จำนวนผู้ติดเชื้อสะสม / จำนวนประชากร", secondary_y=False)
fig.update_yaxes(title_text="จำนวนผู้ได้รับวัคซีนสะสม / จำนวนประชากร", secondary_y=True)
fig.update_xaxes(
    dtick="M1",
    tickformat="%Y-%m")

#legend position
fig.update_layout(
    template='none',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01),
    margin=dict(l=50, r=50, t=50, b=50),
)

st.plotly_chart(fig, use_container_width=True)