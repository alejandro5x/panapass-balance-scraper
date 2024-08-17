### Panapass Balance Scraper with MQTT Integration

This repository contains a Python script that automates the retrieval of the Panapass balance using [Playwright](https://playwright.dev/python) and publishes the balance to an MQTT broker. Panapass is the electronic toll collection system used in Panama, and this script allows users to automatically check their balance and send it to an MQTT topic for further processing or monitoring.

#### Features:
- **Automated Login:** Automatically logs into the Panapass website using the provided credentials.
- **Balance Retrieval:** Scrapes the current Panapass balance.
- **MQTT Publishing:** Publishes the retrieved balance to a specified MQTT broker and topic.
- **Error Handling:** Provides clear error messages if login fails, the balance cannot be retrieved, or MQTT publishing fails.
- **Cross-Platform:** Works on Windows, macOS, and Linux.

#### Requirements:
- Python 3.7+
- Playwright for Python
- Paho-MQTT (for MQTT communication)

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
    ```

#### Usage:
```bash
python scrape_balance.py --username yourPanapassUsername --password yourPanapassPassword --mqtt-broker yourBrokerAddress --mqtt-topic yourTopic
```

#### Example Output:
The script will publish the Panapass balance to the specified MQTT broker and topic:
```
Published balance of $25.00 to MQTT topic 'panapass/balance'.
```
