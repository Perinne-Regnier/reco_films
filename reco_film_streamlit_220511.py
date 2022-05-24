#!/usr/bin/env python
# coding: utf-8

# In[15]:


#les imports
import scipy
import streamlit as st
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from MyModule import get_img_film
from MyModule import get_img_film2
from MyModule import get_director
import MyModule #import du module de fonctions pour le moteur de recommandation
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from PIL import Image


link = "https://github.com/Perinne-Regnier/csv/blob/master/df_films_zip.csv?raw=true"

if 'df_films' not in st.session_state:
    st.session_state['df_films'] = pd.read_csv(link,compression={'method': 'zip'})


if 'sparse_matrix' not in st.session_state:
    st.session_state['sparse_matrix'] = scipy.sparse.load_npz('matrice_creuse_20220510.npz')



st.set_page_config(
     page_title="Recommandation de films",
     page_icon=":film_frames:",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
        'Get Help':  None,
         'Report a bug': None,
         'About': "# Bienvenue ! # \n"
         "Xavier, Aurélie, Adrian, Guillaume et Périnne vous présentent leur moteur de recommandation de films \n"
         "basé l'algorithme KNN. Celui-ci suppose que des objets similaires existent à proximité dans\n"
         "un espace, nous etudions donc les distances entre les films et vous recommandons : #les plus proches voisins#).\n"
         "Tous les films qui vous seront recommandés sont issus de la base IMDb. \n"
         "Etudiants et étudiantes à la Wild Code School de Nantes \n"
     }
 )

#titre de notre page
st.title("Les cinémas TOM CREUSE présentent")


#création du panneau latérale avec deux paramètres : sélection de films et du nombre de voisins
if 'film_list' not in st.session_state:
    st.session_state['film_list']= list(st.session_state['df_films']['title'].unique())


with st.sidebar:
    st.write("Base de données")
    st.image("https://logos-download.com/wp-content/uploads/2016/11/IMDb_logo_logotype.png", width=100)
    st.metric(f"Nombre de films disponibles",st.session_state['df_films']['title'].count())
    st.subheader("Paramètres à paramétrer héhé")
    selectionFilm = st.selectbox(label = "Choisis un film ", options = st.session_state['film_list'])
    nb_voisins= st.slider('Combien de propositions vous souhaitez ?', 5, 20, 4)+1 # ajout +1 pour affichage correct dataframe des films recommandés
    

##############################paramétrage de notre fonction#########################
#recherche du tconst du film selection
with st.container():
    
    IndexFilmSelection=st.session_state['df_films'].loc[st.session_state['df_films']["title"] == selectionFilm].index
    df_sorted_film_selection = st.session_state['df_films'].loc[IndexFilmSelection][['title','averageRating','numVotes']].sort_values(by=['numVotes'], ascending =False)
    IndexFilmSelection=df_sorted_film_selection.iloc[:1,:].index

    col1, col2 = st.columns(2)
    col1.subheader(f"Tu as aimé : {selectionFilm}")
    col1.image(get_img_film(st.session_state['df_films'].loc[IndexFilmSelection[0]]['tconst']), use_column_width = 'auto')

    col2.metric(f"Année",st.session_state['df_films']['startYear'].iloc[IndexFilmSelection])
    col2.metric(f"Genre",st.session_state['df_films']['genres'].iloc[IndexFilmSelection[0]])
    col2.metric(f"Popularité en nb de votes",st.session_state['df_films']['numVotes'].iloc[IndexFilmSelection].astype(int))
    col2.metric(f"Réalisateur",' '.join(get_director(st.session_state['df_films']['directors'].loc[[IndexFilmSelection[0]]].iloc[0].split(','))))
    

#creation d'une deuxième database qui est scalé
df_scale=st.session_state['df_films'][['averageRating', 'numVotes',
       'startYear', 'runtimeMinutes', 'Action', 'Adult', 'Adventure',
       'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama',
       'Family', 'Fantasy', 'Film-Noir', 'History', 'Horror',
       'Music', 'Musical', 'Mystery', 'News', 'Romance',
       'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']]

#Creation de mon X
X=st.session_state['sparse_matrix'].tocsr()

distanceKNN = NearestNeighbors(n_neighbors=nb_voisins).fit(X)

result=distanceKNN.kneighbors(X[IndexFilmSelection,:])

#je cherche le nom du films dans la vraie base 
name=[]
indexf=[]
st.session_state['df_films'] = st.session_state['df_films'].reindex(columns=['title','startYear','averageRating','numVotes','genres','directors',
                                    'Action', 'Adult', 'Adventure','Animation', 'Biography', 'Comedy',
                                     'Crime', 'Documentary', 'Drama','Family', 'Fantasy', 'Film-Noir',
                                     'History', 'Horror','Music', 'Musical', 'Mystery',
                                     'News', 'Romance','Sci-Fi', 'Short', 'Sport',
                                     'Thriller', 'War', 'Western','inconnu', 'tconst', 'runtimeMinutes'])
for x in np.nditer(result[1]):
    name.append(st.session_state['df_films']["title"].iloc[x])
    indexf.append(x)
    
st.subheader(" Tu vas adorer ces films :")


with st.container():
    col1, col2, col3 = st.columns(3)
    list_img = get_img_film2(st.session_state['df_films'].iloc[indexf[1:4],-2])
    col1.metric(st.session_state['df_films'].iloc[indexf[1].tolist(),0], 1)
    col1.image(list_img[0], use_column_width = 'auto')
    col2.metric(st.session_state['df_films'].iloc[indexf[2].tolist(),0], 2)
    col2.image(list_img[1], use_column_width = 'auto')
    col3.metric(st.session_state['df_films'].iloc[indexf[3].tolist(),0], 3)
    col3.image(list_img[2], use_column_width = 'auto')
    recommandations = pd.DataFrame(st.session_state['df_films'].iloc[indexf,:5])
    recommandations.reset_index(inplace=True)
    recommandations = recommandations.iloc[1:,1:]

    st.write("Et pour encore plus de plaisir, la liste des", nb_voisins-1, 'pépites à binge watcher ...')
    st.dataframe(recommandations)





