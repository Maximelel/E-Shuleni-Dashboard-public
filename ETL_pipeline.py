# pypdf
from pypdf import PdfReader
from PyPDF2 import PdfReader
import PyPDF2

import numpy as np
import pandas as pd
import re
from tqdm import tqdm

# Preprocess pdf: extract page numbers for each student

def extract_pages_with_keyword(pdf_reader):
    
        keyword = "'s Progress"
        
        # List to store page numbers containing the keyword
        pages_with_keyword = []
        
        # Iterate through each page
        for page_number in range(len(pdf_reader.pages)):
            # Get the text of the current page
            page_text = pdf_reader.pages[page_number].extract_text()
            
            # Check if the keyword exists in the page text
            if keyword in page_text:
                # Append the page number to the list
                pages_with_keyword.append(page_number + 1)  # Page numbers start from 1
        
        return pages_with_keyword
    
def extract_data(pdf_path, stream, verbose = True):

    # extract pages with keyword
    with open(pdf_path, "rb") as file:
        # Create a PDF reader object
        pdf_reader = PdfReader(file)
        pages_with_keyword = extract_pages_with_keyword(pdf_reader)

    # add 1 to the page number to match the page number in the pdf reader
    pages_with_keyword = pages_with_keyword + [len(pdf_reader.pages) + 1] # + 1 because index starts at 0, does not read last page otherwise

    if verbose:
        print(f"Length of the pdf: {len(pdf_reader.pages)} pages")
        print("Pages containing the keyword 'Progress Report':", pages_with_keyword)

    # Store to dataframe
    df = pd.DataFrame(columns= ['Name', 'Lesson Completed', 'Hours On Program', 'English Test Taken', 'English Test with Excellent/Good', 'Overall Percentage Score', 'Mastered Course', 'Mastered Level'])
    idx = 0

    for i,j in zip(pages_with_keyword[:-1], pages_with_keyword[1:]):
        #print(f"Page {i} to Page {j}")
        # read page i to j
        text = ""
        
        # combine all pages for the same student
        for page_num in range(i-1, j-1):
            text += pdf_reader.pages[page_num].extract_text()
        
        # check patterns
        # Extract name
        #name_pattern = r'([A-Z\s]+)\'s Progress'
        name_pattern = r"([A-Za-z\s]+)'s Progress"
        name_match = re.search(name_pattern, text)
        name = name_match.group(1).strip() if name_match else ""
        # Extract Lesson Completed
        lessons_completed_pattern = r'Completed Lessons: (\d+)'
        lessons_completed_match = re.search(lessons_completed_pattern, text)
        lessons_completed = int(lessons_completed_match.group(1)) if lessons_completed_match else 0
        # Extract Hours on Program
        hours_pattern = r'Playtime: (\d+)hour'
        hours_match = re.search(hours_pattern, text)
        hours_on_program = int(hours_match.group(1)) if hours_match else 0
        # Extract Minutes on Program
        minutes_pattern = r'(\d+)min'
        minutes_match = re.search(minutes_pattern, text)
        minutes_on_program = int(minutes_match.group(1)) if minutes_match else 0
        # Define regular expressions to extract "English Test Taken" and "Overall Percentage Score"
        english_test_pattern = r'English (\d+) (\d+) \((\d+%)\)'
        # Search for the pattern in the input string
        english_test_match = re.search(english_test_pattern, text)
        # Extract the "English Test Taken" and "Overall Percentage Score" if match is found
        english_test_taken = english_test_match.group(1) if english_test_match else None
        english_test_excellent = english_test_match.group(2) if english_test_match else None
        overall_percentage_score = english_test_match.group(3)[:-1] if english_test_match else None
        
        # Define regular expressions to extract "Mastered Course" and "Mastered Level"
        course_pattern = r'mastered Course (\d+)'
        level_pattern = r'Level (\d+)[~-](\d+)'
        # Search for the patterns in the input string
        course_match = re.search(course_pattern, text)
        level_match = re.search(level_pattern, text)
        # Extract the "Mastered Course" and "Mastered Level" if matches are found
        mastered_course = course_match.group(1) if course_match else None
        mastered_level = f"{level_match.group(1)}-{level_match.group(2)}" if level_match else None

        
        # Prepare the extracted data in a dictionary
        extracted_data = {
            "Name": name,
            "Lesson Completed": lessons_completed,
            "Hours On Program": hours_on_program + minutes_on_program/60,
            "English Test Taken": english_test_taken,
            "English Test with Excellent/Good": english_test_excellent,
            "Overall Percentage Score": overall_percentage_score,
            "Mastered Course": mastered_course,
            "Mastered Level": mastered_level
        }
        #print(extracted_data)

        for key, value in extracted_data.items():
            df.loc[idx, key] = value

        idx += 1 # increment index to fill df
    
    # Add stream to the dataframe
    df['Class'] = stream
    
    return df

