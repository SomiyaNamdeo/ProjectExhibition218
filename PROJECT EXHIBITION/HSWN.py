import csv

# Initialize the HSWN data as an empty dictionary
hswn_data = {}

def load_hswn_data(file_path):
    """
    Load the HSWN data from the specified CSV file.
    Returns a dictionary with words as keys and their positive and negative scores as values.
    """
    global hswn_data  # Make sure we modify the global hswn_data variable
    
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        
        for row in reader:
            if len(row) < 5:  # Ensure there are enough columns in the row
                continue
            
            word = row[4].strip()  # Get the sentiment word (assuming it's in the 5th column)
            
            try:
                # Ensure proper float conversion with stripping of unwanted characters or spaces
                pos_score = float(row[2].strip()) if row[2] and row[2].replace('.', '', 1).isdigit() else 0.0
                neg_score = float(row[3].strip()) if row[3] and row[3].replace('.', '', 1).isdigit() else 0.0
            except ValueError as e:
                # Handle cases where conversion to float fails
                print(f"Skipping invalid entry: {row} | Error: {e}")
                continue
            
            hswn_data[word] = (pos_score, neg_score)  # Store in dictionary

def searchHSWN(word):
    """
    Search for the word in the loaded HSWN data and return its polarity.
    Returns 'NF' if the word is not found.
    """
    word = word.strip().lower()  # Normalize the word by stripping spaces and converting to lowercase

    if word in hswn_data:
        pos_score, neg_score = hswn_data[word]
        return pos_score - neg_score  # Return the polarity as the difference between positive and negative scores
    else:
        return 'NF'  # Not found
