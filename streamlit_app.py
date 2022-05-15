import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm

#st.set_page_config(layout="wide")

def fargeplot(df, farger='Snøskred'):
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
                Line2D([0], [0], marker='o', color='w', label='0 - 27',
                        markerfacecolor='grey', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='27-30',
                        markerfacecolor='green', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='30-35',
                        markerfacecolor='yellow', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='35-40',
                        markerfacecolor='orange', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='40-45',
                        markerfacecolor='orangered', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='45-50',
                        markerfacecolor='darkred', markersize=15),
                    Line2D([0], [0], marker='o', color='w', label='50-90',
                        markerfacecolor='black', markersize=15),
        ]
    if farger == 'Jordskred':
        cmap = ListedColormap(['grey', 'palegreen', 'green', 'greenyellow', 'orange', 'orangered', 'darkred'])
        norm = BoundaryNorm([0, 3, 10, 15, 25, 45, 50, 90], cmap.N)
        legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='0 - 3',
                markerfacecolor='grey', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='3-10',
                markerfacecolor='palegreen', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='10-15',
                markerfacecolor='green', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='15-25',
                markerfacecolor='greenyellow', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='25-45',
                markerfacecolor='orange', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='45-50',
                markerfacecolor='orangered', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='50-90',
                markerfacecolor='darkred', markersize=15),
        ]
    if farger == 'Stabilitet':
        cmap = ListedColormap(['blue','palegreen' , 'green', 'greenyellow','yellow', 'orange', 'orangered', 'red', 'darkred', 'black']) #8
        norm = BoundaryNorm([0, 2.9, 3.8, 5.7, 14, 26.6, 33.7, 45, 63.4, 71.6, 90], cmap.N) #10
        #1:20, 1:15, 1:10, 1:4, 1:2, 1:1,5, 1:1, 2:1, 3:1 100:1
        legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='< 1:20',
                markerfacecolor='blue', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:20 - 1:15',
                markerfacecolor='palegreen', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:15 - 1:10',
                markerfacecolor='green', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:10 - 1:4',
                markerfacecolor='greenyellow', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:4 - 1:2',
                markerfacecolor='yellow', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:2 - 1:1',
                markerfacecolor='orange', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='1:1 - 2:1',
                markerfacecolor='red', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='2:1 - 3:1',
                markerfacecolor='darkred', markersize=15),
            Line2D([0], [0], marker='o', color='w', label='> 3:1',
                markerfacecolor='black', markersize=15)
        ]

    fig, ax = plt.subplots(figsize=(15,10))
    coll = LineCollection(segments, cmap=cmap, norm=norm)
    #coll = LineCollection(segments, cmap=plt.cm.gist_ncar)
    coll.set_array(df.Vinkel)
    coll.set_linewidth(3)

    ax.add_collection(coll)
    ax.autoscale_view()
    ax.grid(linestyle = '--', linewidth = 0.5)
    ax.legend(handles=legend_elements)
    ax.set_aspect('equal', 'box')
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

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:

     # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file, sep=';')
    farge = st.radio(
     "Kva fargar skal vises?",
     ('Snøskred', 'Jordskred', 'Stabilitet'))
    check = st.checkbox("Jamn ut profil")
    if check:
        utjamn = st.slider('Kva oppløysing ynskjer du?', 1, 100, 10)
        df_plot = terrengprofil(df, True, utjamn)
        fargeplot(df_plot, farge)
    else:
        df_plot = terrengprofil(df)
        fargeplot(df_plot, farge)