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

def fargeplot(df, rutenettx, rutenetty, farger='Snøskred', aspect=1, tiltak=False, tiltak_plassering=0, femtenlinje=False, meterverdi=0, retning='Mot venstre', justering=0, legend=True):
    #xy = (np.random.random((1000, 2)) - 0.5).cumsum(axis=0)
    xy = df[['M', 'Z']].to_numpy()
    #print(df)
    # Reshape things so that we have a sequence of:
    # [[(x0,y0),(x1,y1)],[(x0,y0),(x1,y1)],...]
    xy = xy.reshape(-1, 1, 2)
    segments = np.hstack([xy[:-1], xy[1:]])
    femten = ein_paa_femten(df, meterverdi, retning, justering)
    tiltak_punkt = vis_tiltak(df, tiltak_plassering)

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
    fig.figimage(img, 100, 50, alpha=0.25)
    ax.add_collection(coll)
    ax.autoscale_view()

    #ticky_space = round(df['Z'].max()/10, -1)
    #tickx_space = round(df['M'].max()/10, -1)
    ax.set_yticks(np.arange(0,df['Z'].max(),rutenetty))
    ax.set_xticks(np.arange(0,df['M'].max(),rutenettx))
    ax.grid(linestyle = '--', linewidth = 0.5)
    if legend:
        ax.legend(handles=legend_elements, title='Helling')
    ax.set_ylabel('Høyde (moh.)')
    ax.set_xlabel('Lengde (m)')
    ax.set_aspect(aspect, 'box')
    ax.set_ylim(df['Z'].min() - 20, df['Z'].max() + 20)
    if tiltak:
        ax.scatter(tiltak_punkt[0], tiltak_punkt[1], marker='x', s=200, color='black', linewidths=3, zorder=10)
        #sirkel = plt.Circle((tiltak_punkt[0], tiltak_punkt[1]), 0.1)
        #ax.add_artist( sirkel )
    if femtenlinje:
        ax.plot(femten[0], femten[1], color='green')
    st.pyplot(fig)
    return

def vis_tiltak(df, meterverdi):
    radnr = df['M'].sub(meterverdi).abs().idxmin()
    M = float(df.iloc[radnr]['M'])
    Z = float(df.iloc[radnr]['Z'])
    return M, Z


def ein_paa_femten(df, meterverdi, retning='Mot venstre', justering=0):
    radnr = df['M'].sub(meterverdi).abs().idxmin()
    M = float(df.iloc[radnr]['M'])
    Z = float(df.iloc[radnr]['Z']) - justering
    M_max = float(df['M'].max())
    liste_x = []
    liste_y = []
    liste_x.append(M)
    liste_y.append(Z)
    if retning == 'Mot venstre':
        liste_x.append(0)
        liste_y.append(Z + M*(1/15))
    if retning == 'Mot høgre':
        liste_x.append(M_max)
        liste_y.append(Z + (M_max-M)*(1/15))
    
    return liste_x, liste_y
 
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
tiltak = False
tiltak_plassering = 0
meterverdi = 0
retning = "Mot høgre"
justering = 0
femtenlinje = False
if uploaded_file is not None:

     # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file, sep=';')
    farge = st.sidebar.radio(
     "Kva fargar skal vises?",
     ('Snøskred', 'Jordskred', 'Stabilitet'))
    aspect = st.sidebar.slider('Kva vertikalskala vil du ha??', 1, 5, 1)
    ticky_space = round(df['Z'].max()/10, -1)
    tickx_space = round(df['M'].max()/10, -1)
    rutenetty = st.sidebar.slider('Avstand rutenett y', 10, 200, int(ticky_space), 10)
    rutenettx = st.sidebar.slider('Avstand rutenett y', 10, 200, int(tickx_space), 10)
    if farge == 'Stabilitet':
        femtenlinje = st.sidebar.checkbox("Vis linje for potensielt løsneområde")
        if femtenlinje:
            meterverdi = st.sidebar.number_input("Gi plassering av linje", 0)
            
            if meterverdi > float(df['M'].max()):
                meterverdi == df['M'].max() - 100
                
            justering = st.sidebar.number_input("Gi justering for line (0.25 x H)", 0)
            retning = st.sidebar.radio('Kva retning skal linje plottes?', ("Mot høgre", "Mot venstre"))
    tiltak = st.sidebar.checkbox("Vis tiltak")
    if tiltak:
        tiltak_plassering = st.sidebar.number_input("Gi plassering for tiltak", 0)
    check = st.sidebar.checkbox("Jamn ut profil")
    tegnforklaring = st.sidebar.checkbox("Vis tegnforklaring", True)
    if check:
        utjamn = st.sidebar.slider('Kva oppløysing ynskjer du?', 1, 100, 10)
        df_plot = terrengprofil(df, True, utjamn)
    else:
        df_plot = terrengprofil(df)

        
    fargeplot(df_plot, rutenettx, rutenetty, farge, aspect, tiltak, tiltak_plassering, femtenlinje, meterverdi, retning, justering, tegnforklaring)


#TODO: 1:15 linje, mot venstre høgre, plassering, justering z.
# fargeplot(df, rutenettx, rutenetty, farger='Snøskred', aspect=1, tiltak=False, tiltak_plassering=None, meterverdi=0, retning='mot_origo', justering=0):