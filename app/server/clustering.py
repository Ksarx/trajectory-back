from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from nltk.corpus import stopwords
from pathlib import Path

import numpy as np
import docx
import pandas as pd
import nltk
import pymorphy2
import re
import json
import os

BASE_DIR = Path(__file__).resolve(strict=True).parent

nltk.download("stopwords")
stop_words = stopwords.words(["russian", "english"])
morph = pymorphy2.MorphAnalyzer()

def model_work(filePath, direction_name, profile_name):
  doc = docx.Document(filePath)
  
  description = []
  discipline_names = []
  for table in doc.tables:
    for i, row in enumerate(table.rows):
        if ("Факультативные дисциплины" in row.cells[1].text ):
          break
        if (row.cells[0].text == '' or i == 0):
          continue
        discipline_names.append(row.cells[1].text.split("\n", maxsplit=1)[0])
        description.append(row.cells[4].text)

  df = pd.DataFrame(list(zip(discipline_names, description)),
                columns =['name', 'description'])
  df['description'] = normalizing_desc(list(df['description']))
  df = df.groupby(['name'], as_index= False ).agg({'description': ' '. join })

  text = list(df['description'])
  vectorizer = TfidfVectorizer(max_df = 0.8, min_df=0.1)
  X = vectorizer.fit_transform(text)
  
  clusters, model = clustering_kmeans(X, text)

  df['cluster'] = clusters['cluster']
  df = df.drop(columns=['description'])
  
  n_clusters = df.cluster.unique().size
  
  top_n_words = 3  
  cluster_words = []

  for i in range(n_clusters):
    cluster_indices = np.argsort(model.cluster_centers_[i])[::-1][:top_n_words]
    words = [vectorizer.get_feature_names_out()[idx] for idx in cluster_indices]
    cluster_words.append(words)


  cluster_names = [" ".join(words) for words in cluster_words]
  
  names = {}
  for i, name in enumerate(cluster_names):
    names[i] = name

  result = []
  for cluster, group in df.groupby('cluster'):
      disciplines = []
      for name in group['name']:
          disciplines.append(name)
      result.append({'name': names[cluster], 'disciplines': disciplines})
  
  final_result = {
    "direction": direction_name,
    "profile": profile_name,
    "fields": result
  }
  return final_result    
  
    
    
    
def normalizing_desc(data):
  result = []
  for i in range(len(data)):
    s = data[i]
    s = s.lower()
    s = re.sub(r"[^А-Яа-яA-Za-z]+", " ", s)
    after = re.search(r'знать\s*(.*)', s)
    s = after.group(1)
    s = re.sub(r"\b(?:владеть|уметь|ид|ук)\b", "", s)
    words = s.split()
    filtered_words = [word for word in words if word not in stop_words]
    normalized_text = ' '.join([morph.parse(word)[0].normal_form for word in filtered_words])
    result.append(normalized_text)
  return result

def clustering_kmeans(X, text):
    sil = []
    kmax = 6

    for k in range(2, kmax+1):
      kmeans = KMeans(n_clusters = k).fit(X)
      labels = kmeans.labels_
      sil.append(silhouette_score(X, labels, metric = 'euclidean'))

    optimal_k = np.argmax(sil) + 2
    model = KMeans(n_clusters=optimal_k, max_iter=600, random_state=42)
    model.fit(X)
    labels = model.labels_

    clusters=pd.DataFrame(list(zip(text,labels)),columns=['title','cluster'])
    return clusters, model