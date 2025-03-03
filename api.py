import requests
import datetime

# Cronofy Credentials
CLIENT_ID = "h2XmrSsyqxA2pvKjRwtc4QeupFAyFRPE"
CLIENT_SECRET = "your_client_secret_here"  # Replace with the provided Client Secret
REDIRECT_URI = "http://localhost:5000"  # Change if you have a custom redirect URI

def get_access_token():
    """
    Generates an authorization URL and retrieves the access token
    after user authorizes the application.
    """
    # Authorization URL
    auth_url = (
        f"https://app.cronofy.com/oauth/authorize?response_type=code"
        f"&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=read_free_busy"
    )
    print(f"Go to this URL to authorize: {auth_url}")
    
    # Prompt user to input the authorization code
    code = input("Enter the authorization code: ")
    
    # Exchange authorization code for access token
    token_url = "https://api.cronofy.com/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    
    response = requests.post(token_url, data=payload)
    response.raise_for_status()  # Raise exception for HTTP errors
    return response.json()

def get_free_busy_slots(access_token):
    """
    Fetches free/busy slots using Cronofy API.
    """
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    
    # Specify the date range for availability
    from_date = (datetime.datetime.utcnow()).isoformat()
    to_date = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat()
    
    url = "https://api.cronofy.com/v1/free_busy"
    params = {
        "from": from_date,
        "to": to_date,
        "tzid": "Etc/UTC",  # Adjust timezone as needed
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Raise exception for HTTP errors
    
    return response.json()

if __name__ == "__main__":
    try:
        # Get access token
        auth_response = get_access_token()
        access_token = auth_response["access_token"]
        print(f"Access Token: {access_token}")
        
        # Fetch free/busy slots
        free_busy_data = get_free_busy_slots(access_token)
        print("Available Slots:")
        for slot in free_busy_data["free_busy"]:
            print(
                f"Start: {slot['start']}, End: {slot['end']}, Status: {slot['status']}"
            )
    except Exception as e:
        print(f"Error: {e}")
