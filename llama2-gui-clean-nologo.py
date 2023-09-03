from multiprocessing import Process
import subprocess
import threading
import asyncio
import random
import requests
import base64
import io
import sys
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageTk
import customtkinter
import os
import tkinter as tk
from llama_cpp import Llama

def run_batch_file():
    subprocess.run(["webui.bat"], shell=True)

script_dir = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(script_dir, "llama-2-7b-chat.ggmlv3.q8_0.bin")
llm = Llama(model_path=model_path, n_ctx=3999)
executor = ThreadPoolExecutor(max_workers=1)

async def llama_generate_async(prompt):
    loop = asyncio.get_event_loop()
    output = await loop.run_in_executor(executor, lambda: llm(prompt, max_tokens=3999))
    return output

def word_by_word_insert(text_box, message):
    for word in message.split(' '):
        text_box.insert(tk.END, f"{word} ")
        text_box.update_idletasks()
        text_box.after(100)
    text_box.insert(tk.END, '\n')
    text_box.see(tk.END)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.setup_gui()

    def setup_gui(self):
        # Configure window
        self.title("OneLoveIPFS AI")
        self.geometry(f"{1820}x{880}")

        # Configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)


        # Create a label to display the image with a grey background
        self.image_label = tk.Label(self, bg='#202225')
        self.image_label.grid(row=4, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")


        # Create text box
        self.text_box = customtkinter.CTkTextbox(self, bg_color="white", text_color="white", border_width=0, height=20, width=50, font=customtkinter.CTkFont(size=13))
        self.text_box.grid(row=0, column=1, rowspan=3, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Chat With Llama")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.send_button = customtkinter.CTkButton(self, text="Send", command=self.on_submit)
        self.send_button.grid(row=3, column=3, padx=(0, 20), pady=(20, 20), sticky="nsew")

        self.entry.bind('<Return>', self.on_submit)


    def on_submit(self, event=None):
        message = self.entry.get().strip()
        if message:
            self.entry.delete(0, tk.END)
            self.text_box.insert(tk.END, f"You: {message}\n")
            self.text_box.see(tk.END)
            threading.Thread(target=self.generate_response, args=(message,)).start()
            threading.Thread(target=self.generate_images, args=(message,)).start()

    def generate_response(self, message):    
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        full_response = loop.run_until_complete(llama_generate_async(message))

        # Ensure full_response is a dictionary and has the expected keys
        if not isinstance(full_response, dict):
            print(f"Unexpected type for full_response: {type(full_response)}. Expected dict.")
            return

        if 'choices' not in full_response or not full_response['choices']:
            print("No 'choices' key or empty 'choices' in full_response")
            return

        # Extract the text from the first choice
        response_text = full_response['choices'][0].get('text', '')

        # Chunking the response
        max_chunk_size = 2000
        response_chunks = [response_text[i:i + max_chunk_size] for i in range(0, len(response_text), max_chunk_size)]

        for chunk in response_chunks:
            word_by_word_insert(self.text_box, f"AI: {chunk}")  # Update word by word


    def generate_images(self, message):
        url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'
        payload = {
            "prompt": message,
            "steps": 9,
            "seed": random.randrange(sys.maxsize),
            "enable_hr": "false",
            "denoising_strength": "0.7",
            "cfg_scale": "7",
            "width": 1000,
            "height": 427,
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            try:
                r = response.json()
                for i in r['images']:
                    image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))
                    img_tk = ImageTk.PhotoImage(image)
                    self.image_label.config(image=img_tk)
                    self.image_label.image = img_tk
            except ValueError as e:
                print("Error processing image data: ", e)
        else:
            print("Error generating image: ", response.status_code)


if __name__ == "__main__":
    # Run the batch file in a separate process
    batch_file_process = Process(target=run_batch_file)
    batch_file_process.start()

    # Run your tkinter app
    app = App()
    app.mainloop()
