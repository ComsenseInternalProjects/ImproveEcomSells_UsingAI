import pandas as pd
from .output import fill_data_dict
from .app import calculate_bullet_counts , spell_check_data , junk_title

def data2df(data):
    try:
        # Create a DataFrame for the 'bullets' field
        bullets = data.get('bullets', [])
        bullet_dict = {}
        for bullet in bullets:
            bullet_parts = bullet.split('~ ')
            bullet_number = bullet_parts[0].split()[1]  # Extract the bullet number
            bullet_text = bullet_parts[1]
            bullet_dict[bullet_number] = bullet_text

        df_bullets = pd.DataFrame.from_dict(bullet_dict, orient='index', columns=['bullet'])
        df_bullets = df_bullets.reset_index().rename(columns={'index': 'bullet_number'})
        
    except Exception as e:
        print(f"Error extracting bullets: {e}")
        df_bullets = pd.DataFrame(columns=['bullet', 'bullet_number'])

    # Create DataFrames for the other fields with error handling
    def create_dataframe(field_name):
        try:
            value = data[field_name]
            df = pd.DataFrame([value], columns=[field_name])
        except KeyError:
            df = pd.DataFrame(columns=[field_name])
        return df

    df_title = create_dataframe('title')
    df_taxonomy = create_dataframe('taxonomy')
    df_price = create_dataframe('price')
    df_ratings = create_dataframe('ratings')
    df_reviews = create_dataframe('reviews')
    df_reviews_count = create_dataframe('review_count')
    df_seller = create_dataframe('seller')
    df_description = create_dataframe('description')
    df_brand_story = create_dataframe('brand_story')
    df_brand = create_dataframe('brand')
    df_legal_disclaimer = create_dataframe('legal_disclaimer')
    df_Product_details = create_dataframe('Product_details')

    # Create DataFrames for images with error handling
    try:
        images = data.get('images', [])
        image_dict = {}
        for i, image_url in enumerate(images, start=1):
            image_dict[f'image{i}'] = [image_url]

        df_images = pd.DataFrame.from_dict(image_dict, orient='index', columns=['image'])
        df_images = df_images.reset_index().rename(columns={'index': 'image_number'})
    except Exception as e:
        print(f"Error extracting images: {e}")
        df_images = pd.DataFrame(columns=['image', 'image_number'])

    # Create DataFrame for video with error handling
    try:
        video = data.get('video', [])
        if isinstance(video, list) and video:
            video = video[0]  # Assuming a list of video URLs, take the first one
        df_video = pd.DataFrame([video], columns=['video'])
    except Exception as e:
        print(f"Error extracting video URL: {e}")
        df_video = pd.DataFrame(columns=['video'])

    # Concatenate all the DataFrames horizontally
    data_frames = [df_title, df_taxonomy, df_price, df_ratings, df_reviews,df_reviews_count, df_seller, df_description, df_brand_story,df_video, df_brand, df_bullets, df_images, df_Product_details, df_legal_disclaimer]
    df_final = pd.concat(data_frames, axis=1)

    # Reset the index for the final DataFrame
    df_final.reset_index(drop=True, inplace=True)

    media_urls = []

    # Iterate through the columns of df_final to find media URLs
    for column_name in df_final.columns:
        if 'image' in column_name or column_name == 'video':
            media_urls.extend(df_final[column_name].dropna().tolist())

    # Print the resulting DataFrame
    return df_final, media_urls

def data_values(url):
    try:
        data = fill_data_dict(url)
    except Exception as fill_data_error:
        print(f"Error in fill_data_dict: {fill_data_error}")
        return None, None, None  # Return None values if there's an error

    try:
        alldatadf = data2df(data)
    except Exception as data2df_error:
        print(f"Error in data2df: {data2df_error}")
        return None, None, None  # Return None values if there's an error
    try:
        datadf, media_data = alldatadf
    except Exception as datadf_error:
        print(f"Error extracting datadf and media_data: {datadf_error}")
        return None, None, None  # Return None values if there's an error

    try:
        results = calculate_bullet_counts(data)
    except Exception as calculate_error:
        print(f"Error in calculate_bullet_counts: {calculate_error}")
        return datadf, media_data, None  # Return None for results

    try:
        spell_check_results = spell_check_data(data)
    except Exception as spell_check_error:
        print(f"Error in spell_check_data: {spell_check_error}")
        return datadf, media_data, None  # Return None for spell_check_results

    # Create a list of dictionaries for bullet details
    bullet_details = []

    def check_title_text_quality(title_text):
        issues = junk_title(title_text)
        return 'Issue found' if issues else 'No issue found'

    # Check text quality for the 'title'
    title_text_quality = check_title_text_quality(data['title'])
    num_bullets = len(results) - 2
    # Add title details to the bullet details
    bullet_details.append({
        'Bullet': 'title',
        'Word count': results['title']['word_count'],
        'Character count': results['title']['char_count'],
        'Spell Check Result': spell_check_results.get('title', 'correct'),
        'Text Quality': title_text_quality,  # Add the text quality result for the title
        'Total Bullet': num_bullets
    })

    # Iterate through the remaining bullets
    for bullet, counts in results.items():
        if bullet != 'title':
            bullet_number = bullet.replace("bullet", "").strip()  # Extract the bullet number
            bullet_details.append({
                'Bullet': f'bullet{bullet_number}',
                'Word count': counts['word_count'],
                'Character count': counts['char_count'],
                'Spell Check Result': spell_check_results.get(bullet, 'correct'),
                'Text Quality': None  # Add None for other bullets
            })

    try:
        # Create a DataFrame from the list of bullet details
        final_df = pd.DataFrame(bullet_details)

        # Add title and description to the DataFrame
        final_df['Total Bullet'] = num_bullets
        final_df['Title_Word count'] = results['title']['word_count']
        final_df['Title_Character count'] = results['title']['char_count']
        final_df['Title_Spell Check Result'] = spell_check_results.get('title', 'correct')
        final_df['Description_Word count'] = results['description']['word_count']
        final_df['Description_Character count'] = results['description']['char_count']
        final_df['Description_Spell Check Result'] = spell_check_results.get('description', 'correct')
    except Exception as final_df_error:
        print(f"Error creating final DataFrame: {final_df_error}")
        return datadf, media_data, None
    df = final_df.iloc[:, :6]
    df['Bullet'] = df['Bullet'].replace({'bullettitle': 'title', 'bulletdescription': 'description'})

    return datadf, media_data, df


if __name__ == "__main__":
    output = data_values("https://www.amazon.com/Hanes-Full-zip-Eco-smart-athletic-sweatshirts/dp/B00JUM4CT4/?_encoding=UTF8&pd_rd_w=6xKyM&content-id=amzn1.sym.64be5821-f651-4b0b-8dd3-4f9b884f10e5&pf_rd_p=64be5821-f651-4b0b-8dd3-4f9b884f10e5&pf_rd_r=R569TVEY39DHCH46AW6B&pd_rd_wg=8e6Z8&pd_rd_r=fa67eb38-52fd-4829-8329-d3f13dcd4e72&ref_=pd_gw_crs_zg_bs_7141123011&th=1")
    datadf , df = output
    datadf_output = datadf
    value_output = df
    print(datadf_output)
    print(value_output)