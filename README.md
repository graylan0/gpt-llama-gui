

# GPT GUI
Requirements: For Windows CPU only

```
pip install customtkinter
pip install torch torchvision torchaudio
pip install transformers
pip install Image
```

Requirements: For Windows GPU

```
pip install customtkinter
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
pip install transformers
pip install Image
```
For Linux Go here
https://pytorch.org/get-started/locally/

(No Prompt Pre Trained Post Trained Generating Transformer)

Gray00 from One Love IPFS created a community inspired Artificial Inteillgence tool using the Free/Open Source GPT-NEO 125M. This GUI uses the Transformers library with a (Zero Pre Orompted) GPT-Neo model, and the customtkinter library to create the user interface.


### Graphical Demo with Quantum Equations
Ubuntu:
![image](https://user-images.githubusercontent.com/34530588/229308122-760ea2cb-8f9c-4b84-b8a3-fdc55854d71b.png)

Windows 10:
![image](https://user-images.githubusercontent.com/34530588/229383244-fd98f89b-480e-4857-8b79-da5f05e5f323.png)


### Features

Loading and configuring the GPT-Neo model and tokenizer: The program loads the GPT-Neo model and tokenizer from the Hugging Face model hub using the Transformers library. It also adds a padding token to the tokenizer and sets the padding token ID in the model configuration.

Generating chunks of text: The program provides a function to split user inputs into smaller chunks of text, to ensure that the inputs do not exceed the maximum input length of the GPT-Neo model.

Generating responses with GPT-Neo: The program provides a function to generate responses to user inputs using the GPT-Neo model. The function encodes the input using the tokenizer, sets the attention mask to exclude the padding tokens, and generates a response using the generate() method of the model. The function also limits the generation time to a specified value and returns the generated response and the time taken to generate it.

Creating a user interface with tkinter: The program uses the tkinter library to create a simple user interface with a text box to display the conversation history and a text entry field to accept user inputs. It also provides a button to submit user inputs and trigger the response generation process.

Writing thoughts to a file: The program writes the user's thoughts to a file using the write_thoughts_to_file() function, which takes the user's thoughts as input, appends a timestamp, and writes the resulting string to a file.

Handling trideque matrix: The program provides a function to handle a trideque matrix, which is a nested list of prompts used to generate responses. The function takes a starting point in the matrix, generates responses to each prompt in the list, and repeats the process a specified number of times or until the user stops the loop.

Managing settings: The program loads settings from a JSON file, including the loop count value used in the trideque function.


### Installation and Requirements


Install Git:
Git is a version control system that allows you to track changes in your code and collaborate with others. To install Git, follow these steps:
a. Go to the Git website at 

https://git-scm.com/downloads

b. Download the appropriate installer for your operating system.
c. Run the installer and follow the instructions.

### Install Python 3.9 with Anaconda:

Anaconda is a distribution of Python that includes many useful packages for data science and scientific computing. To install Python 3.9 with Anaconda, follow these steps:
a. Go to the Anaconda website at 

https://www.anaconda.com/products/individual

b. Download the appropriate installer for your operating system.
c. Run the installer and follow the instructions.
d. During the installation process, make sure to select Python 3.9 as the Python version to install.

### Install the GUI from GitHub using Git clone:

The GUI is hosted on GitHub and can be installed using the Git clone command. Follow these steps to install the GUI:
a. Open a terminal or command prompt.
b. Navigate to the directory where you want to install the GUI.
c. Type the following command to clone the repository: 

`git clone https://github.com/graylan0/gptgui/`
### Install PyTorch:

PyTorch is a popular deep learning framework that can be used to build and train neural networks. To install PyTorch, follow these steps:
a. Open a terminal or command prompt.
b. Make sure that your Anaconda environment is active. You can activate your environment by typing 

`conda activate environment_name`

in the terminal, where "environment_name" is the name of your environment.
c. Type the following command to install PyTorch: 

`conda install pytorch torchvision torchaudio cudatoolkit=11.3 -c pytorch -c nvidia`

This command installs PyTorch with support for CUDA, which is a parallel computing platform used to accelerate deep learning tasks on GPUs. If you do not have a compatible NVIDIA GPU, you can omit the "cudatoolkit=11.3" part of the command.

### Install Customtkinter and any other pip packages needed:

Customtkinter is a custom theme for the tkinter library that provides a modern look and feel for Python GUI applications. To install Customtkinter, follow these steps:
a. Open a terminal or command prompt.
b. Make sure that your Anaconda environment is active. You can activate your environment by typing 

`conda activate environment_name` 

in the terminal, where "environment_name" is the name of your environment.
c. Type the following command to install Customtkinter: 

`pip install customtkinter`

This command installs Customtkinter and any dependencies that it requires. If you need to install other pip packages, you can use the same command, replacing "customtkinter" with the name of the package that you want to install.

Sure, here's a guide on how to use the script, configure the JSON files, run the script, and how the logo works.

### Using the script:
To use the script, run the Python script from the command line or terminal. Once the script is running, you can interact with the chatbot-like interface by typing messages in the text entry field and pressing the "Send" button or the "Enter" key. The program will generate responses to your messages using the GPT-Neo language model and display them in the conversation history box.

Once the repository is cloned, navigate to the directory containing the repository.
Run the Python script to start the GUI.

### Configuring the JSON files:
The script uses two JSON files to store settings and trideque prompts. These files can be edited to configure the behavior of the program. Here's a guide on how to edit these files:

a. `settings.json`: This file contains the following settings:

`loop_count`: The number of times to repeat the trideque prompts. Set to -1 to run indefinitely.
`time_limit`: The maximum time in seconds to generate a response using GPT-Neo. Set to a higher value for longer responses.

b. `trideque.json`: This file contains a nested list of prompts to generate responses using GPT-Neo. Each prompt can be a single sentence or a longer paragraph. To add or remove prompts, simply edit the contents of the file using a text editor.

Running the script:
To run the script, open a command line or terminal window and navigate to the directory containing the Python script. Then, type the following command and press enter:

`python gui.py`

How the logo works:
The logo is displayed in the sidebar of the user interface. It is loaded from a PNG file using the Pillow library, resized to fit the size of the sidebar, and displayed using the tkinter library. The logo file should be named "logo.png" and placed in the same directory as the Python script. If the logo is not displayed correctly, make sure that the file exists and is named correctly. If the size of the logo needs to be changed, modify the logo_img = Image.open(logo_path).resize((140, 77)) line to specify the desired dimensions.
