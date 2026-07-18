from ..LLMinterface import LLMinterface 
from openai import OpenAI
from helper.config import get_settings
from ..LLMEmums import OpenAIEnum
import logging
class OpenAIProvider(LLMinterface):


    def __init__(self, api_key:str , api_url:str = None,
                 default_input_max_characters:int = 1000,
                 default_generated_max_output_token:int = 1000,
                 default_generation_temperature:float = 0.1):

            self.api_key = api_key
            self.api_url = api_url
            
            self.defautl_input_max_characters = default_input_max_characters
            self.defautl_generated_max_output = default_generated_max_output_token
            self.default_generation_temperature = default_generation_temperature
            
            self.settings = get_settings()
            self.generation_model_id = self.settings.GENERATION_MODEL_ID
            
            self.embedding_model_id = self.settings.EMBEDDING_MODEL_ID
            self.embedding_size = self.settings.EMBEDDING_MODEL_SIZE

            self.enums = OpenAIEnum
            
            self.client = OpenAI(
                  
                  api_key=self.api_key,
                  base_url = self.api_url
            )

            self.logger = logging.getLogger(__name__)
    #because we can change the model while the run time it's important  
    def set_generation_model(self, model_id:str ):
          self.generation_model_id = model_id


    def set_embedding_model(self, model_id: str, embedding_size: int):
     self.embedding_model_id = model_id
     self.embedding_size = embedding_size


#code smells : code will raise error but u dont know where 
   
    def generate_text(self ,prompt:str , chat_history = [],max_output_tokens:int=None , 
                      temprature:float= None):


        
        if not self.client:
             self.logger.error('OpenAI client was not set')
             return None
        

        if not self.generation_model_id:
             self.logger.error('Generation model id for OpenAI was not set')
        
        max_output_tokens = max_output_tokens if max_output_tokens is not None  else self.defautl_generated_max_output
        temprature = temprature if temprature is not None else self.default_generation_temperature
        # system messages = what the llm or agent should do ? 'You are an helpfull assistance' , 'you have a phd in AI  i want you to answer these question ' you norrow him to task you want 
        chat_history.append(self.construct_prompt(prompt=prompt , role=OpenAIEnum.USER.value))

        response = self.client.chat.completions.create(
    model=self.generation_model_id,
    messages=chat_history,
    max_tokens=max_output_tokens,
    temperature=temprature,
        reasoning_effort="none"

)
        
        if not response or not response.choices or len(response.choices) == 0 or not response.choices[0].message:
             self.logger.error('error while  generation text with OpenAI')
             return None
        return response.choices[0].message.content



    def embed_text(self, text:str):
        
        if not self.client:
             self.logger.error('OpenAI client was not set')
             return None
        
        if not self.embedding_model_id:
             self.logger.error(
                  'Embedding model for OpenAI was not set'
             )
             return None

        response = self.client.embeddings.create(
             
             model=self.embedding_model_id,
             input = text 

        )

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
             self.logger.error('error while embedding text with OpenAi')
             return None
        
        return response.data[0].embedding
    

     
    def process_text(self, text:str):
         return text[:self.defautl_input_max_characters].strip()
    

    def construct_prompt(self, prompt:str , role:str):
         return {
              
              'role':role,
              'content': prompt
         }
   


