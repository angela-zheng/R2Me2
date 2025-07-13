from flask import Flask, jsonify, request
from flask_cors import CORS
from droid.connect import DroidConnection
from droid.commands import (InitConnectionSequence, MotorControl, HeadTurnRight, 
                            HeadTurnLeft, SpinRight, SpinLeft, HeadNodNo)
from droid.llama import OllamaChat 
from droid.translation import ChatTranslation,sound_code_dict
from droid.sounds import SoundCommand
import asyncio 
import threading
import time 

def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def run_on_ble_loop(coro):
    loop = app.config["BLE_LOOP"]
    return asyncio.run_coroutine_threadsafe(coro, loop).result()

# init Flask app 
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

# begin Asyncio event loop
background_loop = asyncio.new_event_loop()
loop_thread = threading.Thread(target=start_background_loop, args=(background_loop,), daemon=True)
loop_thread.start()
app.config["BLE_LOOP"] = background_loop

# Connecting to the droid
@app.route('/connect', methods=['POST'])
def connect_droid():
    try:
        print("connecting.....")
        droid_connection = run_on_ble_loop(DroidConnection.connect())
        print("Connected", droid_connection)
        client = droid_connection.get_client()
        sequenceInit = InitConnectionSequence(client=client)
        run_on_ble_loop(sequenceInit.run())
        app.config["CLIENT"] = client
        return "success"
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/forward', methods=['POST'])
def droid_forward():
    try:
        client = app.config.get("CLIENT")
        move_forward = MotorControl(motor_forward = True,
                                motor_power = 80,
                                client = client,
                                delay_ms = .5)
        run_on_ble_loop(move_forward.run())
        return("success")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/back', methods=['POST'])
def droid_back():
    try:
        client = app.config.get("CLIENT")
        move_back = MotorControl(motor_forward = False,
                                motor_power = 80,
                                client = client,
                                delay_ms = .5)
        run_on_ble_loop(move_back.run())
        return("success")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/turnleft', methods=['POST'])
def droid_left():
    try:
        client = app.config.get("CLIENT")
        spin_left = SpinLeft(client=client,
                                delay_ms=.5)
        run_on_ble_loop(spin_left.run())
        asyncio.sleep(0.5)
        print("turn left")
        return("success")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/turnright', methods=['POST'])
def droid_right():
    try:
        client = app.config.get("CLIENT")
        spin_right = SpinRight(client=client,
                                delay_ms=.5)
        asyncio.sleep(0.5)
        run_on_ble_loop(spin_right.run())
        print("turn right")
        return("success")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/turnheadright', methods=['POST'])
def droid_headright():
    try:
        client = app.config.get("CLIENT")
        head_right = HeadTurnRight(client=client,
                                delay_ms=.5)
        asyncio.sleep(0.5)
        run_on_ble_loop(head_right.run())
        print("head turn right")
        return("success")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/turnheadleft', methods=['POST'])
def droid_headleft():
    try:
        client = app.config.get("CLIENT")
        head_left = HeadTurnLeft(client=client,
                                delay_ms=.5)
        asyncio.sleep(0.5)
        run_on_ble_loop(head_left.run())
        print("head turn left")
        return("success")
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route('/chat', methods=['POST','GET'])
def droid_chat():
    print("chat called")
    client = app.config.get("CLIENT")

    prompt_json = request.get_json()
    print("PROMPT JSON", prompt_json)
    llama_response = OllamaChat(prompt=prompt_json)
    chat_response = llama_response.chat()
    print("LLAMA RESPONSE", chat_response)
    translated_chat = ChatTranslation(response = chat_response)

    translated_chat.translate()
    print("Translated chat")
    commands = translated_chat.get_commands()
    sounds = translated_chat.get_sounds()
    
    # process commands 
    for c in commands: 
        c = c.strip().lower()
        if c == "forward":
            command_exec = MotorControl(client=client, 
                                        motor_forward=True,
                                        motor_power=80,
                                        ms_delay=.5)
            run_on_ble_loop(command_exec.run())
            time.sleep(.1)
        elif c == "backward":
            command_exec = MotorControl(client=client, 
                                        motor_forward=False,
                                        motor_power=80,
                                        ms_delay=.5)
            run_on_ble_loop(command_exec.run())
            time.sleep(.1)
        elif c == "spin right":
            command_exec = SpinRight(client=client,
                                        ms_delay=1)
            run_on_ble_loop(command_exec.run())
            time.sleep(.1)
        elif c == "spin left":
            command_exec = SpinLeft(client=client,
                                    ms_delay=1)
            run_on_ble_loop(command_exec.run())
            time.sleep(.1)
        elif c == "nod":
            command_exec = HeadNodNo(client=client)
            run_on_ble_loop(command_exec.run())
            time.sleep(.1)
        else:
            command_exec = HeadNodNo(client=client)
            run_on_ble_loop(command_exec.run())
            time.sleep(.1)

    s = sounds[0]
    sound_codes = sound_code_dict[s]
    try:
        print("trying to run sound command")
        sound_command = SoundCommand(
                                        client = client,
                                        sound_bank_id = sound_codes[0],
                                        sound_id = sound_codes[1],
                                        ms_delay = .5    
                                    )
        print("Sound command created: ", sound_command)
        run_on_ble_loop(sound_command.run())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
                
    return("success")
    
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)