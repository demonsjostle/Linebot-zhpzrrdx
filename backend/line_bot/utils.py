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
        # Check if the tag already exists in intents
        intent_exists = next((item for item in chatbot_data['intents'] if item['tag'] == autochat.question), None)
        
        if intent_exists:
            # Append the answer to the existing tag
            intent_exists['responses'].append(autochat.answer)
        else:
            # Create a new tag entry with the question and response
            chatbot_data['intents'].append({
                'tag': autochat.question,
                'input': [autochat.question],  # Assuming the input is the same as the question
                'responses': [autochat.answer]
            })
    
    # Define the path to save the JSON file
    json_path = Path.joinpath(settings.BASE_DIR, 'line_bot/chatbot_model/content.json')

    # Write the data to the JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(chatbot_data, f, ensure_ascii=False, indent=4, cls=DjangoJSONEncoder)
    
    print("Chatbot script saved to content.json")




