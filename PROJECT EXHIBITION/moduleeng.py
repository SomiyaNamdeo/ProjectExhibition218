import HSWN
import translate
def polarity(word):
    """
    Determine the polarity of a word (either from HSWN or by translation).
    
    Parameters:
    word (str): The word to evaluate.
    
    Returns:
    float or str: Returns 1.0 for positive words, -1.0 for negative words, 
                  and 'NF' for not found or neutral.
    """
    # First try to search in the HSWN dictionary for the Hindi word
    polarity_score = HSWN.searchHSWN(word)
    
    if polarity_score != 'NF':
        return polarity_score
    else:
        # If not found in HSWN, attempt translation to English and calculate polarity
        # Only translate if the word is not already found in HSWN
        translated_word = translate.translate(word)
        if translated_word:
            # Search the translated word in the HSWN (English dictionary)
            polarity_score = HSWN.searchHSWN(translated_word)
            if polarity_score != 'NF':
                return polarity_score
            else:
                print(f"Translation of '{word}' to '{translated_word}' returned 'NF' in HSWN.")
        else:
            print(f"Translation failed for word: {word}")
        
        return 'NF'  # If no valid polarity is found (either in HSWN or via translation)
