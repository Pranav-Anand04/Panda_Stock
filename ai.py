import os
from flask import Blueprint, request, jsonify
from google import genai
from flask_cors import CORS

ai_bp = Blueprint('ai', __name__)
CORS(ai_bp)

api_key = "AIzaSyCvxnk69RbQWMcs8BtseG2lf8kO1h370lk" 


client = genai.Client(api_key=api_key)

@ai_bp.route('/ask_ai', methods=['POST'])
def ask_ai():
    data = request.json
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=user_query
        )


        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
