# EchoServe AI - AI-Powered Customer Voice Support

![EchoServe🎧]

## Overview
**EchoServe AI** is an intelligent AI-powered voice support agent designed to enhance customer service by providing real-time, natural voice interactions. It leverages advanced **LLM-powered conversational AI**, **speech-to-text**, and **text-to-speech** models for seamless and efficient query resolution.

## Features
- **Kokoro Voice Model** for high-quality, natural voice interactions
- **LLM-driven conversational AI** for contextual query understanding
- **Real-time speech-to-text and text-to-speech conversion**
- **Intent recognition and sentiment analysis** for accurate responses
- **Multi-channel support** (call centers, chatbots, virtual assistants)
- **Scalable API-based architecture** for seamless integration

## Installation
### Clone the Repository
```bash
git clone https://github.com/sasank-sasi/EchoServe-AI.git
cd EchoServe-AI
```

### Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
### 1. Set Up Environment Variables
Create a `.env` file in the root directory and add your API keys:
```env
KOKORO_API_KEY=your_kokoro_api_key
LLM_API_KEY=your_llm_api_key
```

### 2. Start the Voice AI Agent
```bash
python main.py
```


## API Endpoints
| Endpoint       | Method | Description                        |
|---------------|--------|------------------------------------|
| `/transcribe` | POST   | Converts speech to text           |
| `/synthesize` | POST   | Converts text to speech           |
| `/respond`    | POST   | Generates AI-powered responses    |
| `/analyze`    | POST   | Performs sentiment and intent analysis |

## Contribution
We welcome contributions! To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Added a new feature'`)
4. Push to your branch (`git push origin feature-branch`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For inquiries and collaboration, reach out to [sasank-sasi](https://github.com/sasank-sasi).
