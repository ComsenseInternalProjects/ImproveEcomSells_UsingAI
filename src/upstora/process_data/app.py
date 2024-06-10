import logging
from spellchecker import SpellChecker
from textblob import TextBlob
import re

# Configure logging to print messages to console
logging.basicConfig(filename='scraper_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_bullet_counts(data):
    try:
        bullets = data['bullets']
        title = data['title']
        description = data['description']
        results = {}

        for i, bullet in enumerate(bullets, start=1):
            bullet_text = bullet.split('~ ')[1]
            words = bullet_text.split()
            word_count = len(words)
            char_count = len(bullet_text)
            bullet_key = f'bullet{i}'
            results[bullet_key] = {'word_count': word_count, 'char_count': char_count}

        title_words = title.split()
        title_word_count = len(title_words)
        title_char_count = len(title)

        # Calculate the word count and character count
        description_words = description.split()
        description_word_count = len(description_words)
        description_char_count = len(description)

        results['title'] = {'word_count': title_word_count, 'char_count': title_char_count}
        results['description'] = {'word_count': description_word_count, 'char_count': description_char_count}
        return results
    except Exception as e:
        logging.error(f"Error in calculate_bullet_counts: {e}")
        return None

def spell_check_data(data):
    try:
        def spell_check_text(text):
            blob = TextBlob(text)
            corrected_words = blob.correct()
            misspelled_words = [word for word in corrected_words.words if word != word.correct()]

            return misspelled_words
        spell_check_results = {}

        for bullet in data.get('bullets', []):
            parts = bullet.split(':', 1)
            
            if len(parts) == 2:
                bullet_number, bullet_text = parts
                misspelled_words = spell_check_text(bullet_text.strip())
                if misspelled_words:
                    spell_check_results[bullet_number.strip()] = f'spell_check wrong: {", ".join(misspelled_words)}'
                else:
                    spell_check_results[bullet_number.strip()] = 'correct'


        title_misspelled = spell_check_text(data.get('title', ''))
        description_misspelled = spell_check_text(data.get('description', ''))

        if title_misspelled:
            spell_check_results['title'] = f'spell_check wrong: {", ".join(title_misspelled)}'
        else:
            spell_check_results['title'] = 'correct'

        if description_misspelled:
            spell_check_results['description'] = f'spell_check wrong: {", ".join(description_misspelled)}'
        else:
            spell_check_results['description'] = 'correct'

        return spell_check_results
    except Exception as e:
        logging.error(f"Error in spell_check_data: {e}")
        return None

def junk_title(text):
    try:
        # Check for non-standard or irrelevant characters like (!!!) and ($$$)
        non_standard_chars = re.search(r'[!$]+', text)
        
        # Check for extra spaces, tabs, or line breaks
        has_extra_whitespace = re.search(r'\s{2,}', text)
        
        # Check for emojis
        has_emojis = bool(re.search(r'[^\x00-\x7F]+', text))
        
        issues = []
        
        if non_standard_chars:
            issues.append("Non-standard or irrelevant characters like (!!!) or ($$$) found")
        
        if has_extra_whitespace:
            issues.append("Extra spaces, tabs, or line breaks found")
        
        if has_emojis:
            issues.append("Emojis found")
        
        return issues
    except Exception as e:
        logging.error(f"Error in junk_title: {e}")
        return None

if __name__ == "__main__":
    url = "http://www.amazon.com/exec/obidos/ASIN/{insert ASIN here}"
