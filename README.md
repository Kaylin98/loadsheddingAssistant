# Eskom Loadshedding Schedule Webhook for Dialogflow

This code provides a simple solution to integrate Eskom Loadshedding Schedule into a conversational platform using Dialogflow API v2. With this webhook, you can ask your Google Assistant or Google Home device about your loadshedding schedule, and it will provide the information using Eskom's API.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3 installed on your local machine
- Dialogflow account and knowledge of creating agents and intents
- Google Cloud Platform project for Dialogflow setup
- Access to Eskom API

### Installation

1. Clone the repository to your local machine:
```
git clone https://github.com/Kaylin98/loadsheddingAssistant.git
```

2. Install the required Python packages using pip:
```
pip install -r requirements.txt
```

### Usage

1. Set up your Dialogflow agent:
- Create a new agent in Dialogflow.
- Create an intent to handle loadshedding schedule queries, e.g., "GetLoadsheddingSchedule".
- Enable the Webhook fulfillment for the intent and specify the URL where your webhook will be deployed.

2. Deploy the webhook:
- Deploy the provided Python script to a server or cloud platform. Ensure it's accessible via HTTPS.
- Provide the webhook URL in the Dialogflow agent's fulfillment section.

3. Configure Dialogflow:
- Train your agent with sample utterances for loadshedding schedule queries.
- Test your agent in the Dialogflow console to ensure it invokes the webhook correctly.

4. Interact with Google Assistant:
- On your Google Assistant-enabled device, ask "Hey Google! What's my loadshedding schedule today?"
- Google Assistant will invoke your Dialogflow agent, which in turn calls the webhook to fetch the schedule from the Eskom API.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


