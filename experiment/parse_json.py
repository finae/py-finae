import os
import requests
import json
from pprint import pprint

chatgpt_url = "https://shale.live/v1/chat/completions"
chatgpt_headers = {
    "content-type": "application/json",
    "Authorization":"Bearer {}".format("shale-/vOlxxgbDAD7f5")}

def fetch_imagedescription_and_script(prompt,url,headers):

    # Define the payload for the chat model
    messages = [
        {"role": "system", "content": "You are an expert short form video script writer for Instagram Reels and Youtube shorts."},
        {"role": "user", "content": prompt}
    ]

    chatgpt_payload = {
        "model": "Llama-2-13b-chat-hf",
        "messages": messages,
        "temperature": 1.3,
        "max_tokens": 2000,
        "top_p": 1,
        "stop": ["###"]
    }

    # Make the request to OpenAI's API
    response = requests.post(url, json=chatgpt_payload, headers=headers)
    response_json = response.json()

    # Extract data from the API's response
    output = response_json['choices'][0]['message']['content'].strip()
    # print(output)

    start = output.find('[\n')
    end = output.rfind(']\n')

    print(f'start={start}, end={end}')
    print(output[start:(end+1)])
    print('---------')
    output_json = json.loads(output[start:(end+1)])
    pprint(output_json)
    print('---------')

    image_prompts = [k['image_description'] for k in output_json]
    texts = [k['text'] for k in output_json]
    return image_prompts, texts


# Daily motivation, personal growth and positivity

topic = "Success and Achievement"
goal = "inspire people to overcome challenges, achieve success and celebrate their victories"


prompt_prefix = """You are tasked with creating a script for a {} video that is about 30 seconds.
Your goal is to {}.
Please follow these instructions to create an engaging and impactful video:
1. Begin by setting the scene and capturing the viewer's attention with a captivating visual.
2. Each scene cut should occur every 5-10 seconds, ensuring a smooth flow and transition throughout the video.
3. For each scene cut, provide a detailed description of the stock image being shown.
4. Along with each image description, include a corresponding text that complements and enhances the visual. The text should be concise and powerful.
5. Ensure that the sequence of images and text builds excitement and encourages viewers to take action.
6. Strictly output your response in a JSON list format, adhering to the following sample structure:""".format(topic,goal)

sample_output="""
   [
       { "image_description": "Description of the first image here.", "text": "Text accompanying the first scene cut." },
       { "image_description": "Description of the second image here.", "text": "Text accompanying the second scene cut." },
       ...
   ]"""

prompt_postinstruction="""By following these instructions, you will create an impactful {} short-form video.
Output:""".format(topic)

prompt = prompt_prefix + sample_output + prompt_postinstruction

image_prompts, texts = fetch_imagedescription_and_script(prompt,chatgpt_url,chatgpt_headers)
print("image_prompts: ", image_prompts)
print("texts: ", texts)
print(len(texts))