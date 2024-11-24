# tagger.py

def getTag(post):
    # A simple example of tagging logic
    # For demonstration, we return a list of tags for the words in the post.
    # In a real application, you would implement your own tagging logic.
    tags = []
    words = post.split()  # Split the post into words
    for word in words:
        # Dummy tagging logic: 
        # Let's just tag all words as 'NN' (noun) for simplicity.
        tags.append((word, 'NN'))  # Replace 'NN' with actual tagging logic as needed
    return tags# tagger.py

def getTag(post):
    # A simple example of tagging logic
    # For demonstration, we return a list of tags for the words in the post.
    # In a real application, you would implement your own tagging logic.
    tags = []
    words = post.split()  # Split the post into words
    for word in words:
        # Dummy tagging logic: 
        # Let's just tag all words as 'NN' (noun) for simplicity.
        tags.append((word, 'NN'))  # Replace 'NN' with actual tagging logic as needed
    return tags