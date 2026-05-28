# Agricare AI Backend

This is the backend system for Agricare AI, a WhatsApp assistant designed to help smallholder poultry farmers diagnose bird diseases instantly and get connected to veterinary help when needed.

## How the Code Works

The core of this system lives inside the agricore folder. Here is how the logic flows when a farmer sends a message:

1. Incoming Request (views.py -> WhatsAppWebhookView)
Twilio forwards the farmer's WhatsApp message to our POST webhook endpoint. The code extracts the phone number, the actual message body, and the farmer's WhatsApp profile name.

2. Automatic Registration (views.py -> Farmer model)
The system checks if the phone number already exists in the database. If it is a new number, it automatically creates a new profile using their WhatsApp display name so they don't have to fill out an onboarding form.

3. AI Consultation (views.py -> get_ai_response)
The system passes the farmer's message to a custom AI advisory API built by our AI team. It uses a retry loop (exponential backoff) to handle network timeouts safely.

4. Urgent Triage (views.py -> HealthCase model)
If the AI's response contains high-risk keywords like Newcastle, Coccidiosis, Gumboro, or an [URGENT] flag, the backend automatically flags the chat, creates a pending Health Case entry, and sets a high severity score. This pushes the case to an admin dashboard for human vets to take over.

5. Twilio Response
Finally, the view formats the AI's diagnostic text into standard TwiML XML and sends it back to Twilio to display as a reply on the farmer's WhatsApp screen.

## Project Structure

* core/ : Contains the main project settings, configuration, and base URL routes.
* agricore/ : Contains our app logic, including database models for Farmers, Conversations, and HealthCases, along with the webhook routing.
* requirements.txt : List of all Python packages needed to run this project.

## Local Setup Instructions

To get this backend running on your own computer, follow these steps:

1. Create a virtual environment and activate it:
python -m venv venv
.\venv\Scripts\Activate.ps1

2. Install the project requirements:
pip install -r requirements.txt

3. Create a .env file in the root folder (where manage.py is) and add your keys:
AI_API_KEY=your_actual_ai_api_key
WHATSAPP_VERIFY_TOKEN=your_secret_handshake_token
SECRET_KEY=your_actual_secret_key

4. Run the database migrations:
python manage.py migrate

5. Start the development server:
python manage.py runserver

Once the server is running, you can view the complete interactive API layout by navigating to http://127.0.0.1:8000/swagger/ in your web browser.