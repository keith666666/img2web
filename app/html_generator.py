from flask import current_app
import datetime
import random
import string
import time
import pathlib
import google.generativeai as genai


def generate_unique_id():
    # Get the current time in a precise format
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

    # Generate a random string of 8 characters
    random_chars = "".join(random.choices(string.ascii_letters + string.digits, k=8))

    # Combine the current time and random characters to form a unique ID
    unique_id = f"{current_time}_{random_chars}"

    return unique_id


def clean_html_tags(text):
    if text.startswith("```html"):
        text = text[7:]  # Removes the leading '```html\n'
    if text.strip().endswith("```"):
        text = text.strip()[:-3]  # Removes the trailing '```'
    return text


def generate_html_by_image_file(image_path: str, content_type: str) -> None:
    # for test
    # time.sleep(2)
    # return "20240520093158818673_WqXGnqIM.html"

    bot = "Gemini-1.5-Flash"
    # message = "What is reverse engineering?"
    # message = "Generate a single HTML file from the provided image. The output should include all necessary dynamic information, such as CSS styles, embedded directly within the HTML file. Ensure that the final HTML file is fully self-contained and does not rely on external files or JavaScript."

    genai.configure(api_key=current_app.config["GOOGLE_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = """
    Clear the context of this chat session, generate a single HTML file based on the provided image. The output should meet the following criteria:
    - Include all necessary CSS within the HTML file (no external CSS files).
    - Do not include any JavaScript.
    - Ensure the HTML and CSS are properly formatted and structured.
    - The output should consist only of the HTML code (no explanations, comments, or additional text).
    Provide the complete code for the HTML file below:
    """

    file_name = generate_unique_id() + ".html"
    file_path = f'{current_app.config["TMP_FOLDER"]}/{file_name}'
    img = {
        "mime_type": content_type,
        "data": pathlib.Path(image_path).read_bytes(),
    }
    response = model.generate_content(
        [
            prompt,
            img,
        ],
        stream=True,
    )

    with open(file_path, "w", encoding="utf-8") as file:
        for chunk in response:
            # print(chunk.text)
            file.write(chunk.text)

    return file_name
