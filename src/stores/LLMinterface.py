from abc import ABC , abstractmethod

# we want what ever llm you use to be the same function  , implementation as code no conflication "popular desgin pattern" 
# we need to think about it , the interface doesnt come up with magic u need to think how all the llm will be decoratied it trail and error thing 
class LLMinterface :

    @classmethod
    @abstractmethod
    def set_generation_method(slef, model_id:str):
        pass


    @classmethod
    @abstractmethod
    def set_emmbeding_model(self, model_id:str , embedding_size:int):
        pass

    @classmethod    
    @abstractmethod
    def generate_text(self ,prompt:str , chat_history = [],max_output_tokens:int=None , 
                      temprature:float= None):
        pass

    @classmethod
    @abstractmethod
    # plane text or (query or search) will have different embeddings 
    def embed_text(self, text , document_type :str):
        pass


    @classmethod
    @abstractmethod
    def construct_prompt(self, prompt:str , role:str):
        pass