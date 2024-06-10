from .convert2df import data_values
from .background import image_insight
from .parameters import contains_non_lowercase_articles , title_contains_brand , bullet_capital , html_in_des,high_resolution_image,\
                       verify_influential_content, verify_promotional_content,no_ending_punctuation,non_capitalized_articles,\
                       contains_link , readability_score
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import re

def process_input(input_value):
    asin = input_value
    try:
        output = data_values(f"http://www.amazon.com/exec/obidos/ASIN/{asin}")
        return output
    except Exception as e:
       return None
    
def classify_media_urls(media_urls):
    images = []
    videos = []
    for url in media_urls:
        if url.endswith('.jpg'):
            images.append(url)
        elif url.endswith('.mp4'):
            videos.append(url)
    return images, videos

################################ Title Section ####################################
def title_char(df):
    title_length = df[df['Bullet'] == 'title']['Character count'].values[0]
    if 140 <= title_length <= 200:
        title_char_output = "Meets the Recommended Character Limit"
    else:
        title_char_output = "Doesn't Meet the Recommended Character Limit"
    return title_char_output


def title_cap(input_str):
    input_str = str(input_str)
    output = input_str.isupper()
    if output == True:
        title_cap_output = "All the Characters are Capital"
    else:
        title_cap_output = "All the Characters are not Capital"
    return title_cap_output
    
# def title_each_word(title):
#     if title.istitle():
#         title_each_word_check = "The first letter of each word is capitalized"
#     else:
#         title_each_word_check = "Not all the first letters of words are capitalized"
#     return title_each_word_check

def title_each_word(title):
    articles = ["a", "an", "the", "by", "and", "but", "of", "for", "from", "in", "into", "out", "at", "down", "up", "like", "no", "nor", "so", "yet"]
    words = title.split()
    for word in words:
        if word.lower() not in articles and not word.isdigit() and not word.istitle():
            return "Not all the first letters of words are capitalized"
    return "The first letter of each word is capitalized"

def junk_title(text):
    non_standard_chars = re.search(r'[!$]+', text)
    
    has_emojis = bool(re.search(r'[^\x00-\x7F]+', text))
    
    issues = []
    
    if non_standard_chars:
        issues.append("Non-standard or irrelevant characters like (!!!) or ($$$) found")
    
    if has_emojis:
        issues.append("Emojis found")
    if issues:
        title_emoji_check = "Contains symbols, Emojis and Junk Characters"
    else:
        title_emoji_check = "Free from Symbols, Emojis and Junk Characters"
    
    return title_emoji_check

##################### Taxonomy #######################################
def check_taxonomy(title, taxonomy):
    matches = [""]
    for category in taxonomy:
        if re.search(r'\b' + re.escape(category) + r'\b', title, re.I):
            matches.append(category)

    if matches:
        taxonomy_output = "The product title matches the following taxonomy categories"
        # for match in matches:
        #     print(match)
    else:
        taxonomy_output = "The product title does not match any taxonomy categories"
    return taxonomy_output

################# Bullet ###########################


def bullet_count(df):
    #url = f"http://www.amazon.com/exec/obidos/ASIN/{input_value}"
    # output = process_input(input_value)
    # datadf,media_data,df = output
    total_bullet = df.loc[0, 'Total Bullet']
    if total_bullet > 5:
        bulletcount = "No of bullet points in comparison to the category"
    else:
        bulletcount = "Less bullet points in comparison to the category"
    return bulletcount

def bullets_char_count(df):
    df['Character Count Check'] = df['Bullet'].apply(lambda x: 50 <= len(x) <= 150)
    all_bullets_pass = df['Character Count Check'].all()
    if all_bullets_pass:
        bullets_char_output = "All bullet points have a character count between 50 to 150"
    else:
        bullets_char_output = "Some bullet points doesn't meet the criteria"

    return bullets_char_output

##################### Description #######################

def des_char_count(df):
    des_char = df[df['Bullet'] == 'description']['Character count'].values[0]
    if 840 <= des_char <= 1100: 
        des_char_output = "Description Meets the Recommended Character Limit"
    else:
        des_char_output = "Description Doesn't Meet the Recommended Character Limit"
    return des_char_output

