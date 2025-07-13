from droid.droid_llama import *
import pytest
import asyncio

def test_ollama():
    ll = OllamaChat(prompt="How are you doing?")
    print(ll.chat())
    print("======================")
    print(ll.chat("What is a fun trick you can do?"))
    print("==========================")
    print(ll.chat("Spin in a circle"))
    print("==========================")
    print(ll.chat("Can you move forward?"))
    print("==========================")
    print(ll.chat("I am not feeling well"))
    print("==========================")

    