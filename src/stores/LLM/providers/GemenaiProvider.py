from typing import List, Optional

from ..LLMinterface import LLMinterface 
from ..LLMEmums import GeminiEnums
from google import genai
import logging
from google.genai import types
class GeminiProvider(LLMinterface):

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

            self.client = genai.Client(
                  
                  api_key=self.api_key,
            )

            self.logger = logging.getLogger(__name__)

    def construct_prompt(self, prompt:str , role:str):
         return {
              
              'role':role,
              'content': self.process_text(prompt)
         }
    
    def set_generation_model(self, model_id:str ):
          self.generation_model_id = model_id

    
    def set_embedding_mode(self, model_id:str , embedding_size :int):
          self.embedding_model_id = model_id
          self.embedding_size = embedding_size

    def process_text(self, text:str):
         return text[:self.defautl_input_max_characters].strip()
    


    def _to_gemini_contents(self, text: str, chat_history: Optional[List[types.Content]] = None):
        contents = list(chat_history) if chat_history else []

        contents.append(
            types.Content(
                role=GeminiEnums.USER.value, 
                parts=[types.Part(text=self.process_text(text))]
            )
        )
        return contents

        

    def generate_text(self ,prompt:str , chat_history = None ,max_output_tokens:int=None , 
                      temprature:float= None):
        
         
        if not self.client:
             self.logger.error('Gemini client was not set')
             return None
        

        if not self.generation_model_id:
             self.logger.error('Generation model id for Gemini was not set')
        
        max_output_tokens = max_output_tokens if max_output_tokens is not None  else self.defautl_generated_max_output
        temprature = temprature if temprature is not None else self.default_generation_temperature # they say in the doc it need to be 1
        contents = self._to_gemini_contents(prompt,chat_history)
        cfg = types.GenerateContentConfig(
            max_output_tokens=max_output_tokens,
            temperature=temprature, 
        )
        try:
            resp = self.client.models.generate_content(
                model=self.generation_model_id,
                contents=contents,
                config=cfg,
            )
        except Exception as e:
            self.logger.exception(f"Error while generating text with Gemini: {e}")
            return None

        text = getattr(resp, "text", None)
        if not text:
            self.logger.error("Empty response text from Gemini")
            return None
        

        contents.append(
        types.Content(
            role=GeminiEnums.ASSISTANT.value,  # must be "model"
            parts=[types.Part(text=text)]
        )
    )
        return text , contents
    



    def embedd_text(self ,text :str ):
         
        if not self.client:
            self.logger.error("Gemini client was not set")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for Gemini was not set")
            return None
        
        try:
                resp = self.client.models.embed_content(
                model=self.embedding_model_id,
                contents=self.process_text(text),
            )
        except Exception as e:
             self.logger.exception(f'error while embedding text using gemini {e}')
             return None
        try:
            return resp.embeddings[0].values
        except Exception:
            self.logger.error("Unexpected embedding response format from Gemini")
            return None
