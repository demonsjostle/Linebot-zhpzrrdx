import json
from django.core.serializers.json import DjangoJSONEncoder

from pathlib import Path
from django.conf import settings
from .models import AutoChat

def save_chatbot_script_to_json():
    # Initialize the intents structure
    chatbot_data = {"intents": []}
    
    # Retrieve all AutoChat records
    autochats = AutoChat.objects.all()
    
    # Group questions and answers by tag (you can customize this part based on your needs)
    for autochat in autochats:
        tags = autochat.tags.all()
        tag_string = autochat.question
        if tags:
            tag_names = [tag.tag_name for tag in tags]
            tag_string = ", ".join(tag_names)

        
        # Split the question by commas to handle multiple inputs
        input_list = [question.strip() for question in autochat.question.split(',')]
    
       
        
        # Create a new tag entry with the question and responses
        if autochat.image and settings.CSRF_TRUSTED_ORIGINS:
            image_url = "--img--" + settings.CSRF_TRUSTED_ORIGINS[0]+autochat.image.url 
            chatbot_data['intents'].append({
                'tag': tag_string,
                'input': input_list,  # Assuming the input is the same as the question
                'responses': [autochat.answer+image_url]
            })
        else:
            chatbot_data['intents'].append({
                'tag': tag_string,
                'input': input_list,  # Assuming the input is the same as the question
                'responses': [autochat.answer]
            })
    
    # Define the path to save the JSON file
    json_path = Path.joinpath(settings.BASE_DIR, 'line_bot/chatbot_model/content.json')

    # Write the data to the JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(chatbot_data, f, ensure_ascii=False, indent=4, cls=DjangoJSONEncoder)
    
    print("Chatbot script saved to content.json")




