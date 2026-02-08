# LLM-NER-System

The **LLM-NER-System** is a modular application for performing **Named Entity Recognition (NER)** using Large Language Models (LLMs). It provides an interactive frontend, a backend API, and supports multiple LLM providers via **OpenRouter**.

This README describes how to set up and run the project **locally using Docker**.

## 🚀 Local Setup with Docker

Follow the steps below to run the LLM-NER-System on your local machine.

### Prerequisites

Before you begin, make sure you have the following:

- **Git** installed
- **Docker Desktop** installed and running
- **OpenRouter account** (it's free) ➡️ https://openrouter.ai/

### 1. Clone the Repository

```
git clone https://github.com/fabianloesch/LLM-NER-System.git
cd LLM-NER-System
```

### 2. Create an OpenRouter API Key

1. Log in to your OpenRouter account

2. Navigate to API Keys

3. Create a new API key

4. Copy the generated key (you will need it in the next steps)

### 3. Configure Environment Variables

1. Navigate to the backend directory `llm-ner-backend`
2. Copy the file `.env.example` and paste it in the same directory
3. Rename the copy to `.env`
4. Open the newly created .env file and insert your OpenRouter API key `OPENROUTER_API_KEY=<YOUR_BEARER_TOKEN>`

### 4. Start the Application with Docker Compose

1. Return to the project root directory
2. Then start the application using Docker Compose `docker compose --profile prod up --build`
3. Docker will build all required images and start the application. This may take a few minutes on the first run.

### 5. Access the Application

<ul>
<li>Once the containers are running, open your browser and navigate to http://localhost</li>
<li>The application is available on port 80 by default</li>
</ul>

## ⚠️ Important Note

To take full advantage of the application, it is necessary to top up your OpenRouter account with a small amount of credits ($5 is more than enough). This allows you to use paid models, which are significantly more powerful. However, it is also possible to use only the free models. Unfortunately, it is not possible to apply the evaluation function to free models, as these are subject to a certain rate limit and the evaluation exceeds this limit.
