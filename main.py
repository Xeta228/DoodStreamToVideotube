import requests
import re
from datetime import datetime, timezone
import configparser

config = configparser.ConfigParser()  # создаём объекта парсера
config.read("settings.ini")  # читаем конфиг

API_KEY = config["API_SETTINGS"]["api_key"]  # обращаемся как к обычному словарю!

site_title = config["WP_SETTINGS"]["site_title"]
site_link = config["WP_SETTINGS"]["site_link"]
site_description = config["WP_SETTINGS"]["site_description"]
author_id = config["WP_SETTINGS"]["author_id"]
author_login = config["WP_SETTINGS"]["author_login"]
author_email = config["WP_SETTINGS"]["author_email"]


def format_string_for_video_link(input_string):
    # Replace consecutive spaces with a single hyphen and convert to lowercase
    formatted_string = re.sub(r'(?<=\S)\s+(?=\S)', '-', input_string.lower())

    # Replace '&' with '-'
    formatted_string = formatted_string.replace('&', '-')

    return formatted_string


def form_item(num, response):
    # Extract the first title
    num -= 1
    video_name = response.json()["result"]["files"][num]["title"]
    video_link_on_site = format_string_for_video_link(response.json()["result"]["files"][num]["title"])

    current_datetime = datetime.utcnow()
    formatted_date = current_datetime.strftime("%a, %d %b %Y %H:%M:%S +0000")

    video_iframe = "<iframe width=\"600\" height=\"480\" src=\"https://d0o0d.com/e/" + \
                   response.json()["result"]["files"][num]["file_code"] + \
                   "\" scrolling=\"no\" frameborder=\"0\" allowfullscreen=\"true\"></iframe>"

    video_image_url = response.json()["result"]["files"][num]["single_img"]

    input_string = "<item> <title><![CDATA[" + video_name + "]]></title><link>" + video_link_on_site + "/</link><pubDate>" + formatted_date + "</pubDate><description></description><content:encoded>" \
                                                                                                                                              "<![CDATA[]]></content:encoded><excerpt:encoded><![CDATA[]]></excerpt:encoded><wp:comment_status><![CDATA[open]]></wp:comment_status><wp:ping_status><![CDATA[closed]]></wp:ping_status><wp:post_name><![CDATA[" \
                   + video_link_on_site + "]]></wp:post_name><wp:status><![CDATA[publish]]></wp:status><wp:post_parent>0</wp:post_parent><wp:menu_order>0</wp:menu_order><wp:post_type><![CDATA[video]]></wp:post_type><wp:post_password><![CDATA[]]></wp:post_password><wp:is_sticky>0</wp:is_sticky><wp:postmeta><wp:meta_key><![CDATA[_edit_last]]></wp:meta_key><wp:meta_value><![CDATA[1]]></wp:meta_value></wp:postmeta><wp:postmeta><wp:meta_key><![CDATA[layout]]></wp:meta_key><wp:meta_value><![CDATA[large]]></wp:meta_value></wp:postmeta><wp:postmeta><wp:meta_key><![CDATA[_layout]]></wp:meta_key><wp:meta_value><![CDATA[field_531980e906752]]></wp:meta_value></wp:postmeta><wp:postmeta><wp:meta_key><![CDATA[aspect_ratio]]></wp:meta_key><wp:meta_value><![CDATA[16by9]]></wp:meta_value></wp:postmeta><wp:postmeta><wp:meta_key><![CDATA[_aspect_ratio]]></wp:meta_key><wp:meta_value><![CDATA[field_531980e906751]]></wp:meta_value></wp:postmeta><wp:postmeta><wp:meta_key><![CDATA[video_type]]></wp:meta_key><wp:meta_value><![CDATA[normal]]></wp:meta_value></wp:postmeta><wp:postmeta><wp:meta_key><![CDATA[_video_type]]></wp:meta_key><wp:meta_value><![CDATA[field_53eb79f33936e]]></wp:meta_value></wp:postmeta><wp:postmeta><wp:meta_key><![CDATA[video_url]]></wp:meta_key><wp:meta_value><![CDATA[" \
                   + video_iframe + "]]></wp:meta_value></wp:postmeta><wp:postmeta><wp:meta_key><![CDATA[_video_url]]></wp:meta_key><wp:meta_value><![CDATA[field_53eb7a453936f]]></wp:meta_value></wp:postmeta><wp:postmeta><wp:meta_key><![CDATA[wp_easy_review_option]]></wp:meta_key><wp:meta_value><![CDATA[a:1:{s:6:\"review\";a:3:{s:14:\"review_heading\";s:0:\"\";s:12:\"summary_text\";s:0:\"\";s:16:\"review_criterias\";a:2:{s:4:\"name\";a:1:{i:0;s:0:"";}s:5:\"score\";a:1:{i:0;s:0:"";}}}}]]></wp:meta_value></wp:postmeta><wp:postmeta><wp:meta_key><![CDATA[count_viewed]]></wp:meta_key><wp:meta_value><![CDATA[0]]></wp:meta_value></wp:postmeta><wp:postmeta></wp:postmeta><wp:postmeta><wp:meta_key><![CDATA[fifu_image_url]]></wp:meta_key><wp:meta_value><![CDATA[" + video_image_url \
                   + "]]></wp:meta_value></wp:postmeta> </item>"
    return input_string


response_folders = requests.get("https://doodapi.com/api/folder/list?key=" + API_KEY)
print("Choose folder ID")
for i in range(len(response_folders.json()["result"]["folders"])):
    print(response_folders.json()["result"]["folders"][i]["fld_id"] + " " + response_folders.json()["result"]["folders"][i]
    ["name"])

FLD_ID = input()

response = requests.get("https://doodapi.com/api/folder/list?key=" + API_KEY + "&fld_id=" + FLD_ID)

num_files = len(response.json()["result"]["files"])

all_items = ""

for i in range(num_files):
    all_items += form_item(i, response)

xmlka = "<?xml version=\"1.0\" encoding=\"UTF-8\" ?><!-- This is a WordPress eXtended RSS file generated by WordPress as an export of your site. --><!-- It contains information about your site's posts, pages, comments, categories, and other content. --><!-- You may use this file to transfer that content from one site to another. --><!-- This file is not intended to serve as a complete backup of your site. --><!-- To import this information into a WordPress site follow these steps: --><!-- 1. Log in to that site as an administrator. --><!-- 2. Go to Tools: Import in the WordPress admin panel. --><!-- 3. Install the \"WordPress\" importer from the list. --><!-- 4. Activate & Run Importer. --><!-- 5. Upload this file using the form provided on that page. --><!-- 6. You will first be asked to map the authors in this export file to users --><!--    on the site. For each author, you may choose to map to an --><!--    existing user on the site or to create a new user. --><!-- 7. WordPress will then import each of the posts, pages, comments, categories, etc. --><!--    contained in this file into your site. --><!-- generator=\"WordPress/6.4.1\" created=\"2024-01-04 14:47\" --><rss version=\"2.0\"	xmlns:excerpt=\"http://wordpress.org/export/1.2/excerpt/\"	xmlns:content=\"http://purl.org/rss/1.0/modules/content/\"	xmlns:wfw=\"http://wellformedweb.org/CommentAPI/\"	xmlns:dc=\"http://purl.org/dc/elements/1.1/\"	xmlns:wp=\"http://wordpress.org/export/1.2/\"><channel><title>" + site_title + "</title><link>" + site_link + "</link><description>"+ site_description +"</description><pubDate>Thu, 04 Jan 2024 14:47:20 +0000</pubDate><language>en-US</language><wp:wxr_version>1.2</wp:wxr_version><wp:base_site_url>" + site_link  + "</wp:base_site_url><wp:base_blog_url>" + site_link  + "</wp:base_blog_url><wp:author><wp:author_id>"+author_id+"</wp:author_id><wp:author_login><![CDATA["+ author_login + "]]></wp:author_login><wp:author_email><![CDATA[" + author_email + "]]></wp:author_email><wp:author_display_name><![CDATA["+ author_login + "]]></wp:author_display_name><wp:author_first_name><![CDATA[]]></wp:author_first_name><wp:author_last_name><![CDATA[]]></wp:author_last_name></wp:author><generator>https://wordpress.org/?v=6.4.1</generator>" + all_items + "</channel></rss>"

with open('output.xml', 'w', encoding='utf-8') as file:
    file.write(xmlka)

print("Process finished successfully")
