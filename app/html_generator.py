from flask import current_app
import datetime
import random
import string


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


def generate_html_by_image_file(image_path: str) -> None:
    client = current_app.poe_client

    bot = "Gemini-1.5-Flash"
    # message = "What is reverse engineering?"
    # message = "Generate a single HTML file from the provided image. The output should include all necessary dynamic information, such as CSS styles, embedded directly within the HTML file. Ensure that the final HTML file is fully self-contained and does not rely on external files or JavaScript."
    message = """
    Generate a single HTML file based on the provided image. The output should meet the following criteria:
    - Include all necessary CSS within the HTML file (no external CSS files).
    - Do not include any JavaScript.
    - Ensure the HTML and CSS are properly formatted and structured.
    - The output should consist only of the HTML code (no explanations, comments, or additional text).
    Provide the complete code for the HTML file below:
    """

    proxy_context = [
        {"https": "http://127.0.0.1:7890", "http": "http://127.0.0.1:7890"},
    ]
    tokens = {
        "b": "OUeVasgsO2ctdGBNzhHm9A%3D%3D",
        "lat": "s8T5V6Wj6AAYvfqNdHGVpfzJSaslOGi7hN1OUpmuPw%3D%3D",
    }
    # for local usage
    # client=PoeApi(cookie=tokens, proxy=proxy_context)

    local_paths = [image_path]
    msgPrice = 25
    chatCode = "2balll258t5o4bkt0o3"
    file_name = generate_unique_id() + ".html"
    file_path = f'{current_app.config["TMP_FOLDER"]}/{file_name}'

    with open(file_path, "w", encoding="utf-8") as file:
        # Iterate over the chunks of data
        for chunk in client.send_message(
            bot, message, chatCode=chatCode, msgPrice=msgPrice, file_path=local_paths
        ):
            # Get the response part of the chunk
            response = chunk["response"]
            # Clean the response to remove leading and trailing 'html' markers
            cleaned_response = clean_html_tags(response)
            # Write the cleaned response to the file
            file.write(cleaned_response)
            # Optionally, print to console if needed
            # print(cleaned_response, end="", flush=True)
    return file_name
