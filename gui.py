import torch
from transformers import GPT2Tokenizer, GPTNeoForCausalLM
import customtkinter
import json
import os
from customtkinter import CTkImage
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Frame, Scrollbar, Y, END
from customtkinter.windows.widgets import ctk_textbox
import threading
from datetime import datetime
import time

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = GPTNeoForCausalLM.from_pretrained('EleutherAI/gpt-neo-125M').to(device)
tokenizer = GPT2Tokenizer.from_pretrained('EleutherAI/gpt-neo-125M')

# add padding token to tokenizer
tokenizer.add_special_tokens({'pad_token': '[PAD]'})

# set padding token id to the id of the padding token
model.config.pad_token_id = tokenizer.pad_token_id

stop_loop = False

# Load settings and bot token from the JSON file
with open('settings.json', 'r') as settings_file:
    settings = json.load(settings_file)

# Get the loop count value
loop_count = settings['loop_count']

# Load trideque matrix from the JSON file
with open('trideque.json', 'r') as trideque_file:
    trideque = json.load(trideque_file)

def generate_chunks(prompt, chunk_size=1500):
    words = prompt.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def gpt3_generate(model, tokenizer, chunk, max_length=2000, time_limit=50.0):
    start_time = time.time()

    inputs = tokenizer.encode(chunk, return_tensors='pt', truncation=True, max_length=512).to(device)
    attention_mask = inputs.ne(tokenizer.pad_token_id).float().to(device)
    outputs = model.generate(inputs, max_length=max_length, do_sample=True, max_time=time_limit, attention_mask=attention_mask)

    response = tokenizer.decode(outputs[0])
    end_time = time.time()

    return response, end_time - start_time

def on_stop_loop_click():
    global stop_loop
    stop_loop = True
    
class App(customtkinter.CTk):
    def __init__(self, gpt3):
        super().__init__()
        self.gpt3 = gpt3
        self.send_button = None  # Add this line to define send_button attribute
        self.setup_gui()

    def on_submit(self, event=None):
        message = self.entry.get().strip()
        if message:
            self.entry.delete(0, END)
            self.text_box.insert(END, f"You: {message}\n")
            self.text_box.see(END)
            self.send_button.configure(text="Thinking...")
            threading.Thread(target=self.generate_response, args=(message, 20)).start()  # Set loop_limit to 20 or any other value
            self.write_thoughts_to_file(message)  # Add this line to call the function

    def write_thoughts_to_file(self, thoughts):
        with open('thoughtswrite.txt', 'a', encoding='utf-8') as thoughts_file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            thoughts_file.write(f"{timestamp}: {thoughts}\n")

    def generate_response(self, message, loop_limit=-1):
        loop_count = 0
        while loop_limit == -1 or loop_count < loop_limit:
            # Read the contents of thoughts.txt using UTF-8 encoding
            with open('thoughts.txt', 'r', encoding='utf-8') as thoughts_file:
                thoughts_content = thoughts_file.read()

            # Prepend the thoughts_content to the message
            message_with_thoughts = thoughts_content + "\n" + message

            response, _ = gpt3_generate(self.gpt3, tokenizer, message_with_thoughts)
            self.text_box.insert(END, f"AI: {response}\n")
            self.text_box.see(END)
            self.send_button.configure(text="Send")

            time.sleep(1)  # Pause for 1 second between responses
            loop_count += 1  # Increment the loop counter

    def send_chunks(self, trideque_point, output_text, loop_count=-1):
        stop_loop = False
        total_time = 0.0
        repetition = 0


        if 0 <= trideque_point < len(self.trideque):
            while (loop_count == -1 or repetition < loop_count) and not stop_loop:
                for topic in self.trideque[trideque_point]:
                    prompt_chunks = self.generate_chunks(topic)
                    for chunk in prompt_chunks:
                        gpt3_response, response_time = self.gpt3_generate(chunk)
                        total_time += response_time
                        output_text.insert(END, f"{topic}: {gpt3_response}\n")

                repetition += 1

            output_text.insert(END, f"Total response time: {total_time:.2f} seconds.\n")
        else:
            output_text.insert(END, "Invalid trideque point. Please enter a valid index.\n")

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




    # Create text box and scroll bar
        self.text_frame = Frame(self, bg="white")
        self.text_frame.grid(row=0, column=1, rowspan=3, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.text_frame.grid_propagate(False)  # prevent frame from expanding
        self.text_box = customtkinter.CTkTextbox(self.text_frame, bg_color="white", text_color="white", border_width=0, height=20, width=50, font=customtkinter.CTkFont(size=13))
        self.text_box.pack(side="left", fill="both", expand=True)
        self.scrollbar = customtkinter.CTkScrollbar(self, command=self.text_box.yview)
        self.text_box.configure(yscrollcommand=self.scrollbar.set)

    # Create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Chat With Dave")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.entry.bind('<Return>', self.on_submit)

    # Define send_button
        self.send_button = customtkinter.CTkButton(self, text="Send", command=self.on_submit)
        self.send_button.grid(row=3, column=3, padx=(0, 20), pady=(20, 20), sticky="nsew")

    # Bind the Return key event to the entry widget
        self.entry.bind('<Return>', self.on_submit)

if __name__ == "__main__":
    # create and run the app
    app = App(model)
    app.mainloop()
 
