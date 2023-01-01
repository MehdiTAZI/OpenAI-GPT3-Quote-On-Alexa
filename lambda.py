import json
import openai
import random
from alexa import AlexaSkill

#put your open api api key here, please check the pricing model
openai.api_key = "PUT_YOUR_OPENAI_KEY_HERE"

class QuoteSkill(AlexaSkill):
    def __init__(self):
        AlexaSkill.__init__(self)

    def on_launch(self, launch_request, session):
        return get_welcome_message()

    def on_intent(self, intent_request, session):
        intent = intent_request['intent']
        intent_name = intent_request['intent']['name']

        if intent_name == "QuoteIntent":
            return handle_quote_intent(intent, session)
        else:
            raise ValueError("Invalid intent")

    def get_welcome_message():
        speech_output = "Welcome to random quotes"
        return build_response(create_alexa_response(speech_output))

    # Generate a quote using chatbot engine
    def handle_quote_intent(intent, session):
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="Give me one random quote with it author and explain it. the quote should be from mohamed prophete or Jesus or Moise (PBUH)",
            temperature=1,
            max_tokens= random.randint(150, 1000),
            top_p= 0.7
        )
        quote = response['choices'][0]['text']
        speech_output = f"Today's quote is : {quote}"
        
        return build_response(create_alexa_response(speech_output))
    
    def create_alexa_response(output):
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': output
            },
            'reprompt': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': None
                }
            },
            'shouldEndSession': True
        }
    
    def build_response(alexa_response):
        return {
            'version': '1.0',
            'sessionAttributes': {},
            'response': alexa_response
        }
      
    def lambda_handler(event, context):
      skill = QuoteSkill()
      return skill.route_request(event)
