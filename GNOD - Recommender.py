#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Importing data & models
import pandas as pd
import pickle

database = pd.read_csv('db.csv') # 12k songs, clustered into 9 buckets
hot_songs = pd.read_csv('hot_songs.csv') # 240 songs composed of 3 top 100 lists, de-duped

# Standard Scaler
scaler = pickle.load(open('scaler_saved.sav', 'rb'))
# PCA
pca = pickle.load(open('pca_saved.sav', 'rb'))
# Main model (Gaussian Mixtures)
best_model = pickle.load(open('best_model_saved.sav', 'rb'))


# In[110]:


# Song
from IPython.display import Audio
Audio('chariots.wav', autoplay=True)


# In[93]:


# Welcome screen
from time import sleep
gnod = open('gnod.txt','r')
string = gnod.read()

for line in string.split('\n'):
    print(line)
    sleep(0.4)

print(' ')
print('Welcome to GNOD Song Recommender')
print('Please provide a song\'s title and artist name and our sophisticated AI-ML-DeepLearning-Quantum algorithm will suggest your next track!') 
print(' ')


# In[ ]:


import random

# Read user input
song_artist = input('Please enter song artist: ')
song_title = input('Please enter song title: ')

next = 'y'
# If user typed the correct title and artist of a hot song, return any (other) hot song
if hot_songs[(hot_songs['title'] == song_title) & (hot_songs['artist'] == song_artist)].count()[0] > 0:    
    rand_song = hot_songs[(hot_songs['title'] != song_title) & (hot_songs['artist'] != song_artist)].iloc[random.choice(hot_songs.index)]
    new_song = rand_song[0] + ' - ' + rand_song[1]
    print('Hot song entered, why don\'t you try this one then:')
    print('\033[1;32m', new_song)
    sleep(1)
    next = input('Would you like another recommendation? (y/n)')
    while next == 'y':
        rand_song = hot_songs[(hot_songs['title'] != song_title) & (hot_songs['artist'] != song_artist)].iloc[random.choice(hot_songs.index)]
        new_song = rand_song[0] + ' - ' + rand_song[1]
        print('\033[1;32m', new_song)
        sleep(1)
        next = input('Would you like another recommendation? (y/n)')
        
else: # Alternatively, we conduct a search of the song entered on Spotify to assign a similar track from the clustered database  
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials

    secrets_file = open("secrets.txt","r")
    string = secrets_file.read()

    secrets_dict={}
    for line in string.split('\n'):
        if len(line) > 0:
            secrets_dict[line.split(':')[0]]=line.split(':')[1]

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=secrets_dict['cid'], client_secret=secrets_dict['csecret']))

    # Getting the song's features
    search = song_artist +' - '+ song_title
    while sp.search(q=search, limit = 1)['tracks']['items'] == []:
        print('Song not found, try again')
        song_artist = input('Please enter song artist: ')
        song_title = input('Please enter song title: ')
        search = song_artist +' - '+ song_title

    answer = pd.DataFrame([sp.audio_features(sp.search(q=search, limit = 1)['tracks']['items'][0]['uri'])[0]])
    answer = answer[['danceability','energy','loudness','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature']]

    # Applying transformations
    answer_prep = scaler.transform(answer)
    answer_prep_pca = pca.transform(answer_prep)

    # Predicting the cluster
    magic = best_model.predict(answer_prep_pca)[0]

    # Choosing the random song from that clustes
    while next == 'y':
        recommendation = database.loc[random.choice(list(database[database['cluster'] == magic].index))]
        final_recommendation = recommendation[1] + ' - ' + recommendation[0]
        print('This should be fairly similar to your song:')
        print('\033[1;36m', final_recommendation)
        sleep(1)
        next = input('Would you like another recommendation? (y/n)')
        while next == 'y':
            recommendation = database.loc[random.choice(list(database[database['cluster'] == magic].index))]
            final_recommendation = recommendation[1] + ' - ' + recommendation[0]
            print('\033[1;36m', final_recommendation)
            sleep(1)
            next = input('Would you like another recommendation? (y/n)')


# In[ ]:


# End screen
sleep(3)

print(' ')
print('\033[1;37m', 'This was possible thanks to:')
print(' ')

sleep (2)

spoti = open('spoti.txt','r')
string = spoti.read()
for line in string.split('\n'):
    print(line)
    sleep(0.1)
print(' ')
print(' ')
iron = open('iron.txt','r')
string =iron.read()
for line in string.split('\n'):
    print(line)
    sleep(0.1)
    
p.stop()

