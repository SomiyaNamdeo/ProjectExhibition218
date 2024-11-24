# Example function that returns multiplying factors for words based on some logic
def getMF(tagdata):
    MFlist = []
    
    for word, tag in tagdata:
        if tag == 'NN':  # Noun
            MFlist.append([word, 1.0, 'NN'])
        elif tag == 'VB':  # Verb
            MFlist.append([word, 1.5, 'VB'])
        elif tag == 'JJ':  # Adjective
            MFlist.append([word, 1.2, 'JJ'])
        elif tag == 'RB':  # Adverb
            MFlist.append([word, 1.1, 'RB'])
    
    return MFlist
