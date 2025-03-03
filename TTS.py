import random
import torch
from IPython.display import display, Audio
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'kokoro_82M'))
import numpy as np

from istftnet import AdaIN1d, Decoder
from models import build_model
from kokoro import generate

# Install dependencies silently (this paert should be run in a notebook or shell)
# !git lfs install
# !git clone https://huggingface.co/hexgrad/Kokoro-82M
# after cloning, move the folder to the addon directory and change the name to "kokoro_82M"
# %cd kokoro_82M
# !apt-get -qq -y install espeak-ng > /dev/null 2>&1
# !pip install -q phonemizer torch transformers scipy munch

# Build the model and load the default voicepack
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# change the path to the model file to the correct path "kokoro-v0_19.pth"
MODEL = build_model('/Users/sasanksasi/Downloads/project/taitan ai/addon/kokoro_82M/kokoro-v0_19.pth', device)
VOICE_NAME = 'af'  # Default voice is a 50-50 mix of Bella & Sarah
# change the path to the voice file to the correct path "voices{VOICE_NAME}.pt"
VOICEPACK = torch.load(f'/Users/sasanksasi/Downloads/project/taitan ai/addon/kokoro_82M/voices/am_adam.pt', map_location=device)
print(f'Loaded voice: {VOICE_NAME}')

def generate_voice(text, output_file="output.wav"):
    """
    Generate TTS output for the given text using Kokoro-82M.
    """
    try:
        audio, _ = generate(MODEL, text, VOICEPACK, lang=VOICE_NAME[0])
        # Convert NumPy array to PyTorch tensor if necessary
        if isinstance(audio, np.ndarray):
            audio = torch.tensor(audio)
        # Save the audio to a file
        from scipy.io.wavfile import write
        write(output_file, 24000, audio.cpu().numpy())
        print(f"Audio saved to {output_file}. Playing audio...")
        # Play the audio
        display(Audio(data=audio.cpu().numpy(), rate=24000, autoplay=True))
    except Exception as e:
        print(f"Error generating voice: {e}")

class AIColdCaller:
    def __init__(self):
        self.state = "intro"
        self.agent_name = random.choice(["Brandon", "Louis", "Danyal", "Abdul"])

    def respond(self, user_input):
        if self.state == "intro":
            return self.handle_intro(user_input)
        elif self.state == "identify_challenges":
            return self.handle_challenges(user_input)
        elif self.state == "qualify":
            return self.handle_qualify(user_input)
        elif self.state == "pitch":
            return self.handle_pitch(user_input)
        elif self.state == "close":
            return self.handle_close(user_input)
        elif self.state == "schedule":
            return self.handle_schedule(user_input)
        else:
            return self.end_conversation()

    def handle_intro(self, user_input):
        if any(word in user_input.lower() for word in ["yes", "yup", "yeah", "ok", "sure", "okay", "go ahead"]):
            self.state = "identify_challenges"
            return (
                "Great! I’ve been speaking to a lot of people like you. "
                "Typically, they face two major issues: [Inefficient resource allocation] and [Inconsistent customer engagement]. Does that resonate with you?"
            )
        elif "no" in user_input.lower():
            return "Understood. Should I quickly explain why I’m calling, and if it’s not relevant, we’ll leave it there?"
        else:
            self.state = "end"
            return "No worries. Let me know if you're available later."

    def handle_challenges(self, user_input):
        if any(word in user_input.lower() for word in ["yes", "yup", "yeah", "ok", "sure", "okay", "go ahead"]):
            self.state = "qualify"
            return (
                "Could you share more details about this problem? "
                "What impact is it having on your business, and what have you tried to solve it?"
            )
        else:
            self.state = "end"
            return "Got it. Would you like me to send over some more details?"

    def handle_qualify(self, user_input):
        # Store the user input in the problem variable
        self.problem = user_input
        self.state = "pitch"
        return (
            f"Based on what you’ve shared, it seems like {self.problem}. "
            "We helped [another client] solve this issue by [solution], leading to [outcome]. "
            "Does this sound interesting to you?"
        )

    def handle_pitch(self, user_input):
        if any(word in user_input.lower() for word in ["yes", "yup", "yeah", "ok", "sure", "okay", "go ahead"]):
            self.state = "close"
            return f"Great! Would work for a quick 15-minute call?"
        else:
            self.state = "end"
            return "Understood. Let me know if you’d like to revisit this in the future."

    def handle_close(self, user_input):
        if any(word in user_input.lower() for word in ["yes", "yup", "yeah", "ok", "sure", "okay", "go ahead"]):
            self.state = "schedule"
            return "Perfect! I’ll send you a calendar invitation. Could you confirm your email?"
        else:
            self.state = "end"
            return "Understood. Let me know if you’d like to revisit this in the future."

    def handle_schedule(self, user_input):
        # Store the user input in the email variable
        self.email = user_input
        self.state = "end"
        return (
            "Thank you! I’ve sent the invitation. Looking forward to speaking with you on the scheduled day. "
            "Thank you for your time. Have a great day!"
        )

    def end_conversation(self):
        self.state = "end"
        return "Thank you for your time. Have a great day!"

if __name__ == "__main__":
    cold_caller = AIColdCaller()
    initial_text = (
        f"Hey, it’s {cold_caller.agent_name} calling from Titans AI. "
        "Do you have 30 seconds to hear why I’m reaching out?"
    )
    generate_voice(initial_text)

    while cold_caller.state != "end":
        user_input = input("User: ")
        response = cold_caller.respond(user_input)
        generate_voice(response)