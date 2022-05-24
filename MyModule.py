
# import pour la classe filmAdvisor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

# import pour la fonction get_img_film
from bs4 import BeautifulSoup
import requests
import matplotlib.image as mpimg
from IPython.display import Image, HTML

df_1=pd.read_csv('table_nconst_names_1.zip',compression={'method': 'zip'})
df_2=pd.read_csv('table_nconst_names_2.zip',compression={'method': 'zip'})
df_3=pd.read_csv('table_nconst_names_3.zip',compression={'method': 'zip'})
df_4=pd.read_csv('table_nconst_names_4.zip',compression={'method': 'zip'})
df_5=pd.read_csv('table_nconst_names_5.zip',compression={'method': 'zip'})
df_6=pd.read_csv('table_nconst_names_6.zip',compression={'method': 'zip'})
df_7=pd.read_csv('table_nconst_names_7.zip',compression={'method': 'zip'})
df_nconst_names=pd.concat([df_1, df_2,df_3, df_4, df_5, df_6, df_7], ignore_index=True)


#--------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------- DEBUT DE LA CLASSE FILMDAVISOR---------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------


class filmAdvisor:

    #def __init__(self,dataSet, features, nb_voisins=5):

    def __init__(self, features, nb_voisins=5):
        

        # df_title_ratings2=pd.read_csv('title.ratings.tsv',sep='\t')
        # df_title_basics2=pd.read_csv('title.basics.tsv',sep='\t',usecols=["tconst","titleType","primaryTitle","isAdult",
        #                                                                      "startYear","runtimeMinutes","genres"])
        # df_test=pd.merge(df_title_ratings2,df_title_basics2, how="inner", on="tconst")
        # df_test=df_test.loc[df_test["titleType"]=="movie"]
        # del df_test["titleType"]
        # del df_test["isAdult"]
        # del df_test["startYear"]

        # df_test_genres=df_test
        # df_test_genres=pd.concat([df_test_genres,df_test_genres["genres"].str.get_dummies(sep=",")],axis=1)
        # df_test_genres["runtimeMinutes"]=df_test_genres["runtimeMinutes"].apply(lambda x : np.NaN if x=="\\N" else x)
        # df_test_genres=df_test_genres.dropna(subset=["runtimeMinutes"])
        # df_test_genres.loc[df_test_genres["runtimeMinutes"]=="\\N"].value_counts()
        # del df_test_genres["genres"]
        # df_test_genres=df_test_genres.rename(columns={'\\N':"inconnu"})

        
        link = "https://github.com/Perinne-Regnier/csv/blob/master/df_test.csv?raw=true"
        df_test_genres = pd.read_csv(link,compression={'method': 'zip'})


        self.dataSet = df_test_genres
        self.dataSet_scaled = self.dataSet
        self.filmRecoList =[]
        self.filmRecoList_tconst = []
        self.features = features
        self.nb_voisins = nb_voisins
        self.model = NearestNeighbors(n_neighbors=nb_voisins).fit(self.dataSet[self.features])


       

    def get_film_advise(self,film0rigine, nb_voisins):
        self.nb_voisins = nb_voisins
        distance, index_result=self.model.kneighbors(self.dataSet.loc[self.dataSet["primaryTitle"]==str(film0rigine),self.features], n_neighbors= self.nb_voisins)
        self.filmRecoList= [self.dataSet.iloc[x]["primaryTitle"] for x in index_result[0].tolist()]
        #self.filmRecoList_tconst = [self.dataSet.iloc[x]["tconst"] for x in index_result[0].tolist()]
        #self.filmRecoList= [self.dataSet.iloc[x].index for x in index_result[0].tolist()]
        return self.filmRecoList
        #return index_result

    def scaling_model(self):
        # #self.scaler = StandardScaler().fit(self.dataSet[self.features])
        # self.scaler = StandardScaler().fit(self.dataSet)
        # #self.X_train_scaled = pd.DataFrame(self.scaler.transform(self.dataSet[self.features]))
        # self.X_train_scaled = pd.DataFrame(self.scaler.transform(self.dataSet))
        # self.dataSet_scaled = self.X_train_scaled
        # self.model = NearestNeighbors(n_neighbors=self.nb_voisins).fit(self.dataSet_scaled[self.features])


        # partie copié sur script de Périnne ------------------------------
        #creation d'une deuxième database qui est scalé
        df_scale=df_films[['averageRating', 'numVotes',
       'startYear', 'runtimeMinutes', 'Action', 'Adult', 'Adventure',
       'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama',
       'Family', 'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror',
       'Music', 'Musical', 'Mystery', 'News', 'Reality-TV', 'Romance',
       'Sci-Fi', 'Short', 'Sport', 'Talk-Show', 'Thriller', 'War', 'Western']]

        #Creation de mon X
        self.X= self.dataSet
        # Mon model scaler transforme  datas
        self.scaler = StandardScaler().fit(X)
        self.X_train_scaled = self.scaler.transform(X)

        #je définis mon X_scale qui va me permettre d'ajuster le poids des variables
        self.X_scaled=pd.DataFrame(self.X_train_scaled, columns=self.X.columns)

        #je multiplie le scale de l'année par 10 pour que la distance soit plus longue et donc je "mets" du poids sur cette donnée
        self.X_scaled["startYear"]=self.X_scaled["startYear"]*10
        #je definis et entraine le model de voisinage sur la base de X_scaled que j'ai modifié
        self.model = NearestNeighbors(n_neighbors=self.nb_voisins).fit(self.X_scaled)

        result_dist, result_index=distanceKNN.kneighbors(X_scaled.iloc[IndexFilmSelection,:])

        # ----------------------------------------------------------------------


    
    def get_dataSet(self):
         return self.dataSet


