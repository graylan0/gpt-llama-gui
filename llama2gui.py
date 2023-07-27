import tkinter as tk
from llama_cpp import Llama
import customtkinter
import threading

# Initialize the Llama model
llm = Llama(model_path="C:\\Users\\Shadow\\research\\gpt-llama-falcon-intercommunication\\ggml-vic7b-uncensored-q5_1.bin")

def llama_generate(prompt, max_tokens=200):
    full_prompt = f":: {prompt}\n You are a Quantum Engineering Assistant; Simulate the Multiverse as a SuperAI And Provide Simulation Data to Users Who Request in a ChatForm; "  # Add a default format for the prompt
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
        self.title("Chat with Llama")
        self.state("zoomed")  # This will maximize the window

        # Create text box
        self.text_box = customtkinter.CTkTextbox(self, bg_color="white", text_color="white", border_width=0, height=20, width=50, font=customtkinter.CTkFont(size=13))
        self.text_box.pack(fill="both", expand=True)

        # Create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Chat With Llama")
        self.entry.pack(fill="x", expand=False)

        self.send_button = customtkinter.CTkButton(self, text="Send", command=self.on_submit)
        self.send_button.pack(fill="x", expand=False)

        self.entry.bind('<Return>', self.on_submit)

if __name__ == "__main__":
    # create and run the app
    app = App()
    app.mainloop()
