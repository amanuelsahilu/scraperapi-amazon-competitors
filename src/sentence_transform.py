from sentence_transformers import SentenceTransformer, util
import torch


# Load a pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_parameter(competitor_data):
    sentences = []
    for index,item in enumerate(competitor_data):
        if item['name'] and not item['name']=='':
            sentences.append((index,item['name']))
    return sentences

def find_similarity(product_name,competitor_data,k = 5):
   data = extract_parameter(competitor_data)
   indices = [item[0] for item in data]
   sentences = [item[1] for item in data]
   context = product_name

   sentence_embedding = model.encode(sentences,convert_to_tensor = True)
   context_embedding = model.encode(context,convert_to_tensor = True)
   cos_scores = util.cos_sim(context_embedding,sentence_embedding)[0]
   top_k = torch.topk(cos_scores,k=5)
   return [indices[idx] for idx in top_k.indices]



if __name__ == '__main__':
    top_5 = find_similarity(product_name= "I want wireless earbuds for music",data = data_set)
    print(top_5)