#--------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------- FIN DE LA CLASSE FILMADVISOR ----------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------- DEBUT DE LA FONCTION DE RECUPERATION D'UNE IMAGE DE FILM ------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------

def get_img_film(tconst):
    
    title_name = tconst
    vgm_url = 'https://www.imdb.com/title/'+title_name +'/'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    images = soup.findAll('img')
    example = images[0]
    image_film_adr = example.attrs['src']
    url_ext = example.attrs['src'] #The extension you pulled earlier
    full_url = vgm_url + url_ext #Combining first 2 variables to create       a complete URL
    r = requests.get(full_url, stream=True) #Get request on full_url
    if r.status_code == 200:                     #200 status code = OK
       with open(image_film_adr, 'wb') as f: 
          r.raw.decode_content = True
          shutil.copyfileobj(r.raw, f)
    
    img = mpimg.imread(image_film_adr,format='.jpg')
    return (img)

def get_img_film2(List_tconst):
    
    # fonction renvoyant une liste d'images à partir d'une liste d'identifiants tconst de films 
    img=[]
    for tconst in List_tconst:
        title_name = tconst
        vgm_url = 'https://www.imdb.com/title/'+title_name +'/'
        html_text = requests.get(vgm_url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        images = soup.findAll('img')
        example = images[0]
        image_film_adr = example.attrs['src']
        url_ext = example.attrs['src'] #The extension you pulled earlier
        full_url = vgm_url + url_ext #Combining first 2 variables to create       a complete URL
        r = requests.get(full_url, stream=True) #Get request on full_url
        if r.status_code == 200:                     #200 status code = OK
           with open(image_film_adr, 'wb') as f: 
              r.raw.decode_content = True
              shutil.copyfileobj(r.raw, f)
        
        img.append(mpimg.imread(image_film_adr,format='.jpg'))
        
    return (img)

#--------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------- FIN DE LA FONCTION DE RECUPERATION D'UNE IMAGE DE FILM --------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------- DEBUT DE LA FONCTION DE RECUPERATION DU NOM DU REALISATEUR ----------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------
def get_director(list_nconst):
    
    global df_nconst_names
    #df_nconst_names=pd.read_csv('table_nconst_names.csv',compression={'method': 'zip'})
    list_dir=[]
    for nm in list_nconst:
        list_dir.append(df_nconst_names['primaryName'].loc[(df_nconst_names['nconst']==nm)].to_string(index=False))
    return list_dir
#--------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------- FIN DE LA FONCTION DE RECUPERATION DU NOM DU REALISATEUR ------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------
