import numpy as np
import pandas as pd
import sklearn
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import torch

#import the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def compute_similarity(x,y):
      embedding_1= model.encode(x, convert_to_tensor=True)
      embedding_2 = model.encode(y, convert_to_tensor=True)
      cosi = torch.nn.CosineSimilarity(dim=0)
      output = (cosi(embedding_1, embedding_2)+1)/2
      return output

doc_id="16zMI3339L9uZFGRG275w7DZ0-TlPMd4f8KDdDlrQQuA"
tab_name="Sheet1"
url = "https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}".format(doc_id, tab_name)[:-1]
projects=pd.read_csv(url)


from fastapi import FastAPI, File, UploadFile, HTTPException
app=FastAPI()

@app.get("/")
def root():
    return{"Similarity checker"}

@app.post("/similarity")
def search_match(idea):
  max_score = 0
  most_similar_project_index = None
  for i in range(len(projects["Idea"])):
    score = compute_similarity(idea, str(projects.loc[i, "Idea"])) * 100
    if score > max_score:
      max_score = score
      most_similar_project_index = i

  if max_score > 80:
    msg = "Match Found"
    data = {
      "match": projects.loc[most_similar_project_index, "Idea"],
      "score": round(float(max_score), 2)
    }
  elif 70 <= max_score <= 80:  
    msg = "Neutral"
    data = {
      "match": projects.loc[most_similar_project_index, "Idea"],
      "score": round(float(max_score), 2)
    }
  else:
    msg = "No match"
    data = None  

  return msg, data
