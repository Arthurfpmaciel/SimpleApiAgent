import pandas as pd
import chromadb
from tqdm import tqdm
from typing import List, Optional
from agent.infrastructure.knowledge.semanticSearch.EmbeddingFunction import EmbeddingFunction
from agent.infrastructure.knowledge.semanticSearch.preprocessText import clean_text
embedding_function = EmbeddingFunction()

# configuração base da hnsw do chroma
base_collection_config = {"hnsw:space": "cosine",
                          "hnsw:construction_ef": 100, # tamanho da lista de candidatos para selecionar os vizinhos durante a criação dos índices
                          "hnsw:search_ef":100, # tamanho da lista dinâmica de candidatos durante as buscas por vizinhos, modificável
                          "hnsw:M": 16, # número máximo de vizinhos que cada nó do gráfo pode ter durante a criação dos índices
                          "hnsw:batch_size":100, # número de vetores processados em cada operação de índice, modificável
                          "hnsw:sync_threshold":1000, # quando se deve sincronizar os índices com memória persistente, modificável
                          "hnsw:resize_factor":1.2 # quanto os índices crescem quando precisam mudar de tamanho, modificável
                          }

# configuração reduzida do hnsw do chroma
reduced_collection_config = {"hnsw:space": "cosine",
                          "hnsw:construction_ef": 70,
                          "hnsw:search_ef":70,
                          "hnsw:M": 10,
                          "hnsw:batch_size":100,
                          "hnsw:sync_threshold":1000,
                          "hnsw:resize_factor":1.2}

# configuração melhorada do hnsw do chroma
reconfigs = {"hnsw:search_ef":200,
             "hnsw:batch_size":120,
             "hnsw:sync_threshold":500,
             "hnsw:resize_factor":1.2}

# classe para gerenciar uma coleção chroma
class ChromaCollection:
    def __init__(self, client, collection_name = "collection", embedding_function = embedding_function, collection_config = base_collection_config, ppt_func = clean_text):
        self.client_path = client
        self.client = chromadb.PersistentClient(path=client)
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(name = collection_name, embedding_function = embedding_function, metadata = collection_config)
        self.embedding_function = embedding_function
        self.preprocess_function =  ppt_func
        self.id_col = None

    # adicionar dataframe a coleção
    def add_df(self, df: pd.DataFrame, document_col: str, metadata_cols: List[str], batch_size:int = 5000, limit: Optional[int] = None, append: bool = False):
        count = None
        if append:
            count = self.collection.count()
            df = df.iloc[count:,:]
        if limit is not None:
            df = df.iloc[:limit,:]
        ids = df.index.astype(str).tolist()
        documents = df[document_col].tolist()
        metadatas = df[metadata_cols].to_dict(orient='records')

        for i in tqdm(range(0, len(documents), batch_size), desc="Inserindo batches..."):
            batch_texts = documents[i:i+batch_size]
            batch_metadatas = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+len(batch_metadatas)]
            self.collection.add(documents=batch_texts, ids=batch_ids, metadatas=batch_metadatas)
    
    def encode(self, df: pd.DataFrame, document_col: str):
        df[f"{document_col}_processed"] = df[document_col].apply(self.preprocess_function)
        df = df[df[f"{document_col}_processed"].notna()]
        df = df[df[f"{document_col}_processed"].str.len()>1]
        df[f"id_{document_col}_processed"] = df[f"{document_col}_processed"].astype("category").cat.codes
        self.id_col = f"id_{document_col}_processed"
        return df

    def _getSimilarityDf(self,query_result: List[dict], threshold:float = 0.6):
        if query_result is None:
            return None
        metadatas = query_result["metadatas"][0]
        keys = list(metadatas[0].keys())
        data = {k:[i[k] for i in metadatas] for k in keys}
        data["doc"] = query_result["documents"][0]
        data["similarity"] = [1-i for i in query_result["distances"][0]]
        sim_df = pd.DataFrame(data)
        sim_df = sim_df[sim_df["similarity"]>=threshold].sort_values("similarity", ascending=False)
        return sim_df

    def _getNeighbours(self, description:str, n:int = 1000, threshold:float = 0.6, preprocess:bool = True):
        try:
            if preprocess:
                processed_description = self.preprocess_function(description)
            else:
                processed_description = description 
            emb = self.embedding_function([processed_description])[0]
            result = self.collection.query(query_embeddings = emb, n_results = n)
            sim_df = self._getSimilarityDf(result,threshold)
            return sim_df, processed_description
        except:
            return None, None
        
    def _getNeighboursList(self, descriptions: List[str], n:int = 1000, threshold:float = 0.6, preprocess:bool = True):
            if preprocess:
                processed_descriptions = [self.preprocess_function(description) for description in descriptions]
            else:
                processed_descriptions = descriptions
            embs = self.embedding_function(processed_descriptions)
            results = self.collection.query(query_embeddings = embs, n_results = n)
            results = [{"documents":[results["documents"][i]],
                        "metadatas":[results["metadatas"][i]],
                        "distances":[results["distances"][i]]} if results is not None else None for i in range(len(descriptions))]
            sim_dfs = []
            for result in results:
                sim_df = self._getSimilarityDf(result,threshold)
                sim_dfs.append(sim_df)
            return sim_dfs, processed_descriptions
    
    def semanticSearch(self, docs, n: int = 1000, threshold:float = 0.6, preprocess:bool = True):
        if isinstance(docs, list):
            return self._getNeighboursList(docs, n, threshold, preprocess)
        return self._getNeighbours(docs, n, threshold, preprocess)
    
    def decoder(self, df:pd.DataFrame, neighbours_df:pd.DataFrame, id_col):
        df = df.merge(neighbours_df, on = self.id_col, how='left')
        df = df[df[id_col].notna()]
        return df

    # deletar coleção 
    def delete_collection(self):
        self.client.delete_collection(name=self.collection_name)