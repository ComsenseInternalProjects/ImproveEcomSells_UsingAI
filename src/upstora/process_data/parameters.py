import pandas as pd
import re
import string
import requests
import io
from PIL import Image
from moviepy.editor import VideoFileClip
from fuzzywuzzy import fuzz
from bs4 import BeautifulSoup

# Check Artical lower case
def contains_non_lowercase_articles(string):
    lowercase_articles = {"a", "an", "the", "by", "and", "but", "of", "for", "from", "in", "into", "out", "at", "down", "up", "like", "no", "nor", "so", "yet"}
    words = string.split()
    for word in words:
        if word.lower() in lowercase_articles and word != word.lower():
            return "True"
    return "False"


# Check title contain brand name

def title_contains_brand(brand, title):
    return str(brand in title).capitalize()

# Check ending punctuation
def no_ending_punctuation(input_string):
    for bullet in input_string:
        punctuation_chars = set(string.punctuation)
        cleaned_string = bullet.strip()
        if cleaned_string and cleaned_string[-1] in punctuation_chars:
            return "False"
        else:
            return "True"
    
def bullet_capital(bullets):
    for bullet in bullets:
        if not str(bullet).isupper():
            return "All the Characters are not Capital"
    return "All the Characters are Capital"

def non_capitalized_articles(string):
    for bullet in string:
        lowercase_articles = {"a", "an", "the", "by", "and", "but", "of", "for", "from", "in", "into", "out", "at", "down", "up", "like", "no", "nor", "so", "yet"}
        words = bullet.split()
        for word in words:
            if word.lower() in lowercase_articles and word != word.lower():
                return "False"  
        return "True"

def verify_influential_content(sentence):
    for x in sentence:
        influential_keywords = [
            "powerful", "impactful", "inspiring", "influential",
            "compelling", "persuasive", "captivating", "motivational",
            "dynamic", "charismatic", "convincing", "eloquent",
            "insightful", "thought-provoking", "impressive", "compelling",
            "riveting", "remarkable", "inspirational", "awe-inspiring",
            "empathy", "reliable", "understanding", "patient",
            "dedicated", "attentive", "resolved", "supportive",
            "committed", "courteous", "genuine", "trustworthy",
            "professional", "efficient", "knowledgeable", "friendly",
            "sincere", "considerate", "accommodating", "dependable",
            "solution-oriented", "personalized", "thorough", "insightful",
            "skilled", "expert", "guided", "valued", "focused",
            "comprehensible", "consistent", "fair", "honest",
            "adaptable", "collaborative", "engaged", "precise",
            "receptive", "encouraging", "warm", "gracious",
            "appreciative", "prompt", "assurance", "connected",
            "proactive", "respectful", "sympathetic", "responsive",
            "reassuring", "caring", "timely", "passionate",
            "active", "accountable", "clear", "positive",
            "seamless", "prioritized", "friendly"
        ]
        
        # Set a threshold for fuzzy matching
        threshold = 90  # Adjust as needed
        
        # Check if any influential keyword closely matches the sentence
        for keyword in influential_keywords:
            similarity = fuzz.partial_ratio(keyword, x.lower())
            if similarity >= threshold:
                return "False"
        
        return "True"

def verify_promotional_content(sentence):
    for x in sentence:
        promotional_keywords = [
            "exclusive", "limited time", "special offer", "discount",
            "promotion", "sale", "save", "bonus", "free", "now",
            "new", "launch", "deal", "offer", "don't miss",
            "amazing", "unbelievable", "best", "ultimate", "extra",
            "get yours", "buy now", "limited supply", "act fast",
            "exclusive offer", "promo code", "clearance", "last chance",
            "extra savings", "instant", "double", "super sale",
            "premium", "flash sale", "lowest price", "while supplies last",
            "special price", "upgrade", "bogo", "buy one get one",
            "remarkable", "fantastic", "incredible", "remarkable",
            "remarkable offer", "grand opening", "celebration", "new arrival",
            "save big", "revolutionary", "revolutionize", "first",
            "unveiling", "introducing", "extraordinary", "spectacular",
            "exciting", "remarkable savings", "revolutionary product",
            "revolutionary solution", "exclusive access", "grand opening sale",
            "spectacular deal", "extraordinary offer", "celebratory savings",
            "spectacular savings", "groundbreaking", "celebration sale",
            "unveiling special", "first look", "extraordinary savings"
        ]
        
        # Set a threshold for fuzzy matching
        threshold = 90  # Adjust as needed
        
        # Check if any promotional keyword closely matches the sentence
        for keyword in promotional_keywords:
            similarity = fuzz.partial_ratio(keyword, x.lower())
            if similarity >= threshold:
                return "False"
        return "True"


def contains_link(input_string):
    for x in input_string:
        # Define a regular expression pattern for matching URLs
        url_pattern = re.compile(r'https?://\S+|www\.\S+')

        # Use findall to find all occurrences of the pattern in the input string
        links = re.findall(url_pattern, x)

        # Check if any links were found
        if links:
            return "False"
        else:
            return "True"


# Check descirption not contain html code
def html_in_des_old(input_string):
    code_patterns = [
        r'\bimport\b',
        r'\bclass\b',
        r'\bdef\b',
        r'\bfunction\b',
        r'\bpublic static void main\b',
        r'\bwhile\b',
        r'\bfor\b',
        r'\bif\b',
        r'\belse\b',
        r'\btry\b',
        r'\bcatch\b',
        r'\bint\b',
        r'\breturn\b',
        r'\bprint\b',
        r'\bSystem\.out\.println\b'
    ]

    for pattern in code_patterns:
        if re.search(pattern, input_string, re.IGNORECASE):
            return "False"

    return "True"

def html_in_des(input_string):
    soup = BeautifulSoup(input_string, 'html.parser')
    html_tags = soup.find_all()
    return len(html_tags) > 0

def count_syllables(word):
    # Simple syllable count based on vowels in a word
    vowels = "aeiouy"
    word = word.lower()
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith('e'):
        count -= 1
    if count == 0:
        count = 1
    return count

def readability_score(text):
    sentences = re.split(r'[.!?]+', text)
    word_count = len(re.findall(r'\w+', text))
    syllable_count = sum(count_syllables(word) for word in re.findall(r'\w+', text))

    # Calculating average words per sentence and average syllables per word
    words_per_sentence = word_count / len(sentences)
    syllables_per_word = syllable_count / word_count

    # Custom readability formula
    score = 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word
    if score > 50:
        return "True"
    else:
        return "False"


# Check High resolution image
def high_resolution_image(image_urls):
    try:
        for image_url in image_urls:
            response = requests.get(image_url)
            response.raise_for_status()

            img = Image.open(io.BytesIO(response.content))

            width, height = img.size

            if width < 1280 or height < 720:
                return "True"

        return "False"
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return "False"

# Check Image fit in frame
def image_fits_frame(image_url, frame_width, frame_height, threshold_percentage):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        img = Image.open(io.BytesIO(response.content))

        img_width, img_height = img.size

        width_fit_percentage = (img_width / frame_width) * 100
        height_fit_percentage = (img_height / frame_height) * 100

        if width_fit_percentage >= threshold_percentage and height_fit_percentage >= threshold_percentage:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False



# Check Video lenght
def is_video_duration_in_range(video_url, min_duration, max_duration):
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()

        temp_filename = 'temp_video.mp4'
        with open(temp_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        video = VideoFileClip(temp_filename)
        video_duration = video.duration

        if min_duration <= video_duration <= max_duration:
            return True
        else:
            return False
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False