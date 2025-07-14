from pydantic import BaseModel
from typing import Optional
from droid.commands import *
from droid.llama import OllamaResponse
from droid.sounds import SoundCommand
import re 
import json
import random

categorized_emotions = {
    "joy": [
        "playful",
        "quirky and hopeful",
        "singsong",
        "happy song",
        "funny",
        "laughing",
        "funny failure",
        "happy chirping"
    ],
    "sadness": [
        "sad",
        "disappointed sadness",
        "confused sad",
        "scared sad",
        "disappointed",
        "quietly scared",
        "sad disappointed",
        "cutesy disappointed"
    ],
    "fear": [
        "worried",
        "excited anxious",
        "shy and scared",
        "scared",
        "quietly scared"
    ],
    "concern": [
        "singsong concerned",
        "happily concerned and nervous",
        "worried and questioning",
        "concerned and questioning",
        "questioning"
    ],
    "surprise": [
        "blaster sounds",
        "explosion"
    ]
}

# tuple of sound bank and sound id. (sound bank, sound Id (within the bank))
sound_code_dict = {
    "worried": (0, 0),
    "excited anxious": (0, 1),
    "singsong, concerned": (0, 2),
    "shy and scared": (0, 3),
    "happily concerned and nervous": (0, 4),
    "playful": (1, 0),
    "quirky and hopeful": (1, 1),
    "singsong": (1, 2),
    "happy song": (1, 3),
    "worried and questioning": (2, 0),
    "questioning": (2, 1),
    "funny": (2, 2),
    "laughing": (2, 3),
    "funny failure": (2, 4),
    "concerned and questioning": (3, 0),
    "scared": (4, 0),
    "sad": (5, 0),
    "disappointed sadness": (5, 1),
    "confused sad": (5, 2),
    "scared sad": (5, 3),
    "disappointed": (6, 1),
    "quietly scared": (6, 2),
    "sad disappointed": (6, 3),
    "cutesy disappointed": (6, 4),
    "happy chirping": (7, 0),
    "blaster sounds": (8, 0),
    "explosion": (8, 1)
}

class ChatTranslation(BaseModel):
    # client: BleakClient
    response: OllamaResponse
    commands: Optional[list[BLECommand]] = None
    sounds: Optional[list[SoundCommand]] = None

    class Config:
        arbitrary_types_allowed = True

    def translate(self):
        value = self.response.response
        print("RESPONSE: ", value)
        value = value.strip()
        value = re.sub(r"^```(?:json)?\n?", "", value)
        value = re.sub(r"\n?```$", "", value)
        try:
            json_data = json.loads(value)
            print("Json data loaded successfully")

        except json.JSONDecodeError:
            print(value)
            raise ValueError("Response is not valid JSON")

        command = list(json_data.get("command",[]))
        sound = list(json_data.get("sound",[]))
        
        sound_selection_lst = []
        # randomly select, sub sounds within each "emotion" category
        for s in sound:
            print("Sound category: ", s)
            sub_list_sounds = categorized_emotions[s.strip().lower()]
            random_number_of_sounds = random.randint(0, len(sub_list_sounds))
            random_selected_sounds = random.sample(sub_list_sounds,random_number_of_sounds)
            sound_selection_lst += random_selected_sounds

        print("Sound selection list: ", sound_selection_lst)
        self.commands = command
        self.sounds = sound_selection_lst
        print("Translation created")
        
    def get_commands(self):
        if self.commands is None:
            return []
        return self.commands
    
    def get_sounds(self):
        if self.sounds is None:
            return []
        return self.sounds

    # async def execute_commands(self):
    #     if len(list(self.command_execution)) <1:
    #         print("No commands to execute")
    #         return
    #     print("executing commands")
    #     for command in list(self.command_execution): 
    #         print("Running command: ", command)
    #         await command.run()
    #         await asyncio.sleep(.5)
        
    # async def execute_sounds(self):
    #     print("executing sounds")
    #     # currently only executing one sound
    #     command = list(self.sound_execution)[0]
    #     await command.run()
    #     await asyncio.sleep(.5)
        # for command in list(self.sound_execution)[:1]:
        #     print("Running sound command: ", command)
        #     await command.run()
        #     await asyncio.sleep(.5)
