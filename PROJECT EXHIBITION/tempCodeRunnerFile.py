# algo.py
# -*- coding: utf-8 -*-

import HSWN
import preprocess
import MF
import tagger
import sys
import openpyxl  # Use openpyxl for reading .xlsx files
import translate
import moduleeng

# Check if the correct number of arguments are passed
if len(sys.argv) != 2:
    sys.exit("Usage: python algo.py <input_filename.xlsx>")

# Read the corpus
posts = []

# Open the Excel file using openpyxl
try:
    book = openpyxl.load_workbook(sys.argv[1])  # Load the workbook
    sheet = book.active  # Get the active sheet
except Exception as e:
    sys.exit(f"Error opening the Excel file: {e}")

# Read data from the second column (assuming it contains the posts)
for row in sheet.iter_rows(min_row=2, min_col=2, max_col=2, values_only=True):
    if row[0]:  # Check if the post is not None or empty
        posts.append(row[0])

# Write posts with polarity
with open('OUTPUT.csv', 'w+') as writeDoc:
    writeDoc.write("PostID,Polarity\n")  # Write header

    # STEP 1 - Apply preprocessing
    for i in range(len(posts)):
        if posts[i]:  # Ensure that the post is not None or empty
            processed_post = preprocess.preProcess(posts[i])
            # Ensure processed_post is a string; join if it's a list
            if isinstance(processed_post, list):
                processed_post = ' '.join(processed_post)
            posts[i] = processed_post

    # STEP 2 - Actual work
    sno = 1
    for post in posts:
        totalPol = 0.0

        tagdata = tagger.getTag(post)  # Get the tag data for the post
        MFlist = MF.getMF(tagdata)  # List of multiplying factors

        for word in post.split(' '):
            mult = 1  # Default multiplier
            typ = None

            # Get multiplier for the word
            for mf in MFlist:
                if mf[0] == word:
                    mult = mf[1]
                    typ = mf[2]
                    break  # Break after finding the multiplier

            # If word exists in HSWN
            if HSWN.searchHSWN(word) != 'NF':
                wordPol = HSWN.searchHSWN(word)

                # Handle multiplier
                wordPol *= mult
                totalPol += wordPol

            # If word not in HSWN
            elif typ in ['NN', 'VB', 'JJ', 'RB']:
                inEn = translate.translate(word)  # Translate word to English
                pol = moduleeng.polarity(inEn, typ)  # Get polarity using English module
                if pol != 'NF':
                    totalPol += pol

        # Write the result to the output file
        writeDoc.write(f"{sno},{1 if totalPol > 0.1 else -1 if totalPol < -0.1 else 0}\n")
        sno += 1