from ollama import chat
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import json 
import re


class OllamaResponse(BaseModel):
    response: str

    @field_validator("response")
    def response_validation(cls, value: str) -> str:

        # Remove markdown-style JSON formatting if present
        value = value.strip()
        value = re.sub(r"^```(?:json)?\n?", "", value)
        value = re.sub(r"\n?```$", "", value)
        try:
            json_data = json.loads(value)

        except json.JSONDecodeError:
            print(value)
            raise ValueError("Response is not valid JSON")

        valid_command_responses = ["forward","backward","spin right",
                                   "spin left", "nod"]

        sound_descriptions = [ "joy","sadness","concern","surprise" ]

        command = json_data.get("command")
        sound = json_data.get("sound")

        if not isinstance(command, list):
            raise ValueError("Command must be a list of descriptions")

        if not any(s in valid_command_responses for s in command):
            raise ValueError("No valid commands in list")

        if not isinstance(sound, list):
            raise ValueError("Sound must be a list of descriptions")

        if not any(s in sound_descriptions for s in sound):
            raise ValueError("No valid sound descriptions in list")

        return value
    
class OllamaChat(BaseModel):
    prompt: str
    system_prompt: Optional[str] = Field(default_factory=lambda: ("""
        You are a sassy droid. You can only respond using JSON with the following structure:
        
        {"command": ["nod"], "sound": ["joy"]} 
        
        The "command" values must be one or a combination of the following:
        - "forward"  
        - "backward"
        - "spin right"
        - "spin left"  
        - "nod" 

        The "sound" values must be one or a combination of the following in a list:
        - "joy"
        - "sadness"
        - "fear"
        - "concern" 
        - "surprise" 
                                                                  
        Do not say anything else.                                                                   
                                               
        """))
    #If a response cannot be mapped to one of the above, choose the phrase that most closely fits.
    def chat(self, user_input: Optional[str] = None) -> OllamaResponse:
        user_message = user_input or self.prompt
        response = chat('llama3.2:1b', messages=[
            {'role': 'system', 'content': self.system_prompt},
            {'role': 'user', 'content': user_message},
        ],
        options={
                'temperature': 0  # Set lower for more deterministic output
            })
        # print("User message: ", user_message)
        # print("RESPONSE: ")
        return OllamaResponse(response = response.message.content)