import json
from django.core.serializers.json import DjangoJSONEncoder

from pathlib import Path
from django.conf import settings
from .models import AutoChat, ChatRecord

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
    json_path = Path.joinpath(settings.BASE_DIR, 'line_bot/ai_data/content.json')

    # Write the data to the JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(chatbot_data, f, ensure_ascii=False, indent=4, cls=DjangoJSONEncoder)
    
    print("Chatbot script saved to content.json")
    return True


def generate_simple_answer(question: str):
    # Define the path to load the JSON file
    json_path = Path.joinpath(settings.BASE_DIR, 'line_bot/ai_data/content.json')

    # Load the chatbot data from the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        chatbot_data = json.load(f)
    
    # Loop through each intent in the chatbot data
    for intent in chatbot_data['intents']:
        # Check if any keyword in the 'input' list matches the question
        for input_keyword in intent['input']:
            if input_keyword.lower() in question.lower():  # Case-insensitive comparison
                # Return the first response found
                return intent['tag'],intent['responses'][0]
    
    # If no match is found, return a default response
    return "unknown", "🙅 ❌ \nไม่สามารถเข้าใจคำถามได้ รบกวนปรับเปลี่ยนคำถามเล็กน้อยและลองใหม่อีกครั้งนะคะ ❌🙅"


    
def record_chat(question, answer, user=None, source="Simple-AI"):
    """
    Function to record a chat interaction in the database.
    
    Args:
        question (str): The question asked.
        answer (str): The answer provided.
        user (User, optional): The user who asked the question. Defaults to None.
        source (str, optional): The source of the answer (e.g., AI, human). Defaults to "AI". 
    Returns:
        ChatRecord: The saved chat record instance.
    """
    chat_record = ChatRecord.objects.create(
        question=question,
        answer=answer,
        user=user,
        source=source
    )
    return chat_record
