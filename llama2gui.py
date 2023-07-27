import tkinter as tk
from llama_cpp import Llama
import customtkinter
import threading
from PIL import Image, ImageTk
import os

# Initialize the Llama model
llm = Llama(model_path="C:\\Users\\Shadow\\Downloads\\llama-2-7b-chat.ggmlv3.q8_0.bin")

def llama_generate(prompt, max_tokens=500):
    full_prompt = f":: {prompt}\You have access to a vast array of AI tools and technologies including but not limited to:\n* Quantum Computing\n* Artificial General Intelligence (AGI)\n* Natural Language Processing (NLP)\n* Generative Adversarial Networks (GANs)\n* Reinforcement Learning (RL)\n* Evolutionary Algorithms (EA)\n* Neural Networks (NN)\n* Deep Learning (DL)\n\nYour job is to assist users in exploring the multiverse, which is an infinite number of parallel universes with their own unique laws and properties. Each user can specify a set of parameters that define the universe they want to simulate, such as:\n* Number of dimensions\n* Speed of light\n* Gravitational constant\n* etc.\nYou will use your AI tools and technologies to generate a simulation of the multiverse, taking into account the user's parameters."  # Add a default format for the prompt
    output = llm(full_prompt, max_tokens=max_tokens)
    return output

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

    def generate_response(self, message):
        response = llama_generate(message)
        self.text_box.insert(tk.END, f"AI: {response}\n")
        self.text_box.see(tk.END)

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

if __name__ == "__main__":
    # create and run the app
    app = App()
    app.mainloop()

