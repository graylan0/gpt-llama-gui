
stop_loop = False  # global variable to stop loop

def generate_chunks(input_text, chunk_size=200):
    """
    Splits input text into chunks of the given size.
    """
    chunks = []
    current_chunk = ""
    for word in input_text.split():
        if len(current_chunk) + len(word) + 1 <= chunk_size:
            current_chunk += " " + word
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks