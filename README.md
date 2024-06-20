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
    recaptcha_site_key: YOUR_RECAPTCHA_SITE_KEY
    recaptcha_secret_key: YOUR_RECAPTCHA_SECRET_KEY
