import tkinter as tk
import threading
import os
import time
import requests
import numpy as np
import base64
from collections import deque
from dataclasses import dataclass
from typing import List, Dict
from PIL import Image, ImageTk
from llama_cpp import Llama
import bisect
import customtkinter
import requests
from PIL import Image
from io import BytesIO
import io
import sys
import random

# Initialize the Llama model
llm = Llama(model_path="C:\\Users\\Shadow\\Downloads\\llama-2-7b-chat.ggmlv3.q8_0.bin")

def llama_generate(prompt, max_tokens=500):
    output = llm(prompt, max_tokens=max_tokens)
    return output

@dataclass
class CharacterProfile:
    name: str
    age: int
    occupation: str
    skills: List[str]
    relationships: Dict[str, str]

class Memory:
    def __init__(self, content, priority=0):
        self.content = content
        self.priority = priority
        self.timestamp = time.time()

class TriDeque:
    def __init__(self, maxlen):
        self.data = deque(maxlen=maxlen)

    def push(self, memory):
        # Insert memory in order of priority
        index = bisect.bisect([m.priority for m in self.data], memory.priority)
        self.data.insert(index, memory)

    def remove(self, memory):
        # Remove a specific memory item
        self.data.remove(memory)

    def update_priority(self, memory, new_priority):
        # Remove the memory item
        self.remove(memory)
        # Update its priority
        memory.priority = new_priority
        # Re-insert it with the new priority
        self.push(memory)

    def __iter__(self):
        # Make the TriDeque iterable
        return iter(self.data)

class CharacterMemory:
    MAX_PAST_ACTIONS = 100  # maximum number of past actions to store in memory

    def __init__(self):
        self.attributes = {}
        self.past_actions = TriDeque(self.MAX_PAST_ACTIONS)  # Initialize a TriDeque with a size of MAX_PAST_ACTIONS
        self.color_code = "white"  # default color
        self.profile = CharacterProfile("John Doe", 40, "Detective", ["Investigation", "Hand-to-hand combat"], {"Sarah": "Wife", "Tom": "Partner"})

    def update_attribute(self, attribute, value):
        self.attributes[attribute] = value
        if attribute == "mood":
            self.update_color_code(value)

    def update_color_code(self, mood):
        if mood == "happy":
            self.color_code = "yellow"
        elif mood == "sad":
            self.color_code = "blue"
        elif mood == "angry":
            self.color_code = "red"
        else:
            self.color_code = "white"

    def add_past_action(self, action, priority=0):
        memory = Memory(action, priority)
        self.past_actions.push(memory)

@dataclass
class StoryEntry:
    story_action: str
    narration_result: str