def des_cap_check(description):
    # description = data_df['description'] 
    def starts_with_capital(sentence):
        return str(sentence[0]).isupper()
    
    sentences = sent_tokenize(description)
    all_start_with_capital = all(starts_with_capital(sentence) for sentence in sentences)
    if all_start_with_capital:
        deschar_check_output = "First Letter Capitalized of each sentence"
    else:
        deschar_check_output = "First Letter not capitalized of each sentence"
    return deschar_check_output


#################### Image ####################################

def image_count(images):
    #images, video = classify_media_urls(media_data)
    if images:
        three_images = len(images)
        if three_images == 3:
            image_count = "Three images found"
        else:
            image_count = "Less than three images found"
        return image_count
    else:
        image_count = 0
        return image_count


def image_bg(images):
    #images, video = classify_media_urls(media_data)
    bg_px = image_insight(images[0])
    background = bg_px['background'].iloc[0]
    return background

######################## Video ######################

def videos(video):
    #images, video = classify_media_urls(media_data)
    if video:
        one_video = "One Video included"
    else:
        one_video = "Video not included"
    return one_video


def get_all_answer(input_value):
    output = process_input(input_value)
    datadf,media_data,df = output
    #title operations
    title_data = datadf['title'][0]
    title = [title_data]
    # print(title)
    title_char_output = title_char(df)
    title_cap_output = title_cap(title[0])
    title_cap_output = str(title_cap_output)
    title_each_word_output = title_each_word(title[0])
    junk_title_output = junk_title(title[0])
    contains_non_lowercase_articles_output = contains_non_lowercase_articles(title[0])
    title_contains_brand_output = title_contains_brand(datadf['brand'][0],datadf['title'][0])
    check_influential_content = verify_influential_content(title)
    check_promotional_content = verify_promotional_content(title)
    #taxonomy operation
    taxonomy = datadf['taxonomy'][0]
    # print(taxonomy)
    taxonomy_output = check_taxonomy(title[0], taxonomy)
    #bullets operations
    bullet = datadf['bullet'].tolist()
    # print(bullet)
    bullet_count_output = bullet_count(df)
    bullets_char_count_output = bullets_char_count(df)
    total_bullet = df.loc[0, 'Total Bullet']
    bullets_capital = bullet_capital(bullet)
    no_ending_punctuation_output = no_ending_punctuation(bullet)
    non_capitalized_articles_output = non_capitalized_articles(bullet)
    check_influential_content_bullet = verify_influential_content(bullet)
    check_promotional_content_bullet = verify_promotional_content(bullet)
    contains_link_bullet = contains_link(bullet)
    #description operations 
    des_char_count_output = des_char_count(df)
    description_data= datadf['description'][0]
    description = [description_data]
    # print(description)
    des_cap_check_output = str(des_cap_check(description[0]))
    html_in_des_output = html_in_des(description[0])
    description_char_cap = title_cap(description[0])
    non_capitalized_articles_des = non_capitalized_articles(description)
    check_influential_content_des = verify_influential_content(description)
    check_promotional_content_des = verify_promotional_content(description)
    check_promotional_content_des = verify_promotional_content(description)
    check_readability_score = readability_score(description[0])
    contains_link_des = contains_link(description)
    #image operations
    images, video = classify_media_urls(media_data)
    image_count_output = image_count(images)
    image_bg_output = image_bg(images)
    high_resolution_image_output = high_resolution_image(images)
    #Video operations
    video_count_output = videos(video)

    return title_char_output , title_cap_output , title_each_word_output , junk_title_output,contains_non_lowercase_articles_output,title_contains_brand_output,taxonomy_output, bullet_count_output ,\
    check_influential_content,check_promotional_content,bullets_char_count_output,bullets_capital,no_ending_punctuation_output,non_capitalized_articles_output,check_influential_content_bullet,\
    check_promotional_content_bullet,contains_link_bullet, des_char_count_output , des_cap_check_output,html_in_des_output,description_char_cap, \
    non_capitalized_articles_des,check_influential_content_des,check_promotional_content_des,image_count_output , image_bg_output,\
    check_readability_score,contains_link_des,high_resolution_image_output,video_count_output, datadf, media_data, df , images , video

if __name__ == "__main__":
    asin = "B0057UUGRU"
    print(get_all_answer(asin))