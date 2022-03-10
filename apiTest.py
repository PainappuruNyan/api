import requests
from api import config
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

news_api = config.news_api
api_key = config.api_key
bot = Bot(token=config.bot_token)
dp = Dispatcher(bot)


@dp.message_handler(content_types=["text"])
async def daily(message: types.Message):
    geo = requests.get("http://ipwhois.app/json/").json()
    country = geo["country"]
    news = requests.get(f"https://newsapi.org/v2/everything?q={country}&language=ru&apiKey={news_api}").json()[
        "articles"
    ]
    lat = geo["latitude"]
    lon = geo["longitude"]
    city_weather = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&lang=ru&appid={api_key}"
    ).json()
    await bot.send_message(
        message.from_user.id,
        f"{city_weather['weather'][0]['description']}\nтемпература воздуха: {city_weather['main']['temp'] - 273.15}\n"
        f"скорость ветра: {city_weather['wind']['speed']}",
    )
    await bot.send_message(message.from_user.id, news[0]["url"])
    await bot.send_message(message.from_user.id, news[1]["url"])
    await bot.send_message(message.from_user.id, news[2]["url"])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