class StoryGenerator:
    MAX_PAST_ENTRIES = 100  # maximum number of past entries to store in memory

    def __init__(self, character_memory):
        self.character_memory = character_memory
        self.past_story_entries = TriDeque(self.MAX_PAST_ENTRIES)  # Initialize a TriDeque with a size of MAX_PAST_ENTRIES
        initial_prompt = self.construct_initial_prompt()
        self.past_story_entries.push(
            StoryEntry(
                story_action='',
                narration_result=initial_prompt
            )
        )

    def construct_initial_prompt(self):
        rules = """Create a writing prompt to start an Multiverse text adventure game.  Adhere to the following rules:
                    1. The story in a randomly generated location with 4 Dimentional Space Coordnates given to the Prompt.
                    2. You should describe the player's characteristics, where they are, what time period they are in, and what surrounds them, their name, their age, their emotional coloring
                    3. In the Game AI can Simulate SpaceTime and HyperTime.
                    4. Use the 2nd person perspective.
                    5. The prompt should be only 3 - 5 sentences long."""
        initial_prompt = llama_generate(rules)
        return initial_prompt

    def construct_prompt_messages(self, story_action: str):
        messages = [
            {
                'role': 'system',
                'content': """Please perform the function of a text adventure game, following the rules listed below:

                            Presentation Rules:

                            1. At each turn, the user says an action and you reply with a multiverse generaiton portal forecasting events in the future based upon the events that happen in the story based on the action the user performed.

                            2. Stay in character as a powerful high throughput multiverse simulator

                            Fundamental Game Mechanics:

                            1. If an action is unsuccessful, respond with a relevant errorlog.


                            Start Simulator.""",
            },
        ]
        for story_entry in self.past_story_entries:
            if story_entry.story_action:
                messages += [{'role': 'user',
                              'content': story_entry.story_action}]
            if story_entry.narration_result:
                messages += [
                    {
                        'role': 'assistant',
                        'content': story_entry.narration_result,
                    }
                ]
        # Add character's past actions to the messages
        for action in self.character_memory.past_actions:
            messages.append({'role': 'user', 'content': action.content})
        messages.append({'role': 'user', 'content': story_action})
        return messages

    def generate_next_story_narration(self, story_action: str):
        """Generates the continuation of the story given a user action"""
        next_narration = llama_generate(story_action)
        self.past_story_entries.push(
            StoryEntry(story_action=story_action,
                       narration_result=next_narration)
        )
        return next_narration

    def reset(self):
        self.past_story_entries = TriDeque(self.MAX_PAST_ENTRIES)  # Reset it before calling construct_initial_prompt
        initial_prompt = self.construct_initial_prompt()
        self.past_story_entries.push(
            StoryEntry(
                story_action='',
                narration_result=initial_prompt
            )
        )

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.setup_gui()

    def on_submit(self, event=None):
        message = self.entry.get().strip()
        if message:
            self.entry.delete(0, tk.END)
            self.text_box.insert(tk.END, f"You: {message}\n")
            self.text_box.see(tk.END)
            threading.Thread(target=self.generate_response, args=(message,)).start()
            threading.Thread(target=self.generate_images, args=(message,)).start()

    def generate_response(self, message):
        response = llama_generate(message)
        self.text_box.insert(tk.END, f"AI: {response}\n")
        self.text_box.see(tk.END)

    def generate_images(self, message):
        url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'
        payload = {
            "prompt": message,
            "steps" : 50,
            "seed" : random.randrange(sys.maxsize),
            "enable_hr": "false",
            "denoising_strength": "0.7",
            "cfg_scale" : "7",
            "width": 512,
            "height": 512,
            "restore_faces": "true",
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            try:
                r = response.json()
                for i in r['images']:
                    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
                    img_tk = ImageTk.PhotoImage(image)
                    self.image_label.config(image=img_tk)
                    self.image_label.image = img_tk  # keep a reference to the image
            except ValueError as e:
                print("Error processing image data: ", e)
        else:
            print("Error generating image: ", response.status_code)

    def setup_gui(self):
        # Configure window
        self.title("OneLoveIPFS AI")
        self.geometry(f"{1100}x{580}")

        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        # Load logo image and display in sidebar frame
        logo_path = os.path.join(os.getcwd(), "logo.png")
        logo_img = Image.open(logo_path).resize((140, 77))  # Add the .resize() method with the desired dimensions
        logo_photo = ImageTk.PhotoImage(logo_img)  # Convert PIL.Image to tkinter.PhotoImage
        self.logo_label = tk.Label(self.sidebar_frame, image=logo_photo, bg=self.sidebar_frame["bg"])  # Create a tkinter.Label
        self.logo_label.image = logo_photo  # Keep a reference to the image
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))  # This is the correct position for the logo_label grid statement

        # Create text box
        self.text_box = customtkinter.CTkTextbox(self, bg_color="white", text_color="white", border_width=0, height=20, width=50, font=customtkinter.CTkFont(size=13))
        self.text_box.grid(row=0, column=1, rowspan=3, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Chat With Llama")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.send_button = customtkinter.CTkButton(self, text="Send", command=self.on_submit)
        self.send_button.grid(row=3, column=3, padx=(0, 20), pady=(20, 20), sticky="nsew")

        self.entry.bind('<Return>', self.on_submit)

        # Create a label to display the image
        self.image_label = tk.Label(self)
        self.image_label.grid(row=4, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

if __name__ == "__main__":
    # create and run the app
    app = App()
    app.mainloop()

