# Real Estate Assistant

🏡 **Real Estate Assistant** is an interactive chatbot designed to assist users with real estate queries. It leverages Google Generative AI to provide comprehensive, informative, and engaging responses based on the provided property details.

## Features

- Upload and process PDF or CSV files containing property details.
- Interactive chat interface for real estate queries.
- Customizable background with user-uploaded images.
- Secure API integration using environment variables.

## Requirements

- Python 3.11
- Streamlit
- Google Generative AI
- dotenv
- pandas
- PyPDF2
- base64

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/real-estate-assistant.git
    cd real-estate-assistant
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your Google Generative AI API key:
    ```ini
    YOUR_API_KEY=your_google_api_key_here
    ```

5. Run the application:
    ```bash
    streamlit run main.py
    ```

## Usage

1. Access the application via the local URL provided by Streamlit.
2. Upload a PDF or CSV file containing property details.
3. Interact with the chatbot to get answers to your real estate queries.

## Troubleshooting

If you encounter any issues, ensure your packages are up-to-date and compatible:

```bash
pip install --upgrade protobuf google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 google-generativeai
