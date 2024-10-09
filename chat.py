import random
import json
import torch
from openai import OpenAI
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from dotenv import load_dotenv
import os


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load the intents file
with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

# Load the model
FILE = "data.pth"
data = torch.load(FILE)

# Load the data from the model
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Mai"


# Function to get the response from the model
def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    # If primary model doesn't have a confident response, it will call ChatGPT API
    return chatgpt_response(msg)


# Function to get a response from OpenAI's ChatGPT API
def chatgpt_response(msg):
    """
    Get a response from OpenAI's ChatGPT API.
    """
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for a racing club called EpiRacing, part of EPITA Paris. Your responses should always be related to car racing, club activities, go-karting, racing events, and the EPITA student experience. Stay on theme and avoid generic responses."},
                
            {"role": "user", "content": msg},
        ],
        max_tokens=100,
        temperature=0.7)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling ChatGPT API: {e}")
        return "Sorry, I didn't get that. Perhaps, try rephrasing your question please."



if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        #where you input your question
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

