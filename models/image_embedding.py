'''
# Embedding
* 评估文本检索图片的RAG策略，直接通过doc 检索图片/doc图片
* https://huggingface.co/jinaai/jina-clip-v1
* https://huggingface.co/BAAI/bge-visualized
* https://github.com/weaviate/recipes/blob/main/weaviate-features/named-vectors/NamedVectors-ColPali-POC.ipynb
* https://github.com/adithya-s-k/VARAG
* https://adithya-s-k.github.io/VARAG/
* https://github.com/PromtEngineer/localGPT-Vision.git
* https://github.com/OpenBMB/VisRAG
* https://huggingface.co/blog/marco/announcing-mcdse-2b-v1
* https://docs.cohere.com/v2/changelog/embed-v3-is-multimodal
* https://arxiv.org/html/2406.11251?monicaAutoTranslate=1&monicaAutoParallelShowAll=1 如何训练一个image embedding模型 一般是vlm模型基础进行训练微调
* https://github.com/texttron/tevatron/tree/main/examples/dse
'''


class ImageEmbedding():
    def __init__(self):
        '''Constructor
        集成主流image embedding的策略 实现多模态RAG的能力
        '''
        self.desc = "image embedding description"
        
        
    def image_vis_rag(self):
        pass
    
    def image_jina_clip_embedding(self):
        pass
    
    def image_colpali(self):
        pass
        