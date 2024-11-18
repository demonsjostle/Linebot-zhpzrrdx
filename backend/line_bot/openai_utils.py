from openai import OpenAI
from decouple import config 
import json
import re
from django.conf import settings
from pathlib import Path
from .models import AutoChat, GPTConfig

OPENAI_KEY = config('OPENAI_KEY')


def prepare_gpt_dataset():

    train_data = []
    valid_data = []

    autochats = AutoChat.objects.all()
    system = GPTConfig.objects.filter(in_use=True).order_by('-id').first()

    for autochat in autochats:
        # Split the question by commas to handle multiple inputs
        input_list = [question.strip() for question in autochat.question.split(',')]
    
        for question in input_list:
            # Create a new tag entry with the question and responses
            if autochat.image and settings.CSRF_TRUSTED_ORIGINS:
                image_url = "--img--" + settings.CSRF_TRUSTED_ORIGINS[0]+autochat.image.url 
                train_data.append(
                    {
                        "messages": [
                        {"role": "system", "content": system.system},
                        {"role": "user", "content": question},
                        {"role": "assistant", "content": autochat.answer+image_url}
                        ]
                    }
                )
            else:
                train_data.append(
                    {
                        "messages": [
                            {"role": "system", "content": system.system},
                            {"role": "user", "content": question},
                            {"role": "assistant", "content": autochat.answer}
                        ]
                    }
                )

        # valid_data.append(
        #     {
        #         "messages": [
        #             {"role": "system", "content": system},
        #             {"role": "user", "content": d.validation_question},
        #             {"role": "assistant", "content": d.validation_answer}
        #         ]
        #     }
        # )

    # Write the dataset to a JSONL file
    with open(Path.joinpath(settings.BASE_DIR, 'line_bot/ai_data/training_data.jsonl'), 'w', encoding='utf-8') as f:
        for entry in train_data:
            json.dump(entry, f, ensure_ascii=False)
            f.write('\n')

    # with open(Path.joinpath(settings.BASE_DIR, 'bot/validation_data.jsonl'), 'w', encoding='utf-8') as f:
    #     for entry in valid_data:
    #         json.dump(entry, f, ensure_ascii=False)
    #         f.write('\n')
    print("Success prepare dataset")


def fine_tuning_gpt(training_data_path=None, model="gpt-4o", n_epochs=4):
    """
    Fine-tunes a GPT-3.5-turbo model with the given training data.

    :param api_key: Your OpenAI API key.
    :param training_data_path: Path to the JSONL file containing training data.
    :param model: The model to fine-tune. Default is "gpt-3.5-turbo".
    :param n_epochs: Number of training epochs. Default is 4.
    :return: The ID of the fine-tuned model and its status.
    """

    if training_data_path == None:
        training_data_path = Path.joinpath(
            settings.BASE_DIR, 'line_bot/ai_data/training_data.jsonl')
    # validation_data_path = Path.joinpath(
    #     settings.BASE_DIR, 'bot/validation_data.jsonl')

    client = OpenAI(
        api_key=str(OPENAI_KEY))

    training_file = client.files.create(
        file=open(training_data_path, "rb"),
        purpose="fine-tune"
    )
    # validation_file = client.files.create(
    #     file=open(validation_data_path, "rb"),
    #     purpose="fine-tune"
    # )

    print("Training")
    try:

        response = client.fine_tuning.jobs.create(
            training_file=training_file.id,
            # validation_file=validation_file.id,
            model="gpt-4o-2024-08-06",

        )
        print(response)


        if response:
            return True
    except:
        return False


def generate_gpt_answer(question: str):
    system = GPTConfig.objects.filter(in_use=True).order_by('-id').first()
    if system:
        fine_tuning_model = system.fine_tuned_model
        system_content = system.system
        client = OpenAI(
            api_key=str(OPENAI_KEY))

        completion = client.chat.completions.create(
            model=fine_tuning_model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": question}
            ]
        )

        return completion.choices[0].message.content

    else:
        # fine_tuning_model = ""
        # system_content = "คณมีชื่อว่าเติมดี คุณเป็นแชทบอทเกี่ยวกับระบบเติมเงิน โปรดตอบคำถามและนำทางผู้ใช้ในเรื่องเกี่ยวกับระบบเติมเงินเท่านั้น"
        return "ขออภัยระบบมีปัญหา"


def get_fine_tuned_models(api_key=str(OPENAI_KEY)):
    """
    Retrieves and returns a list of all fine-tuned model IDs associated with the provided OpenAI API key.

    :param api_key: The OpenAI API key to authenticate the request.
    :return: A list of fine-tuned model IDs.
    """
    # Set the OpenAI API key
    client = OpenAI(api_key=api_key)

    # List 10 fine-tuning jobs
    jobs = client.fine_tuning.jobs.list(limit=10)

    print(jobs)





######################### Manage database #################################
# def generate_database_to_json():
#     data = Data.objects.all()
#     dataset = []
#     for d in data:
#         dataset.append({
#             'question': d.training_question,
#             'answer': d.training_answer,
#         })
#
#     # Write the dataset to a JSON file
#     with open('dataset.json', 'w', encoding='utf-8') as json_file:
#         json.dump(dataset, json_file, ensure_ascii=False, indent=4)
#
#
# def add_data_to_database(json_file_path):
#     with open(json_file_path, 'r', encoding='utf-8') as file:
#         data_list = json.load(file)
#         for item in data_list:
#             data = Data(
#                 training_question=item['question'], training_answer=item['answer'])
#             data.save()
#     print(f"Successfully loaded {len(data_list)} records into the database.")
######################### Manage database #################################
