import datetime

class TridequeEntry:
    def __init__(self, trideque, matrix=None):
        self.trideque = trideque
        if matrix is None:
            self.matrix = [[["" for _ in range(1)] for _ in range(50)] for _ in range(2)]  # Adjust dimensions according to your trideque matrix size
        else:
            self.matrix = matrix

        self.conversational_history = []
        self.timestamps = []
        self.last_message = ""

    def append_to_buffer(self, text):
        self.last_message = text
        self.conversational_history.append(text)
        self.timestamps.append(datetime.now())
        
    def get_conversational_history(self):
        return self.conversational_history
    
    def get_timestamps(self):
        return self.timestamps
    
    def get_last_message(self):
        return self.last_message