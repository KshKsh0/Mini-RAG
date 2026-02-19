from ...LLMinterface import LLMinterface 
from ...LLMEmums import CoHereEnums
import cohere
import logging

class CoHereProvider(LLMinterface):
    def __init__(self, api_key:str ,
                 default_input_max_characters:int = 1000,
                 default_generated_max_output_token:int = 1000,
                 default_generation_temperature:float = 0.1):
      

            self.api_key = api_key
            
            self.defautl_input_max_characters = default_input_max_characters
            self.defautl_generated_max_output = default_generated_max_output_token
            self.default_generation_temperature = default_generation_temperature
            
            self.generation_model_id =None
            
            self.embedding_model_id = None
            self.embedding_size = None

            self.client = cohere.ClientV2(api_key=self.api_key)

    def set_generation_model(self, model_id:str ):
          self.generation_model_id = model_id

    
    def set_embedding_mode(self, model_id:str , embedding_size :int):
          self.embedding_model_id = model_id
          self.embedding_size = embedding_size


    def process_text(self, text:str):
         return text[:self.defautl_input_max_characters].strip()
    
    def generate_text(self ,prompt:str , chat_history = [],max_output_tokens:int=None , 
                      temprature:float= None):
          
        if not self.client:
            self.logger.error('OpenAI client was not set')
            return None
        

        if not self.generation_model_id:
             self.logger.error('Generation model id for OpenAI was not set')
        
        max_output_tokens = max_output_tokens if max_output_tokens is not None  else self.defautl_generated_max_output
        temperature = temprature if temprature is not None else self.default_generation_temperature
        # system messages = what the llm or agent should do ? 'You are an helpfull assistance' , 'you have a phd in AI  i want you to answer these question ' you norrow him to task you want 
        chat_history.append(self.construct_prompt(prompt=prompt , role=CoHereEnums.USER.value))
        response = self.client.chat(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )

        if not response or not response.message:
            self.logger.error("Error generating text with Cohere")
            return None
        
        assistant_reply = response.message.content[0].text
        chat_history.append(self.construct_prompt(prompt=assistant_reply , role=CoHereEnums.ASSISTANT.value))
        return assistant_reply


    

    def embed_text(self, text:str , document_type:str =None):
        if not self.client:
            self.logger.error('Cohere client was not set')
            return None
        
        if not self.embedding_model_id:
             self.logger.error('Embedding model id for Cohere was not set')
             return None
        
        input_type = CoHereEnums.DOCUMENT.value if document_type == 'document' else CoHereEnums.QUERY.value
        response = self.client.embed(
            model=self.embedding_model_id,
            input=[self.process_text(text)],
            input_type=input_type,
            embeding_types = ['float']
        )

        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("Error embedding text with Cohere")
            return None
        return response.embeddings.float[0]
    

    def construct_prompt(self, prompt:str , role:str):
         return {
              
              'role':role,
              'content': self.process_text(prompt)
         }
   