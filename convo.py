import random
import requests

def get_calendly_slots():
    """
    Fetch available Calendly slots using their API.
    """
    # Replace with your actual token
    auth_token = "eyJraWQiOiIxY2UxZTEzNjE3ZGNmNzY2YjNjZWJjY2Y4ZGM1YmFmYThhNjVlNjg0MDIzZjdjMzJiZTgzNDliMjM4MDEzNWI0IiwidHlwIjoiUEFUIiwiYWxnIjoiRVMyNTYifQ.eyJpc3MiOiJodHRwczovL2F1dGguY2FsZW5kbHkuY29tIiwiaWF0IjoxNzMzOTQxODg1LCJqdGkiOiI4NWE4NzQ4NS03MzQ1LTRmNGItYWIzZi1mYTY2NDhkYTM2NDEiLCJ1c2VyX3V1aWQiOiJhZDAxZGViNS0yMWY1LTQ3MTYtYmEyMC04Y2U1YmZkNGRkNDIifQ.Oj71NAI3B1JDYGCQr0AR9UyqmnvVlbKBEdzltHf_dZMEzlS5H1cL3FCsaCQ1-a9_x01Xbjr240z540XP21lKjw"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }

    # Replace with the actual Calendly API endpoint for availability schedules
    url = "https://api.calendly.com/availability/schedules"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        # Extract slots from the nested structure, customize based on API response
        slots = [
            {"day": slot["start_time"].split("T")[0], "time": slot["start_time"].split("T")[1][:5]}
            for slot in data.get("collection", [])
        ]
        return slots
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Calendly slots: {e}")
        return []

class AIColdCaller:
    def __init__(self):
        self.state = "intro"  # Initial state of the conversation
        self.agent_name = random.choice(["Brandon", "Louis", "Danyal", "Abdul"])  # Randomly pick a name for the agent

    def respond(self, user_input):
        """
        Process user input and determine the next response and state.
        """
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
        if any(word in user_input.lower() for word in ["yes", "yup", "yeah", "yea", "ok", "sure", "okay", "go ahead"]):
            self.state = "identify_challenges"
            return (
                f"Great! I’ve been speaking to a lot of people like you. "
                f"Typically, they face two major issues: [Inefficient resource allocation] and [Inconsistent customer engagement]. Does that resonate with you?"
            )
        elif "no" in user_input.lower():
            return "Understood. Should I quickly explain why I’m calling, and if it’s not relevant, we’ll leave it there?"
        else:
            self.state = "end"
            return "No worries. Let me know if you're available later."

    def handle_challenges(self, user_input):
        if any(word in user_input.lower() for word in ["yes", "yup", "yeah", "yea", "ok", "sure", "okay", "go ahead"]):
            self.state = "qualify"
            return (
                "Could you share more details about this problem? "
                "What impact is it having on your business, and what have you tried to solve it?"
            )
        else:
            self.state = "end"
            return "Got it. Would you like me to send over some more details?"

    def handle_qualify(self, user_input):
        if any(word in user_input.lower() for word in ["yes", "yup", "yeah", "yea", "ok", "sure", "okay", "go ahead"]):
            self.state = "pitch"
            return (
                "Based on what you’ve shared, it seems like [problem]. "
                "We helped [another client] solve this issue by [solution], leading to [outcome]. "
                "Does this sound interesting to you?"
            )

    def handle_pitch(self, user_input):
        if any(word in user_input.lower() for word in ["yes", "yup", "yeah", "yea", "ok", "sure", "okay", "go ahead"]):
            self.state = "close"
            slots = get_calendly_slots()
            if not slots:
                return "Unfortunately, I couldn't fetch availability slots at the moment. Can I email you the details instead?"
            times = " or ".join([f"{slot['day']} at {slot['time']}" for slot in slots])
            return f"Great! Would {times} work for a quick 15-minute call?"
        else:
            self.state = "end"
            return "Understood. Let me know if you’d like to revisit this in the future."

    def handle_close(self, user_input):
        if any(word in user_input.lower() for word in ["yes", "yup", "yeah", "yea", "ok", "sure", "okay", "go ahead"]):
            self.state = "schedule"
            return "Perfect! I’ll send you a calendar invitation. Could you confirm your email?"
        else:
            self.state = "end"
            return "Understood. Let me know if you’d like to revisit this in the future."

    def handle_schedule(self, user_input):
        self.state = "end"
        return (
            "Thank you! I’ve sent the invitation. Looking forward to speaking with you on the scheduled day. "
            "Thank you for your time. Have a great day!"
        )

    def end_conversation(self):
        self.state = "end"
        return "Thank you for your time. Have a great day!"

# Simulate the AI Cold Caller
if __name__ == "__main__":
    cold_caller = AIColdCaller()
    print(
        f"AI Cold Caller ({cold_caller.agent_name}): Hey, it’s {cold_caller.agent_name} calling from Titans AI. "
        "Do you have 30 seconds to hear why I’m reaching out?"
    )

    while cold_caller.state != "end":
        user_input = input("User: ")
        response = cold_caller.respond(user_input)
        print(f"AI Cold Caller ({cold_caller.agent_name}): {response}")
