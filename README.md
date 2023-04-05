# telegram-budget

Telegram bot to manage your budget, fully self-hosted

# How to use

Create a `conf.json` organized as follows:
```json
{
    "api-key": "your_api_key",
    "user-id": "your_user_id"
}
```
Then create a `venv` by running the following command:
```bash
python3 -m venv venv
```
Activate the `venv` by running the following command:
```bash
source venv/bin/activate
```
Install the dependencies by running the following command:
```bash
pip install -r requirements.txt
```
Run the bot by running the following command:
```bash
python3 bot.py
```

