from .new_final_json import get_all_answer 
from .score import calculate_section_score ,calculate_points
import json
import logging

logging.basicConfig(filename='scraper_logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def json_format(asin):
    try:
        result = get_all_answer(asin)
        title_char_output , title_cap_output , title_each_word_output , junk_title_output ,contains_non_lowercase_articles_output,title_contains_brand_output,taxonomy_output, bullet_count_output ,\
        check_influential_content,check_promotional_content,bullets_char_count_output, bullets_capital,no_ending_punctuation_output,non_capitalized_articles_output,check_influential_content_bullet,check_promotional_content_bullet, \
        contains_link_bullet,des_char_count_output , des_cap_check_output ,description_char_cap,html_in_des_output, \
        non_capitalized_articles_des,check_influential_content_des,check_promotional_content_des,check_readability_score,contains_link_des,image_count_output , image_bg_output,\
        high_resolution_image_output,video_count_output, datadf, media_data, df,images , video = result

        Meets_the_Recommended_Character_Limit = title_char_output == "Meets the Recommended Character Limit"
        All_the_Characters_are_not_Capital = title_cap_output == "All the Characters are not Capital"
        First_Letter_Capitalized_of_each_word = title_each_word_output == "The first letter of each word is capitalized"
        Free_from_Symbols_Emojis_and_Junk_Characters = junk_title_output == "Free from Symbols, Emojis and Junk Characters"
        Non_capitalized_articles_or_prepositions = contains_non_lowercase_articles_output == "False"
        Title_initiates_with_the_Brand_of_the_product = title_contains_brand_output =="True"
        No_usage_of_influential_content = check_influential_content == "True"
        No_promotional_content = check_promotional_content == "True"
        Product_Categorized_Correctly_Within_Taxonomy = taxonomy_output == "The product title matches the following taxonomy categories"
        No_of_bullet_points_in_comparison_to_the_category = bullet_count_output == "No of bullet points in comparison to the category"
        Each_Bullet_Meets_the_Recommended_Character_Limit = bullets_char_count_output == "All bullet points have a character count between 50 to 150"
        All_the_bullets_Characters_are_not_Capital = bullets_capital == "All the Characters are not Capital"
        No_usage_of_ending_punctuations = no_ending_punctuation_output == "True"
        non_capitalized_articles_for_bullet = non_capitalized_articles_output == "True"
        No_usage_of_influential_content_bullet = check_influential_content_bullet == "True"
        No_promotional_content_bullet= check_promotional_content_bullet == "True"
        No_usage_of_web_app_links_bullet = contains_link_bullet == "True"
        Description_Meets_the_Recommended_Character_Limit = des_char_count_output == "Description Meets the Recommended Character Limit"
        First_Letter_Capitalized_of_each_sentence = des_cap_check_output == "First Letter Capitalized of each sentence" 
        No_usage_of_HTML_code = html_in_des_output == "True"
        All_the_Characters_are_not_Capital_des = description_char_cap == "True"
        non_capitalized_articles_for_des = non_capitalized_articles_des == "True"
        No_usage_of_influential_content_des = check_influential_content_des == "True"
        No_promotional_content_des = check_promotional_content_des == "True"
        well_structured_des = check_readability_score == "True"
        No_usage_of_web_app_links_des = contains_link_des == "True"
        No_of_Images= image_count_output == "Three images found"
        White_background_used_for_main_and_all_other_images  = image_bg_output == "Background is white or nearly white"
        Usege_of_High_resolution_images = high_resolution_image_output == "True"
        No_of_Videos= video_count_output == "One Video included"


        section_scores = calculate_section_score(title_char_output, title_cap_output, title_each_word_output, junk_title_output,
                                                contains_non_lowercase_articles_output,title_contains_brand_output,check_influential_content,check_promotional_content,
                                                taxonomy_output, bullet_count_output, bullets_char_count_output,bullets_capital,no_ending_punctuation_output,\
                                                non_capitalized_articles_output,check_influential_content_bullet,check_promotional_content_bullet,contains_link_bullet,
                                                des_char_count_output, des_cap_check_output,html_in_des_output,description_char_cap, \
                                                non_capitalized_articles_des, check_influential_content_des, check_promotional_content_des,\
                                                check_readability_score,contains_link_des,image_count_output,
                                                image_bg_output,high_resolution_image_output, video_count_output)

        bullet_count= int(df['Total Bullet'][0])
        brand_story = datadf['brand_story']

        brand_story_presence = "Present" if brand_story is not None and not brand_story.astype(str).str.strip().eq('').any() else "Missing"
        json_data = [
            {
                "section": "ASIN",
                "data":[
                    {"field": "ASIN", "status":str(asin)}
                ]
            },

            {
                "section": "Title",
                "data": [
                    {"field": "Title","status":str(datadf['title'][0])},
                    {"field": "Section_score","status":str((section_scores["Title"]))},
                    {"field": "Meets the Recommended Character Limit", "status": str(Meets_the_Recommended_Character_Limit)},
                    {"field": "All the Characters are not Capital", "status": str(All_the_Characters_are_not_Capital)},
                    {"field": "First Letter Capitalized of each word", "status": str(First_Letter_Capitalized_of_each_word)},
                    {"field": "Free from Symbols, Emojis and Junk Characters", "status": str(Free_from_Symbols_Emojis_and_Junk_Characters)},
                    {"field": "Non-capitalized articles or prepositions", "status": str(Non_capitalized_articles_or_prepositions)},
                    {"field": "Title initiates with the Brand of the product", "status": str(Title_initiates_with_the_Brand_of_the_product)},
                    {"field": "No usage of superfluous or subjectve content", "status": str(No_usage_of_influential_content)},
                    {"field": "No promotional content", "status": str(No_promotional_content)},
                    {"field": "Ranking", "status":round(calculate_points(sum([Meets_the_Recommended_Character_Limit,
                                                    All_the_Characters_are_not_Capital,
                                                    First_Letter_Capitalized_of_each_word,
                                                    Free_from_Symbols_Emojis_and_Junk_Characters,
                                                    Non_capitalized_articles_or_prepositions,
                                                    Title_initiates_with_the_Brand_of_the_product,
                                                    No_usage_of_influential_content,
                                                    No_promotional_content]), 8)-7)}
                    
                ]
            },
            {
                "section": "Taxonomy",
                "data": [
                    {"field": "Taxonomy","status":str(datadf['taxonomy'][0])},
                    {"field": "Section_score","status":str((section_scores["Taxonomy"]))},
                    {"field": "The product title matches the following taxonomy categories", "status": str(Product_Categorized_Correctly_Within_Taxonomy)},
                    {"field": "Accurate Browse Nodes Been Applied to the Product Listing", "status": str(Product_Categorized_Correctly_Within_Taxonomy)},
                    {"field": "Product's Category Aligned with its Main Features and Attributes", "status": str(Product_Categorized_Correctly_Within_Taxonomy)},
                    {"field": "The Parent-Child Relationship Well-Established", "status": str(Product_Categorized_Correctly_Within_Taxonomy)},
                    {"field": "Ranking", "status":round(calculate_points(Product_Categorized_Correctly_Within_Taxonomy, 1)-7)}

                ]
            },
            {
                "section": "Bullets",
                "data": [
                    {"field": "Bullets", "status":datadf['bullet'].tolist()},
                    {"field": "Bullets Count", "status":bullet_count},
                    {"field": "Section_score","status":str((section_scores["Bullets"]))},
                    {"field": "Number of bullet points in comparison to the category", "status": str(No_of_bullet_points_in_comparison_to_the_category)},
                    {"field": "Each Bullet Meets the Recommended Character Limit", "status": str(Each_Bullet_Meets_the_Recommended_Character_Limit)},
                    {"field": "All the Characters are not Capital", "status":str(All_the_bullets_Characters_are_not_Capital)},
                    {"field": "No usage of ending punctuations", "status":str(No_usage_of_ending_punctuations)},
                    {"field": "Non-capitalized articles or prepositions", "status":str(non_capitalized_articles_for_bullet)},
                    {"field": "No usage of superfluous or subjectve content", "status":str(No_usage_of_influential_content_bullet)},
                    {"field": "No usage of pricing and promotional content", "status":str(No_promotional_content_bullet)},
                    {"field": "No usage of web/app links", "status":str(No_usage_of_web_app_links_bullet)},
                    
                    {"field": "Ranking", "status":round(calculate_points(sum([No_of_bullet_points_in_comparison_to_the_category,
                                                    Each_Bullet_Meets_the_Recommended_Character_Limit,
                                                    All_the_bullets_Characters_are_not_Capital,
                                                    No_usage_of_ending_punctuations,
                                                    non_capitalized_articles_for_bullet,
                                                    No_usage_of_influential_content_bullet,
                                                    No_promotional_content_bullet,
                                                    No_usage_of_web_app_links_bullet]), 8)-7)}

                ]
            },

            {
                "section": "Brand story",
                "data": [
                    {"field": "Brand_Story", "status":str(brand_story_presence)}
                ]
            },

            {
                "section": "Description",
                "data": [
                    {"field": "Description", "status":str(datadf['description'][0])},
                    {"field": "Section_score","status":str((section_scores["Description"]))},
                    {"field": "Description Meets the Recommended Character Limit", "status": str(Description_Meets_the_Recommended_Character_Limit)},
                    {"field": "First Letter Capitalized of each sentence", "status": str(First_Letter_Capitalized_of_each_sentence)},
                    {"field": "No usage of HTML code", "status": str(No_usage_of_HTML_code)},
                    {"field": "All the Characters are not Capital", "status": str(All_the_Characters_are_not_Capital_des)},
                    {"field": "Non-capitalized articles or prepositions", "status": str(non_capitalized_articles_for_des)},
                    {"field": "No usage of superfluous or subjectve content", "status": str(No_usage_of_influential_content_des)},
                    {"field": "Non usage of pricing and promotional content", "status": str(No_promotional_content_des)},
                    {"field": "Easy language and well structured description", "status": str(well_structured_des)},
                    {"field": "No usage of web/app links", "status": str(No_usage_of_web_app_links_des)},
                    {"field": "Ranking", "status":round(calculate_points(sum([Description_Meets_the_Recommended_Character_Limit,
                                                    First_Letter_Capitalized_of_each_sentence,
                                                    No_usage_of_HTML_code,
                                                    All_the_Characters_are_not_Capital_des,
                                                    non_capitalized_articles_for_des,
                                                    No_usage_of_influential_content_des,
                                                    No_promotional_content_des,
                                                    well_structured_des,
                                                    No_usage_of_web_app_links_des]), 9)-7)}
                ]
            },

            {
                "section": "Image",
                "data": [
                    {"field": "Images", "status":images},
                    {"field": "Section_score","status":str((section_scores["Image"]))},
                    {"field": "Number of Images", "status": str(No_of_Images)},
                    {"field": "White / Appropriate background used for main and all other images", "status": str(White_background_used_for_main_and_all_other_images)},
                    {"field": "Usege of High-resolution images", "status": str(Usege_of_High_resolution_images)},
                    {"field": "Ranking", "status":round(calculate_points(sum([No_of_Images, White_background_used_for_main_and_all_other_images,Usege_of_High_resolution_images]), 3)-7)}
                ]
            },

            {
                "section": "Video",
                "data": [
                    {"field": "video", "status":video},
                    {"field": "Section_score","status":str((section_scores["Video"]))},
                    {"field": "Number of Videos", "status": str(No_of_Videos)},
                    {"field": "Ranking", "status":round(calculate_points(No_of_Videos, 1))}
                ]
            }
        ]

        # Calculate and add the average point values for image and video
        # image_video_average = round((calculate_points(sum([No_of_Images, White_background_used_for_main_and_all_other_images,Usege_of_High_resolution_images]), 3) + calculate_points(sum([No_of_Videos]), 1)) / 2)
        # content_average = round((calculate_points(sum([Meets_the_Recommended_Character_Limit,
        #                                             All_the_Characters_are_not_Capital,
        #                                             First_Letter_Capitalized_of_each_word,
        #                                             Free_from_Symbols_Emojis_and_Junk_Characters,
        #                                             Non_capitalized_articles_or_prepositions,
        #                                             Title_initiates_with_the_Brand_of_the_product]), 6)+ calculate_points(Product_Categorized_Correctly_Within_Taxonomy, 1) + calculate_points(sum([No_of_bullet_points_in_comparison_to_the_category,
        #                                             Each_Bullet_Meets_the_Recommended_Character_Limit,All_the_bullets_Characters_are_not_Capital]), 3) + calculate_points(sum([Description_Meets_the_Recommended_Character_Limit,
        #                                             First_Letter_Capitalized_of_each_sentence,No_usage_of_HTML_code]), 3)) / 4)
        # total_score = round((image_video_average + content_average) /2)

        image_video_average = round((calculate_points(sum([No_of_Images, White_background_used_for_main_and_all_other_images,
                                        Usege_of_High_resolution_images]), 3) - 7 + calculate_points(sum([No_of_Videos]), 1) - 7) / 2)
        content_average = round((calculate_points(sum([Meets_the_Recommended_Character_Limit,
                                                    All_the_Characters_are_not_Capital,
                                                    First_Letter_Capitalized_of_each_word,
                                                    Free_from_Symbols_Emojis_and_Junk_Characters,
                                                    Non_capitalized_articles_or_prepositions,
                                                    Title_initiates_with_the_Brand_of_the_product,
                                                    No_usage_of_influential_content,
                                                    No_promotional_content]), 8) - 7 +
                                calculate_points(Product_Categorized_Correctly_Within_Taxonomy, 1) - 7 +
                                calculate_points(sum([No_of_bullet_points_in_comparison_to_the_category,
                                                    Each_Bullet_Meets_the_Recommended_Character_Limit,
                                                    All_the_bullets_Characters_are_not_Capital,
                                                    No_usage_of_ending_punctuations,
                                                    non_capitalized_articles_for_bullet,
                                                    No_usage_of_influential_content_bullet,
                                                    No_promotional_content_bullet,
                                                    No_usage_of_web_app_links_bullet]), 8) - 7 +
                                calculate_points(sum([Description_Meets_the_Recommended_Character_Limit,
                                                    First_Letter_Capitalized_of_each_sentence,
                                                    No_usage_of_HTML_code,
                                                    All_the_Characters_are_not_Capital_des,
                                                    non_capitalized_articles_for_des,
                                                    No_usage_of_influential_content_des,
                                                    No_promotional_content_des,
                                                    well_structured_des,
                                                    No_usage_of_web_app_links_des]), 9) - 7) / 4)
        total_score = round((image_video_average + content_average) / 2)
                        
        json_data.append({
            "section": "Final_Score",
            "data": [
                {"field": "media_score", "status": str(image_video_average)},
                {"field": "content_score", "status": str(content_average)},
                {"field": "total_score", "status": str(total_score)},
            ]
        })

        converted_data = {"data": json_data}

        final_json = json.dumps(converted_data, indent=4)
    except Exception as e:
        logging.error(f"Error in generate_json: {str(e)}")
        return None
    return final_json


if __name__ == "__main__":
    asin = "B096NFX7V7"
    print(json_format(asin)) 