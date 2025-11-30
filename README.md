Adaptive Emotional–Logical Conversational Agent

A multi-agent conversational system that intelligently classifies a user’s message as emotional or logical and responds with the appropriate tone. Built using LangGraph, LangChain, and Google Gemini 2.5 Flash, this project demonstrates adaptive AI behavior, multi-agent routing, and structured output workflows.

📌 Project Summary

Human communication requires different response styles. Some messages need empathy, others need facts. Most chatbots respond the same way every time, making them feel robotic or inappropriate.

This project solves that challenge by creating an agent system that:

Detects whether a user message is emotional or logical

Routes the message to a specialized agent

Generates responses that match user intent

Uses a graph-based architecture for clean, modular design

This project was built as part of the AI Agents Intensive Capstone Project.

🧠 Key Features

Message Type Classification: Identifies emotional vs. logical messages using structured LLM output

Multi-Agent System:

Message Classifier Agent

Therapist Agent (emotional responses)

Logical Agent (factual responses)

Dynamic Routing: LangGraph chooses the correct agent at runtime

State Management: Maintains conversation history

Modular, Extendable Architecture

Continuous Chat Loop for real-time conversation

🏗️ Architecture Overview
1. Message Classifier

Uses the LLM with Pydantic structured output to categorize messages as "emotional" or "logical".

2. Router Node

Reads classification result and forwards the message to the correct agent.

3. Therapist Agent

Provides:

Empathy

Validation

Supportive conversational tone

4. Logical Agent

Provides:

Fact-based answers

Clear explanations

No emotional tone

5. StateGraph

Controls the workflow:

START → Classify → Router → Therapist/Logical → END

📁 Project Structure
.
├── adaptive_chatbot.ipynb   # Jupyter Notebook version
├── main.py                  # Python script version of the chatbot
├── README.md                # Documentation
├── requirements.txt         # Dependency list
└── assets/                  # (Optional) images or thumbnails

⚙️ Installation & Setup
1. Clone the repository
git clone https://github.com/yourusername/emotional-logical-agent.git
cd emotional-logical-agent

2. Install dependencies
pip install -r requirements.txt

3. Add your Google API Key

Create a .env file in the root directory:

GOOGLE_API_KEY=your_key_here

4. Run the application
python main.py


or open the Jupyter Notebook:

jupyter notebook adaptive_chatbot.ipynb

▶️ How It Works (Demo Flow)

User enters a message

The classifier analyzes it

The router selects the appropriate agent

The agent generates a response

Output is displayed in the console

The cycle continues until the user exits

Example:

User: I feel stressed about exams.
Assistant (Therapist): I'm sorry you're feeling stressed...

User: What is the capital of Japan?
Assistant (Logical): The capital of Japan is Tokyo.

🛠️ Tech Stack

Python 3.x

LangGraph

LangChain

Google Gemini 2.5 Flash

Pydantic

dotenv

🔮 Future Enhancements

Multi-emotion classification (sad, angry, confused, stressed)

Sentiment scoring

Memory for long-term personal context

Voice support (speech-to-text, TTS)

Web-based UI using Streamlit/React

Deployment on Google Cloud Run / Vertex AI Agent Engine

Logging, tracing, and observability tools

📜 License

This project is open-source under the MIT License.

❤️ Acknowledgments

This project was built for the 5-Day AI Agents Intensive with Google and demonstrates key concepts like multi-agent workflows, structured output, state management, and LLM-based decision-making.
