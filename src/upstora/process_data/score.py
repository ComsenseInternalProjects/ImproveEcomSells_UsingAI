def calculate_points(true_count, total_fields):
    if total_fields == 0:
        return 0
    return (true_count / total_fields) * 100

def calculate_section_score(title_char_output, title_cap_output, title_each_word_output, junk_title_output,contains_non_lowercase_articles_output,title_contains_brand_output,check_influential_content,\
                            check_promotional_content,taxonomy_output,bullet_count_output, bullets_char_count_output,bullets_capital, no_ending_punctuation_output,\
                            non_capitalized_articles_output,check_influential_content_bullet,check_promotional_content_bullet,contains_link_bullet, des_char_count_output, des_cap_check_output,description_char_cap,html_in_des_output,
                            non_capitalized_articles_des,check_influential_content_des,check_promotional_content_des,check_readability_score,contains_link_des,image_count_output, image_bg_output,high_resolution_image_output, video_count_output):
    section_scores = {
        "Title": 0,
        "Taxonomy": 0,
        "Bullets": 0,
        "Description": 0,
        "Image": 0,
        "Video": 0
    }
    
    title_true_count = sum([title_char_output == "Meets the Recommended Character Limit",
                            title_cap_output == "All the Characters are not Capital",
                            title_each_word_output == "Not all the first letters of words are capitalized",
                            junk_title_output == "Free from Symbols, Emojis and Junk Characters",
                            contains_non_lowercase_articles_output == True,
                            title_contains_brand_output == True,
                            check_influential_content == True,
                            check_promotional_content == True])
    
    if 4 <= title_true_count <= 6:
        section_scores["Title"] = "Satisfactory"
    elif title_true_count < 4:
        section_scores["Title"] = "Needs Improvement"
    else:
        section_scores["Title"] = "Outstanding"

    
    if taxonomy_output == "The product title matches the following taxonomy categories":
        section_scores["Taxonomy"] = "Outstanding"
    else:
        section_scores["Taxonomy"] = "Needs Improvement"
    
    bullets_true_count = sum([bullet_count_output == "No of bullet points in comparison to the category",
                            bullets_char_count_output == "All bullet points have a character count between 50 to 150",
                            bullets_capital == "All the Characters are not Capital",
                            no_ending_punctuation_output == True,
                            non_capitalized_articles_output == True,
                            check_influential_content_bullet == True,
                            check_promotional_content_bullet == True,
                            contains_link_bullet == True])
    
    if 5 <= bullets_true_count <= 7:
        section_scores["Bullets"] = "Satisfactory"
    elif bullets_true_count < 5:
        section_scores["Bullets"] = "Needs Improvement"
    else:
        section_scores["Bullets"] = "Outstanding"
    
    # if bullets_true_count == 3:
    #     section_scores["Bullets"] = "Outstanding"
    # elif 1 <= bullets_true_count <= 2:
    #     section_scores["Bullets"] = "Satisfactory"
    # else:
    #     section_scores["Bullets"] = "Needs Improvement"

    
    description_true_count = sum([des_char_count_output == "Description Meets the Recommended Character Limit",
                            des_cap_check_output == "First Letter Capitalized of each sentence",
                            html_in_des_output == True,
                            description_char_cap == True,
                            non_capitalized_articles_des == True,
                            check_influential_content_des == True,
                            check_promotional_content_des == True,
                            check_readability_score == True,
                            contains_link_des == True,
                            ])
    
    if 5 <= description_true_count <= 7:
        section_scores["Description"] = "Satisfactory"
    elif description_true_count < 5:
        section_scores["Description"] = "Needs Improvement"
    else:
        section_scores["Description"] = "Outstanding"

    # if description_true_count == 3:
    #     section_scores["Description"] = "Outstanding"
    # elif 1 <= description_true_count <= 2:
    #     section_scores["Description"] = "Satisfactory"
    # else:
    #     section_scores["Description"] = "Needs Improvement"
    
    image_true_count = sum([image_count_output == "Three images found",
                            image_bg_output == "Background is white or nearly white",
                            high_resolution_image_output == True])
    
    if image_true_count == 3:
        section_scores["Image"] = "Outstanding"
    elif 1 <= image_true_count <= 2:
        section_scores["Image"] = "Satisfactory"
    else:
        section_scores["Image"] = "Needs Improvement"

    video_true_count = sum([video_count_output == "One Video included"])
    if video_true_count >= 1:
        section_scores["Video"] = "Outstanding"
    else:
        section_scores["Video"] = "Needs Improvement"

    return section_scores