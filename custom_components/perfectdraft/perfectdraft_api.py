import requests
from bs4 import BeautifulSoup

class PerfectDraftAPI:
    def __init__(self, email, password, x_api_key, recaptcha_site_key, recaptcha_secret_key):
        self.base_url = "https://api.perfectdraft.com"
        self.email = email
        self.password = password
        self.x_api_key = x_api_key
        self.recaptcha_site_key = recaptcha_site_key
        self.recaptcha_secret_key = recaptcha_secret_key
        self.access_token = None
        self.id_token = None
        self.refresh_token = None
    
    def get_recaptcha_token(self):
        # Replace this URL with the URL of your page that has the reCAPTCHA v3 integration
        recaptcha_page_url = "https://your-site-with-recaptcha.com"
        response = requests.get(recaptcha_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        recaptcha_token = None
        for script in soup.find_all('script'):
            if 'grecaptcha.execute' in script.text:
                recaptcha_token = script.text.split("'")[1]
                break
        
        return recaptcha_token

    def authenticate(self):
        recaptcha_token = self.get_recaptcha_token()
        if not recaptcha_token:
            print("Failed to get reCAPTCHA token")
            return False

        url = f"{self.base_url}/authentication/sign-in"
        headers = {
            "x-api-key": self.x_api_key
        }
        payload = {
            "email": self.email,
            "password": self.password,
            "recaptchaAction": "Android_recaptchaThatWorks/login",
            "recaptchaToken": recaptcha_token
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get("AccessToken")
            self.id_token = data.get("IdToken")
            self.refresh_token = data.get("RefreshToken")
            return True
        return False

    def check_status(self):
        url = f"{self.base_url}/lager-top/status"
        response = requests.get(url)
        return response.status_code == 200

    def get_user_info(self):
        url = f"{self.base_url}/api/me"
        headers = {
            "x-access-token": self.access_token
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_machine_info(self, machine_id):
        url = f"{self.base_url}/api/perfectdraft_machines/{machine_id}"
        headers = {
            "x-access-token": self.access_token
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None
