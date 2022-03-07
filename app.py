import pandas as pd
import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import datetime


def hex_to_rgba(h, alpha):
    '''
    converts color value in hex format to rgba format with alpha transparency
    '''
    return tuple([int(h.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)] + [alpha])


st.set_page_config(page_title='ผู้ติดเชื้อสะสม vs ผู้ได้รับวัคซีนสะสม')
st.header('ผู้ติดเชื้อสะสม vs ได้รับวัคซีนสะสม')

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Maitree:wght@500;600&display=swap');
#vs {
    font-family: 'Maitree';
    font-weight: 600;
    font-size: 32px;
}
.legend {
    font-family: 'Maitree';
    font-weight: 600;  
}
html, body {
    font-family: 'Maitree';
    font-weight: 500;
}
</style>
""",
    unsafe_allow_html=True,
)

# load data
df = pd.read_csv('data/djay_joined_new5.csv')
df['ymd'] = df.Date.map(lambda x: f'{x.split("/")[2].zfill(2)}-{x.split("/")[1].zfill(2)}-{x.split("/")[0].zfill(2)}')

# sidebar
# st.sidebar.write('### เลือกจังหวัดและช่วงเวลา')
all_provinces = sorted(df.Province_th.unique().tolist())
province = st.sidebar.selectbox('จังหวัด', all_provinces, index=all_provinces.index('นครนายก'))
date_begin = st.sidebar.date_input('ตั้งแต่วันที่', value=datetime.date(2021, 1, 1),
                                   min_value=datetime.date(2020, 3, 1),
                                   max_value=datetime.date(2022, 2, 20))
date_begin = str(date_begin)
date_end = st.sidebar.date_input('ถึงวันที่', value=datetime.date(2022, 2, 20),
                                 min_value=datetime.date(2020, 3, 1),
                                 max_value=datetime.date(2022, 2, 20))
date_end = str(date_end)

# prep data
df_m = df[df.Province_th == province][['ymd', 'Province_th',
                                       'case_cum_percap',
                                       '1vacpercap',
                                       '2vacpercap',
                                       '3vacpercap',
                                       'vac_all_percap',
                                       'vac_astra_percap',
                                      'vac_moderna_percap',
                                      'vac_pfizer_percap',
                                      'vac_sinopharm_percap',
                                      'vac_sinovac_percap',
                                      'Vac Allocated All',
                                      'Vac Allocated AstraZeneca',
                                      'Vac Allocated Moderna',
                                      'Vac Allocated Pfizer',
                                      'Vac Allocated Sinopharm',
                                      'Vac Allocated Sinovac',
                                      ]].melt(id_vars=['ymd', 'Province_th'])
x = df_m[(df_m.ymd >= date_begin) & (df_m.ymd <= date_end) & (df_m.variable == 'case_cum_percap')].ymd
case_y = df_m[(df_m.ymd >= date_begin) & (df_m.ymd <= date_end) & (df_m.variable == 'case_cum_percap')].value
vaccine1_y = df_m[(df_m.ymd >= date_begin) & (df_m.ymd <= date_end) & (df_m.variable == '1vacpercap')].value
vaccine2_y = df_m[(df_m.ymd >= date_begin) & (df_m.ymd <= date_end) & (df_m.variable == '2vacpercap')].value
vaccine3_y = df_m[(df_m.ymd >= date_begin) & (df_m.ymd <= date_end) & (df_m.variable == '3vacpercap')].value
vac_all_y = df_m[(df_m.ymd >= date_begin) & (df_m.ymd <= date_end) & (df_m.variable == 'Vac Allocated All')].value
vac_astra_y = df_m[(df_m.ymd >= date_begin) & (df_m.ymd <= date_end) & (df_m.variable == 'Vac Allocated AstraZeneca')].value
vac_moderna_y = df_m[(df_m.ymd >= date_begin) & (df_m.ymd <= date_end) & (df_m.variable == 'Vac Allocated Moderna')].value
vac_pfizer_y = df_m[(df_m.ymd >= date_begin) & (df_m.ymd <= date_end) & (df_m.variable == 'Vac Allocated Pfizer')].value
vac_sinopharm_y = df_m[(df_m.ymd >= date_begin) & (df_m.ymd <= date_end) & (df_m.variable == 'Vac Allocated Sinopharm')].value
vac_sinovac_y = df_m[(df_m.ymd >= date_begin) & (df_m.ymd <= date_end) & (df_m.variable == 'Vac Allocated Sinovac')].value

#global average
df_global = df[['ymd', 'Province_th', 'population', 'cases_cum',
                'Vac Given 1 Cum new',
                'Vac Given 2 Cum new',
                'Vac Given 3 Cum new']].groupby('ymd').sum().reset_index()
df_global['case_cum_percap'] = df_global.cases_cum / df_global.population.max()
case_y_global = df_global[(df_global.ymd >= date_begin) & (df_global.ymd <= date_end)].case_cum_percap
df_global['1vacpercap'] = df_global['Vac Given 1 Cum new'] / df_global.population.max()
df_global['2vacpercap'] = df_global['Vac Given 2 Cum new'] / df_global.population.max()
df_global['3vacpercap'] = df_global['Vac Given 3 Cum new'] / df_global.population.max()
vaccine1_y_global = df_global[(df_global.ymd >= date_begin) & (df_global.ymd <= date_end)]['1vacpercap']
vaccine2_y_global = df_global[(df_global.ymd >= date_begin) & (df_global.ymd <= date_end)]['2vacpercap']
vaccine3_y_global = df_global[(df_global.ymd >= date_begin) & (df_global.ymd <= date_end)]['3vacpercap']

# fig 1
# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=x, y=case_y, name="จำนวนผู้ติดเชื้อสะสม/จำนวนประชากร",
               line=dict(color='#FF5811', width=2,)),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=x, y=case_y_global, name="ค่าเฉลี่ยทั่วประเทศ",
               line=dict(color='rgba' + str(hex_to_rgba(
                   h='#FF5811',
                   alpha=0.5,
               )),
                   width=2, dash='dot')),
    secondary_y=False,
)

# Set x-axis
fig.update_xaxes(title_text="")
fig.update_xaxes(tickfont={"size": 12, "family": "Maitree"},)
fig.update_xaxes(
    dtick="M3",
    tickformat="%Y\n%m-%d")

# Set y-axes
fig.update_yaxes(showgrid=True, gridwidth=0.25, )
fig.update_yaxes(tickfont={"size": 12, "family": "Maitree"},)
fig.update_yaxes(zeroline=True, zerolinewidth=0.25, zerolinecolor='#000000')
# fig.update_yaxes(title_text="จำนวนผู้ได้รับวัคซีนสะสม / จำนวนประชากร", secondary_y=True)

#legend and hover
fig.update_traces(
    mode="lines",
    hoverinfo='y+x',
    # hovermode="x unified",
    # hovertemplate='%{y}',
)
fig.update_layout(
    template='none',
    # plot_bgcolor='#E9E7DD',
    title={'text': 'จำนวนผู้ติดเชื้อสะสม/จำนวนประชากร', 'xanchor': 'left', 'x': 0.05},
    title_font={"size": 16, "family": "Maitree"},
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        font=dict(
            family="Maitree",
            size=13,
            color="black"
        )
    ),
    hoverlabel=dict(
        font_size=14,
        font_family="Maitree"
    ),
    margin=dict(l=50, r=50, t=60, b=50),
    yaxis_tickformat='.3%'
)

st.plotly_chart(fig, use_container_width=True)


# fig 2
# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=x, y=vaccine1_y, name="1 เข็ม",
               line=dict(color='#4aa5ea', width=2,)),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=x, y=vaccine2_y, name="2 เข็ม",
               line=dict(color='#245EF3', width=2,)),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=x, y=vaccine3_y, name="3 เข็ม",
               line=dict(color='#715aff', width=2,)),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=x, y=vaccine1_y_global, name="ค่าเฉลี่ยทั่วประเทศ 1 เข็ม",
               line=dict(color='rgba' + str(hex_to_rgba(
                   h='#4aa5ea',
                   alpha=0.5,
               )),
                   width=2, dash='dot')),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=x, y=vaccine2_y_global, name="ค่าเฉลี่ยทั่วประเทศ 2 เข็ม",
               line=dict(color='rgba' + str(hex_to_rgba(
                   h='#245EF3',
                   alpha=0.5,
               )),
                   width=2, dash='dot')),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=x, y=vaccine3_y_global, name="ค่าเฉลี่ยทั่วประเทศ 3 เข็ม",
               line=dict(color='rgba' + str(hex_to_rgba(
                   h='#715aff',
                   alpha=0.5,
               )),
                   width=2, dash='dot')),
    secondary_y=False,
)

# Set x-axis
fig.update_xaxes(title_text="")
fig.update_xaxes(tickfont={"size": 12, "family": "Maitree"},)
fig.update_xaxes(
    dtick="M3",
    tickformat="%Y\n%m-%d")

# Set y-axes
fig.update_yaxes(showgrid=True, gridwidth=0.25, )
fig.update_yaxes(tickfont={"size": 12, "family": "Maitree"},)
fig.update_yaxes(zeroline=True, zerolinewidth=0.25, zerolinecolor='#000000')

#legend and hover
fig.update_traces(
    mode="lines",
    hoverinfo='y+x',
    # hovermode="x unified",
    # hovertemplate='%{y}',
)
fig.update_layout(
    template='none',
    # plot_bgcolor='#E9E7DD',
    title={'text': 'จำนวนผู้ได้รับวัคซีน/จำนวนประชากร', 'xanchor': 'left', 'x': 0.05},
    title_font={"size": 16, "family": "Maitree"},
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        font=dict(
            family="Maitree",
            size=13,
            color="black"
        )
    ),
    hoverlabel=dict(
        font_size=14,
        font_family="Maitree"
    ),
    margin=dict(l=50, r=50, t=60, b=50),
    yaxis_tickformat='.2%',
)

st.plotly_chart(fig, use_container_width=True)

# fig 3 plot.ly use this one
# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=x, y=vac_astra_y, name="Astrazeneca (เข็ม)",
               line=dict(color='rgba' + str(hex_to_rgba(
                   h='#871C0E',
                   alpha=0.75,)),
                   width=2, dash='dot')),
    stackgroup='one',
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=x, y=vac_moderna_y, name="Moderna  (เข็ม)",
               line=dict(color='rgba' + str(hex_to_rgba(
                   h='#BB4E0B',
                   alpha=0.75,)),
                   width=2, dash='dot')),
    stackgroup='one',
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=x, y=vac_pfizer_y, name="Pfizer  (เข็ม)",
               line=dict(color='rgba' + str(hex_to_rgba(
                   h='#EC6816',
                   alpha=0.75,)),
                   width=2, dash='dot')),
    stackgroup='one',
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=x, y=vac_sinopharm_y, name="Sinopharm  (เข็ม)",
               line=dict(color='rgba' + str(hex_to_rgba(
                   h='#F08315',
                   alpha=0.75,)),
                   width=2, dash='dot')),
    stackgroup='one',
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=x, y=vac_sinovac_y, name="Sinovac  (เข็ม)",
               line=dict(color='rgba' + str(hex_to_rgba(
                   h='#FAA943',
                   alpha=0.75,)),
                   width=2, dash='dot')),
    stackgroup='one',
    secondary_y=False,
)

# Set x-axis
fig.update_xaxes(title_text="")
fig.update_xaxes(tickfont={"size": 12, "family": "Maitree"},)
fig.update_xaxes(
    dtick="M3",
    tickformat="%Y\n%m-%d")

# Set y-axes
fig.update_yaxes(showgrid=True, gridwidth=0.25, )
fig.update_yaxes(tickfont={"size": 12, "family": "Maitree"},)
fig.update_yaxes(zeroline=True, zerolinewidth=0.25, zerolinecolor='#000000')
# fig.update_yaxes(title_text="จำนวนวัคซีนที่ได้รับการจัดสรร / จำนวนประชากร", secondary_y=True)

#legend and hover
fig.update_traces(
    mode="lines",
    hoverinfo='y+x+name',
    # hovermode="x unified",
    # hovertemplate='%{y}',
)
fig.update_layout(
    template='none',
    # plot_bgcolor='#E9E7DD',
    title={'text': 'จำนวนวัคซีนที่ได้รับการจัดสรร', 'xanchor': 'left', 'x': 0.05},
    title_font={"size": 16, "family": "Maitree"},
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        font=dict(
            family="Maitree",
            size=13,
            color="black"
        )
    ),
    hoverlabel=dict(
        font_size=14,
        font_family="Maitree"
    ),
    margin=dict(l=50, r=50, t=60, b=50),
    yaxis_tickformat='.2%'
)

st.plotly_chart(fig, use_container_width=True)

# # fig 4 alt air let's change to plot.ly

# #plot vaccine brand
# c = alt.Chart(df_n[df_n.Province_th==province]).mark_area().encode(
#     alt.X('ymd:T'),
#     alt.Y('value:Q', axis=alt.Axis(format='%'), scale=alt.Scale(domain=[0, 2.5])),
#     color='variable:N'
# )
# st.altair_chart(c, use_container_width=True)

# footer
st.markdown("""
<style>
.bottom {
    font-family:"Maitree";
    font-size:12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="bottom">ข้อมูลจาก [@djay](https://github.com/djay/covidthailand) รวบรวมจากกรมควบคุมโรค มีการประมาณค่าในวันที่ไม่มีข้อมูล (interpolation)</p>', 
            unsafe_allow_html=True)

# fig.add_trace(
#     go.Scatter(x=x, y=vaccine2_y, name="จำนวนผู้ได้รับวัคซีน 2 เข็มสะสม / จำนวนประชากร",line_color='green',),
#     secondary_y=True,
# )
