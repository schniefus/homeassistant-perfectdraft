# Home Assistant PerfectDraft Custom Component

This custom component integrates the PerfectDraft API with Home Assistant, allowing you to monitor your PerfectDraft machines.

## Installation

1. Add this repository to HACS.
2. Install the "PerfectDraft" integration.
3. Configure the integration with your PerfectDraft API credentials.

## Configuration

In your `configuration.yaml`:

```yaml
sensor:
  - platform: perfectdraft
    email: YOUR_EMAIL
    password: YOUR_PASSWORD
    x_api_key: YOUR_API_KEY
    recaptcha_token: YOUR_RECAPTCHA_TOKEN

Add the Repository to HACS
Go to your Home Assistant instance.
Open the HACS interface.
Click on the three dots menu in the top right corner and select "Custom repositories".
Add your GitHub repository URL and select the category "Integration".
Your custom component should now appear in HACS, and you can install it.
Step 6: Configure the Integration
After installing the component through HACS, add the configuration to your configuration.yaml file as specified in the README.md:

yaml
Copy code
sensor:
  - platform: perfectdraft
    email: YOUR_EMAIL
    password: YOUR_PASSWORD
    x_api_key: YOUR_API_KEY
    recaptcha_token: YOUR_RECAPTCHA_TOKEN
Restart Home Assistant to apply the changes.
