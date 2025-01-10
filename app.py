from dotenv import load_dotenv
from flask import Flask, request, jsonify
from twilio.rest import Client

import os
from flask_cors import CORS



load_dotenv()


app = Flask(__name__) 
CORS(app)



# Twilio credentials from the environment
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/call', methods=['POST'])
def call():
    # Get the data from the POST request
    data = request.get_json()

    if data is None or 'phoneNumber' not in data:
        return jsonify({'error': 'No phone number provided'}), 400

    phone_number = data['phoneNumber']

    try:
        # Place the call using Twilio API
        call = client.calls.create(
            to=phone_number,  # The phone number to call
            from_=TWILIO_PHONE_NUMBER,  # Your Twilio phone number
            url="http://demo.twilio.com/docs/voice.xml"  # URL that contains the instructions for the call
        )
        
        print(f"Call initiated to {phone_number}, Call SID: {call.sid}")

        return jsonify({
            'success': True,
            'message': 'Call initiated successfully',
            'callSid': call.sid
        })
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

@app.route('/hangup', methods=['POST'])
def hangup():
    data = request.get_json()
    call_sid = data.get('callSid')  # Expecting the CallSid in the body of the request

    if call_sid:
        try:
            # Update the call status to 'completed' using the CallSid
            call = client.calls(call_sid).update(status='completed')
            return jsonify({'success': True, 'message': 'Call ended successfully'})
        except Exception as e:
            return jsonify({'error': f'Failed to end call: {str(e)}'}), 500
    return jsonify({'error': 'CallSid is required'}), 400


if __name__ == '__main__':
    # Run the app with debug mode on
    app.run()
