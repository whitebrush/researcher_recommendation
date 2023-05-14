
import numpy as np
from openai.embeddings_utils import get_embedding
from sklearn.neighbors import NearestNeighbors
import tiktoken

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191

def clean_research_description(curr_description):
  curr_description = curr_description.replace('\n', '')
  curr_description = curr_description.replace('\t', '')
  curr_description = curr_description.replace('"', '')
  curr_description = curr_description.replace('.', '')
  curr_description = curr_description.replace(',', '')
  curr_description = curr_description.replace('\'', '')
  curr_description = curr_description.replace(':', '')
  curr_description = curr_description.replace('(', '')
  curr_description = curr_description.replace(')', '')
  curr_description = curr_description.replace(':', '')
  curr_description = curr_description.replace('+', '')
  curr_description = curr_description.replace('-', '')
  curr_description = curr_description.replace('1', '')
  curr_description = curr_description.replace('2', '')
  curr_description = curr_description.replace('3', '')
  curr_description = curr_description.replace('4', '')
  curr_description = curr_description.replace('5', '')
  curr_description = curr_description.replace('6', '')
  curr_description = curr_description.replace('7', '')
  curr_description = curr_description.replace('8', '')
  curr_description = curr_description.replace('9', '')
  curr_description = curr_description.replace('0', '')
  curr_description = curr_description.replace('/', '')
  curr_description = curr_description.replace('\\', '')
  curr_description = curr_description.replace('\'', '')
  curr_description = ' '.join(curr_description.split())  
  curr_description = curr_description.lower()
  return curr_description

def find_nearest_pis(pi_df, student_description, top_k=5):
  pi_matrix = np.array(np.array(pi_df.embedding.apply(eval)).tolist())
  neigh = NearestNeighbors(n_neighbors=5)
  neigh.fit(pi_matrix)

  encoding = tiktoken.get_encoding(embedding_encoding)
  msu_student_info = {}
  msu_student_info['description'] = clean_research_description(student_description)
  msu_student_info['n_tokens'] = len(encoding.encode(msu_student_info['description']))
  msu_student_info["embedding"] = get_embedding(msu_student_info['description'], engine=embedding_model)
  print(neigh.kneighbors(np.array([msu_student_info["embedding"]]))[1].tolist())
  p_df = pi_df.loc[neigh.kneighbors(np.array([msu_student_info["embedding"]]))[1][0].tolist()].copy().reset_index(drop=True)
  print(p_df)
  return p_df