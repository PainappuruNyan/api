import keyring

bot_token = keyring.get_password("api", "telegram")
weather_api = keyring.get_password("api", "weather")
news_api = keyring.get_password("api", "news")
