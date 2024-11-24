from googletrans import Translator

def translate(word):
    translator = Translator()
    try:
        # Attempt translation from Hindi to English
        translation = translator.translate(word, src='hi', dest='en')
        
        # Check if translation is valid
        if translation.text:
            return translation.text
        else:
            print(f"Translation failed for word: {word}")
            return None
    except Exception as e:
        print(f"Error in translation for word '{word}': {e}")
        return None
