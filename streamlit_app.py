import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.image as image

st.set_page_config(layout="wide")

#st.set_page_config(layout="wide")
with open('logo (Phone).png', 'rb') as file:
    img = image.imread(file)

def fargeplot(df, rutenettx, rutenetty, farger='Snøskred', aspect=1, tiltak=False, tiltak_plassering=None):
    #xy = (np.random.random((1000, 2)) - 0.5).cumsum(axis=0)
    xy = df[['M', 'Z']].to_numpy()

    # Reshape things so that we have a sequence of:
    # [[(x0,y0),(x1,y1)],[(x0,y0),(x1,y1)],...]
    xy = xy.reshape(-1, 1, 2)
    segments = np.hstack([xy[:-1], xy[1:]])

    if farger == 'Snøskred':
        cmap = ListedColormap(['grey', 'green', 'yellow', 'orange', 'orangered', 'red', 'darkred'])
        norm = BoundaryNorm([0, 27, 30, 35, 40, 45, 50, 90], cmap.N)
        legend_elements = [
                Line2D([0], [0], marker='o', color='w', label='0 - 27\N{DEGREE SIGN}',
                        markerfacecolor='grey', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='27-30\N{DEGREE SIGN}',
                        markerfacecolor='green', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='30-35\N{DEGREE SIGN}',
                        markerfacecolor='yellow', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='35-40\N{DEGREE SIGN}',
                        markerfacecolor='orange', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='40-45\N{DEGREE SIGN}',
                        markerfacecolor='orangered', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='45-50\N{DEGREE SIGN}',
                        markerfacecolor='darkred', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='50-90\N{DEGREE SIGN}',
                        markerfacecolor='black', markersize=15),
        ]
    if farger == 'Jordskred':
        cmap = ListedColormap(['grey', 'palegreen', 'green', 'greenyellow', 'orange', 'orangered', 'darkred'])
        norm = BoundaryNorm([0, 3, 10, 15, 25, 45, 50, 90], cmap.N)
        legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='0 - 3\N{DEGREE SIGN}',
                markerfacecolor='grey', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='3-10\N{DEGREE SIGN}',
                markerfacecolor='palegreen', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='10-15\N{DEGREE SIGN}',
                markerfacecolor='green', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='15-25\N{DEGREE SIGN}',
                markerfacecolor='greenyellow', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='25-45\N{DEGREE SIGN}',
                markerfacecolor='orange', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='45-50\N{DEGREE SIGN}',
                markerfacecolor='orangered', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='50-90\N{DEGREE SIGN}',
                markerfacecolor='darkred', markersize=15),
        ]
    if farger == 'Stabilitet':
        cmap = ListedColormap(['blue','aquamarine' , 'lime', 'green','yellow', 'orange', 'orangered', 'red', 'black']) #8
        norm = BoundaryNorm([0, 2.9, 3.8, 5.7, 14, 26.6, 33.7, 45, 63.4, 90], cmap.N) #10
        #1:20, 1:15, 1:10, 1:4, 1:2, 1:1,5, 1:1, 2:1, 3:1 100:1
        legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='< 1:20',
                markerfacecolor='blue', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:20 - 1:15',
                markerfacecolor='aquamarine', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:15 - 1:10',
                markerfacecolor='lime', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:10 - 1:4',
                markerfacecolor='green', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:4 - 1:2',
                markerfacecolor='yellow', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:2 - 1:1.5',
                markerfacecolor='orange', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:1.5 - 1:1',
                markerfacecolor='orangered', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='> 1:1',
                markerfacecolor='red', markersize=15)
        ]

    fig, ax = plt.subplots(figsize=(15,10))
    coll = LineCollection(segments, cmap=cmap, norm=norm)
    #coll = LineCollection(segments, cmap=plt.cm.gist_ncar)
    coll.set_array(df.Vinkel)
    coll.set_linewidth(3)
    
    ax.add_collection(coll)
    ax.autoscale_view()
    #ticky_space = round(df['Z'].max()/10, -1)
    #tickx_space = round(df['M'].max()/10, -1)
    ax.set_yticks(np.arange(0,df['Z'].max(),rutenetty))
    ax.set_xticks(np.arange(0,df['M'].max(),rutenettx))
    ax.grid(linestyle = '--', linewidth = 0.5)
    ax.legend(handles=legend_elements, loc='best', title='Helling')
    ax.set_ylabel('Høyde (moh.)')
    ax.set_xlabel('Lengde (m)')
    ax.set_aspect(aspect, 'box')
    fig.figimage(img, 100, 50, alpha=0.25)
    st.pyplot(fig)
    return


 
def terrengprofil(df, utjamning=False, opplosning=None):
    if utjamning == True:
        df = df.groupby(np.arange(len(df))//opplosning).mean()
    z = df['Z'].tolist()
    m = df['M'].tolist()
    h = []
    #Rekner ut hellinger, litt uelegant utanfor pandas, men funker..
    for i in range(len(z)):
        h.append((z[i] - z[i -1])/(m[i] - m[i - 1])) 
    df['Helning'] = h
    df['Vinkel'] = abs(np.degrees(np.arctan(df['Helning'])))
    return df

st.header('Profilverktøy')
st.write('Leser csv filer fra profilverktøyet på Høydedata.no')

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

     # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file, sep=';')
    farge = st.sidebar.radio(
     "Kva fargar skal vises?",
     ('Snøskred', 'Jordskred', 'Stabilitet'))
    aspect = st.sidebar.slider('Kva vertikalskala vil du ha??', 1, 5, 1)
    check = st.sidebar.checkbox("Jamn ut profil")
    if check:
        utjamn = st.sidebar.slider('Kva oppløysing ynskjer du?', 1, 100, 10)
        df_plot = terrengprofil(df, True, utjamn)
        ticky_space = round(df_plot['Z'].max()/10, -1)
        tickx_space = round(df_plot['M'].max()/10, -1)
        rutenetty = st.sidebar.slider('Avstand rutenett y', 10, 200, int(ticky_space), 10)
        rutenettx = st.sidebar.slider('Avstand rutenett y', 10, 200, int(tickx_space), 10)
        fargeplot(df_plot, rutenettx, rutenetty, farge, aspect)

    else:
        df_plot = terrengprofil(df)
        ticky_space = int(round(df_plot['Z'].max()/10, -1))
        print(ticky_space)
        tickx_space = int(round(df_plot['M'].max()/10, -1))
        print(tickx_space)
        rutenetty = st.sidebar.slider('Avstand rutenett y', 10, 200, ticky_space, 10)
        rutenettx = st.sidebar.slider('Avstand rutenett y', 10, 200, tickx_space, 10)
        fargeplot(df_plot, rutenettx, rutenetty, farge, aspect)
        



#TODO: 1:15 linje, mot venstre høgre, plassering, justering z.