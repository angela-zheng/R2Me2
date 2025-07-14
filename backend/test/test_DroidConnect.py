import pytest
import asyncio
from droid.connect import DroidConnection
from droid.sounds import SoundCommand
from droid.translation import ChatTranslation, sound_code_dict
from droid.commands import *
from droid.llama import OllamaChat
WRITE_UUID = "09b600b1-3e42-41fc-b474-e9c0c8f0c801"

@pytest.mark.asyncio

async def test_droid_connection():
    d_connect = await DroidConnection.connect()
    print("Connected", d_connect)
    #await d_connect.get_device_services()
    # await d_connect.test()

    client = d_connect.get_client()
    response = OllamaChat(prompt="Translate this to Droid language: Move forward and play a happy sound.").chat()
    translated_chat = ChatTranslation(response = response)
    # print("Created translation")
    # async def run_all():
    translated_chat.translate()
    # commands = translated_chat.get_commands()
    sounds = translated_chat.get_sounds()

    # for c in commands:
    #     command_mapper[c.strip().lower()]
    #     asyncio.run(command_mapper[c.strip().lower()].run())
    #     asyncio.sleep(.1)
    s = sounds[0]
    sound_codes = sound_code_dict[s]
    sound_command = SoundCommand(
                                    client = client,
                                    sound_bank_id = sound_codes[0],
                                    sound_id = sound_codes[1],
                                    ms_delay = .5    
                                )
    await sound_command.run()

    # sound = SoundCommand(client = client,
    #                      sound_bank_id = 1,
    #                      sound_id = 1,
    #                      ms_delay = .05)
    # await sound.run()   
    # init connection sequence 
    # sequenceInit = InitConnectionSequence(client=client)
    # await sequenceInit.run()


    # # move forward 
    # move_forward = MotorControl(motor_forward = True,
    #                             motor_number = 1,
    #                             motor_power = 80,
    #                             client = client,
    #                             delay_ms = .05)
    # await move_forward.run()
    # # test = '8000'

    # # # Head Right
    # head_right = HeadTurnRight(client=client, 
    #                            delay_ms = .3)
    # await head_right.run()

    # # Head turn Left
    # head_left = HeadTurnLeft(client=client, 
    #                            delay_ms = .5)
    # await head_left.run()

    # spin_right = SpinRight(client=client,
    #                        delay_ms = 5)
    # await spin_right.run() 

    # head_nod = HeadNodNo(client=client,
    #                        delay_ms = .5)
    # await head_nod.run()

    # spin_left = SpinLeft(client=client,
    #                      delay_ms = 5)
    # await spin_left.run()

    # client.disconnect()


############################
# Sound Bank: 27420F4444001F01
############################
# # Sounds like, a fart. Idk 
#     await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F01"))
#     await asyncio.sleep(.05)
#     await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001800"))

# # do, do, do, sounds like quirky? Hopeful? 
#     await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F01"))
#     await asyncio.sleep(.05)
#     await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001801"))

# # singsong
#     await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F01"))
#     await asyncio.sleep(.05)
#     await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001802"))

# # singsong, sounds happy, longish
#     await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F01"))
#     await asyncio.sleep(.05)
#     await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001803"))

###############
# 27420F4444001F00
###############
# Sounds worried? 
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F00"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001800"))

# A little quicker, sound anxious?
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F00"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001801"))

# # singsong, sounds concerned
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F00"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001802"))

# # Sounds shy/scared 
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F00"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001803"))

# singing a song. Slightly happy/concerned 
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F00"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001804"))


###############
# 27420F4444001F02
###############
# Sounds worried/questioning
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F02"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001800"))

# Longer, questioning
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F02"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001801"))

# # Kinda funny sounds
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F02"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001802"))

# # Kinda funny, longer, honk honk like a clown
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F02"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001803"))

# # Funny, like he failed at something 
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F02"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001804"))


###############
# 27420F4444001F03
###############
# Sounds worried/questioning
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F03"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001800"))


###############
# 27420F4444001F04
###############
# Weird sound, like scared. Reminds me of squidward
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F04"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001800"))

###############
# 27420F4444001F05
###############
# Sounds like he failed
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F05"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001800"))

# Failure, womp womp
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F05"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001801"))

# singsong, chirp chirp, questioning/failure
#     await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F05"))
#     await asyncio.sleep(.05)
#     await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001802"))

# Sounds questioning and scared
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F05"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001803"))


###############
# 27420F4444001F06
###############
# another Failure, womp womp
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F06"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001801"))

# awwwwooooo do, scared failure - kinda quiet
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F06"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001802"))

# Not happy, quiet, disappointed
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F06"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001803"))

# disappointed, cute and funny
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F06"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001804"))

###############
# 27420F4444001F07
###############
# Vroom up, sounds like happy chirping
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F07"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001800"))

###############
# 27420F4444001F0A
###############
#  Blaster sounds
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F0A"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001800"))

# Explosion
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001F0A"))
    # await asyncio.sleep(.05)
    # await client.write_gatt_char(WRITE_UUID, bytes.fromhex("27420F4444001801"))
