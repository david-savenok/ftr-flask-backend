from flask import Flask, render_template, request, jsonify
from datetime import datetime
import time
import re

app = Flask(__name__)

def clean_response(text):
    """Clean and format the bot's response"""
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text

def get_bot_response(user_message):
    """Generate bot response based on user input"""
    user_message = user_message.lower()
    
    if 'hello' in user_message or 'hi' in user_message:
        return "Hey there! How can I help you today?"
    
    elif 'help' in user_message:
        return "I can help you with:\n- General questions\n- Technical support\n- Product information\nJust ask away!"
    
    elif 'bye' in user_message:
        return "Goodbye! Have a great day!"
    
    
    return "I'm still learning! Could you try rephrasing that?"

    """
    def get_bot_response(user_message):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    
    try:
        tokenizer = AutoTokenizer.from_pretrained("model-name")
        model = AutoModelForCausalLM.from_pretrained("model-name")
        
        inputs = tokenizer.encode(user_message, return_tensors="pt")
        outputs = model.generate(inputs)
        response = tokenizer.decode(outputs[0])
        
        return response
    except Exception as e:
        print(f"Model error: {e}")
        return "I'm having trouble processing your request right now."
    """

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Get the message from the request
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'error': 'Empty message',
                'response': 'Please send a non-empty message.'
            }), 400
        
        # time.sleep(0.5)
        
        # Get bot response
        response = get_bot_response(user_message)
        
        # Clean the response
        response = clean_response(response)
        
        print(f"User: {user_message}")
        print(f"Bot: {response}")
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().strftime('%I:%M %p')
        })
        
    except Exception as e:
        print(f"Error processing message: {e}")
        return jsonify({
            'error': 'Internal server error',
            'response': "I'm having trouble processing your message right now. Please try again later."
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({
        'error': 'Not found',
        'response': 'The requested resource was not found.'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'response': 'An internal error occurred. Please try again later.'
    }), 500

if __name__ == '__main__':
    app.run(debug=True)