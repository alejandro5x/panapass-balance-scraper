### Panapass Balance Scraper with MQTT Integration

This repository contains a Python script designed to automate the retrieval of the Panapass balance using [Playwright](https://playwright.dev/python), with the additional capability to publish the balance to an MQTT broker. Panapass serves as the electronic toll collection system utilized in Panama, and this script facilitates the seamless acquisition of the balance, followed by its transmission to a specified MQTT topic. The script is configured to use an `.env` file for securely storing credentials and configuration settings.

#### Features:
- **Automated Login:** The script securely logs into the Panapass website using credentials stored in an `.env` file, ensuring that sensitive information remains protected.
- **Balance Retrieval:** It efficiently scrapes and retrieves the current Panapass balance.
- **MQTT Publishing:** Once retrieved, the balance is published to an MQTT broker, with the topic and broker details also sourced from the `.env` file.
- **Error Handling:** Robust error handling is implemented to manage issues related to login failures, balance retrieval errors, and MQTT publishing failures.
- **Cross-Platform Compatibility:** The script is designed to operate across various platforms, including Windows, macOS, and Linux.

#### Requirements:
- Python 3.7+
- Playwright for Python
- Paho-MQTT (for MQTT communication)
- Python-dotenv (for loading environment variables)

#### Installation:
1. Clone the repository:
    ```bash
    git clone https://github.com/alejandro5x/panapass-balance-scraper.git
    cd panapass-balance-scraper
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    playwright install
    playwright install-deps
    ```

3. Create an `.env` file in the root directory of the project with the following structure:
    ```
    PANAPASS_NUMBER=yourPanapassNumber
    PANAPASS_PASSWORD=yourPanapassPassword
    MQTT_BROKER=yourMQTTBrokerAddress
    MQTT_TOPIC=yourMQTTTopic
    MQTT_ERROR_TOPIC=yourMQTTErrorTopic
    MQTT_PORT=yourMQTTPort
    MQTT_USER=yourMQTTUser
    MQTT_PASSWORD=yourMQTTPassword
    ```

#### Usage:
```bash
python scrape_balance.py
```

#### Example Output:
Upon execution, the script will retrieve the Panapass balance and publish it to the specified MQTT broker and topic, as defined in the `.env` file:
```
Published balance of $25.10 to MQTT topic 'panapass/balance'.
```
