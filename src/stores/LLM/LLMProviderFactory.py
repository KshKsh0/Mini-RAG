from .LLMEmums import LLMEnum
from .providers import CoHereProvider , OpenAIProvider , GeminiProvider

class LLMProviderFactory:
    def __init__(self, config:dict):
        self.config = config
    
    def create(self, providers :str):
        if providers == LLMEnum.OPENAI.value:
            return OpenAIProvider(
                api_key = self.config.OPENAI_API_KEY,
                api_url = self.config.OPENAI_API_URL, 
                default_input_max_characters = self.config.INPUT_DAFUALT_MAX_CHARACTERS,
                default_generated_max_output_token = self.config.GENERATION_DAFUALT_MAX_TOKENS,
                default_generation_temperature = self.config.GENERATION_DAFUALT_TEMPERATURE
            )
        if providers == LLMEnum.COHERE.value:
            return CoHereProvider(
                api_key = self.config.COHERE_API_KEY,
                default_input_max_characters = self.config.INPUT_DAFUALT_MAX_CHARACTERS,
                default_generated_max_output_token = self.config.GENERATION_DAFUALT_MAX_TOKENS,
                default_generation_temperature = self.config.GENERATION_DAFUALT_TEMPERATURE
            )
        if providers == LLMEnum.GEMINI.value:
            return GeminiProvider(

                api_key = self.config.GEMINI_API_KEY,
                default_input_max_characters = self.config.INPUT_DAFUALT_MAX_CHARACTERS,
                default_generated_max_output_token = self.config.GENERATION_DAFUALT_MAX_TOKENS,
                default_generation_temperature = self.config.GENERATION_DAFUALT_TEMPERATURE

            )
        return None