import re
import string

def load_stopwords(file_path):
    """
    Load stopwords from the provided file.
    """
    stop_words = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            stop_words.add(line.strip().lower())  # Ensure stopwords are in lowercase for comparison
    return stop_words

def preProcess(text, stop_words, remove_stopwords=True, remove_punctuation=True):
    """
    Preprocess the input text by normalizing, tokenizing, and optionally removing stopwords and punctuation.
    
    Parameters:
    text (str): The text to preprocess.
    stop_words (set): A set of stopwords to remove.
    remove_stopwords (bool): Flag to remove stopwords. Default is True.
    remove_punctuation (bool): Flag to remove punctuation. Default is True.
    
    Returns:
    list: A list of processed tokens.
    """
    if text is None or text == '':  # Handle empty or None text
        return []

    # Convert to lowercase
    text = text.lower()

    # Tokenize the text into words (splitting by spaces)
    words = re.findall(r'\b\w+\b', text)  # Tokenize while keeping only alphabetic words
    
    # Remove punctuation if the flag is set
    if remove_punctuation:
        # We remove punctuation except for words like "I'm" and "don't", 
        # which should retain the apostrophe as part of the word
        words = [word.strip(string.punctuation) for word in words]

    # Remove stopwords if the flag is set
    if remove_stopwords:
        words = [word for word in words if word not in stop_words]

    # Return the filtered words as a list
    return words
