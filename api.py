from flask import Flask, request
from flask_restful import Resource, Api, fields, marshal_with
# It seems 'langchain.chat_models' is a custom module. Ensure it's correctly installed and imported.
from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv
import os

app = Flask(__name__)
api = Api(app)

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the chat model with the API key
chat_model = ChatOpenAI(openai_api_key=api_key)

# To keep track of the chat history
chat_history = []

# Define the resource fields for serialization
# Adjust these fields based on the actual structure of the 'result' you want to return
resource_fields = {
    'response': fields.String,
    # Add more fields as necessary
}

class GPT_response(Resource):
    @marshal_with(resource_fields)
    def post(self):
        # Accessing global variable within the class method
        global chat_history
        
        # Get JSON data from the request
        json_data = request.get_json(force=True)
        prompt = json_data.get('prompt')
        
        # Append the user's prompt to the chat history
        chat_history.append({'user': prompt})
        
        # Use the chat model to generate a response based on the prompt
        result = chat_model.predict(prompt)
        
        # Append the generated response to the chat history
        chat_history.append({'system': result})
        
        # Here you might want to adjust the return statement to match the structure of your 'resource_fields'
        return {'response': result}


# Adding the resource to the API
api.add_resource(GPT_response, '/chat')

if __name__ == '__main__':
    app.run(debug=True)  # Turn off debug mode in production
