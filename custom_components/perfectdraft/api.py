import requests

class PerfectDraftAPI:
    def __init__(self, email, password, x_api_key, recaptcha_token):
        self.base_url = "https://api.perfectdraft.com"
        self.email = email
        self.password = password
        self.x_api_key = x_api_key
        self.recaptcha_token = recaptcha_token
        self.access_token = None
        self.id_token = None
        self.refresh_token = None

    def authenticate(self):
        url = f"{self.base_url}/authentication/sign-in"
        payload = {
            "email": self.email,
            "password": self.password,
            "recaptchaAction": "Android_recaptchaThatWorks/login",
            "recaptchaToken": self.recaptcha_token
        }
        headers = {"x-api-key": self.x_api_key}
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        self.access_token = data['AccessToken']
        self.id_token = data['IdToken']
        self.refresh_token = data['RefreshToken']

    def get_status(self):
        url = f"{self.base_url}/api/me"
        headers = {"x-access-token": self.access_token}
        response = requests.get(url, headers=headers)
        return response.json()

    def get_machine_details(self, machine_id):
        url = f"{self.base_url}/api/perfectdraft_machines/{machine_id}"
        headers = {"x-access-token": self.access_token}
        response = requests.get(url, headers=headers)
        return response.json()
