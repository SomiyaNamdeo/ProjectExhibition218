import HSWN
import preprocess
import tagger
import translate
import sys
import openpyxl  # For reading .xlsx files
import re
import MF  # Multiplying factors
from moduleeng import polarity  # Ensure this is correctly imported
import os  # To check if the file exists

# Load HSWN data
HSWN.load_hswn_data('HSWN.csv')

# Load stopwords from the stopwords.txt file
stop_words = preprocess.load_stopwords('stopwords.txt')

# Check if the correct number of arguments are passed
if len(sys.argv) != 2:
    print(f"Error: {len(sys.argv)} arguments passed.")
    input_file = input("Please enter the input file name (e.g., input_filename.xlsx): ").strip()  # Remove leading/trailing spaces
    if not input_file:
        sys.exit("No file provided. Exiting the program.")
else:
    input_file = sys.argv[1].strip()  # Remove any accidental spaces

# Ensure the file exists
if not os.path.exists(input_file):
    sys.exit(f"Error: The file '{input_file}' does not exist.")

# Read the corpus (input file)
posts = []

# Open the Excel file using openpyxl
try:
    book = openpyxl.load_workbook(input_file)  # Load the workbook
    sheet = book.active  # Get the active sheet
except Exception as e:
    sys.exit(f"Error opening the Excel file: {e}")

# Read data from the second column (assuming it contains the posts)
for row in sheet.iter_rows(min_row=2, min_col=2, max_col=2, values_only=True):
    if row[0]:  # Check if the post is not None or empty
        posts.append(row[0])

# Write posts with polarity to output CSV
with open('OUTPUT.csv', 'w+', encoding='utf-8') as writeDoc:
    writeDoc.write("PostID,Polarity\n")  # Write header

    # STEP 1 - Apply preprocessing
    for i in range(len(posts)):
        if posts[i]:  # Ensure that the post is not None or empty
            processed_post = preprocess.preProcess(posts[i], stop_words)
            # Ensure processed_post is a string; join if it's a list
            if isinstance(processed_post, list):
                processed_post = ' '.join(processed_post)
            posts[i] = processed_post

    # STEP 2 - Actual work
    sno = 1
    for post in posts:
        totalPol = 0.0

        # Get the tag data for the post
        tagdata = tagger.getTag(post)  
        MFlist = MF.getMF(tagdata)  # List of multiplying factors

        for word in post.split(' '):
            # Skip words that are URLs, mentions, or hashtags using regular expressions
            if re.match(r'^(https?://|www\.)|^@|^#|^//', word):
                print(f"Skipping non-text word: '{word}'")
                continue

            mult = 1  # Default multiplier
            typ = None

            # Get multiplier for the word
            for mf in MFlist:
                if mf[0] == word:
                    mult = mf[1]
                    typ = mf[2]  # Word tag (e.g., NN, VB, etc.)
                    break

            # Get the sentiment polarity score for the word
            word_pol = polarity(word)  # Call the imported 'polarity' function
            if word_pol != 'NF':
                totalPol += word_pol * mult  # Apply multiplier to the sentiment score

        # Determine final polarity for the post based on total sentiment score
        final_polarity = 1 if totalPol > 0.1 else -1 if totalPol < -0.1 else 0
        writeDoc.write(f"{sno},{final_polarity}\n")  # Write results to output CSV
        sno += 1
