from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
import time
import logging
import asyncio
import DataBase
import Myparser

configs = {
    'token': ''
}

logging.basicConfig(level=logging.INFO)
myapibot = Bot(token=configs['token'])
bot = Dispatcher(myapibot)
db = DataBase.DataBase()

CSGOnews = Myparser.news()
CSGOupdate = Myparser.updates()
CSGOmatches = Myparser.matches()
CSGOresult = Myparser.results()

@bot.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.answer(f"""
						My commands:
						/subscribe_updates or /SU - Subscribe to news updates
						/unsubscribe_updates or /UU - Unsubscribe from news updates
						/subscribe_matches or /SM - Subscribe to matches
						/unsubscribe_matches or /UM - Unsubscribe from matches
						/subscribe_news or /SN - Subscribe to news
						/unsubscribe_news or /UN - Unsubscribe from news
						/matches_results - /MR Get matches result today""", reply_markup=keyboard)

@bot.message_handler(commands=['author'])
async def author(message):
	await message.answer(f"Github - https://github.com/Fo1Go\nVK - https://vk.com/seva229\nTelegram - @Folgogo", reply_markup=keyboard)

# Subscribed to updates
@bot.message_handler(commands=['subscribe_updates', 'SU'])
async def subscribe_updates(message):
	db.update_subscription_updates(message.chat.id,True)
	await message.answer(f"You subscribed on csgo updates news.", reply_markup=keyboard)


# Unsubscribed from updates
@bot.message_handler(commands=['unsubscribe_updates', 'UU'])
async def unsubscribe_updates(message):
	db.update_subscription_updates(message.chat.id,False)
	await message.answer("You unsubscribe from csgo updates news.", reply_markup=keyboard)


# Subscribed to matches
@bot.message_handler(commands=['subscribe_matches', 'SM'])
async def subscribe_matches(message):
	db.update_subscription_matches(message.chat.id,True)
	await message.answer("You subscribed on matches csgo.", reply_markup=keyboard)


# Unsubscribed from matches
@bot.message_handler(commands=['unsubscribe_matches', 'UM'])
async def unsubscribe_matches(message):
	db.update_subscription_matches(message.chat.id,False)
	await message.answer("You unsubscribe from matches csgo.", reply_markup=keyboard)


# Subscribed to news
@bot.message_handler(commands=['subscribe_news', 'SN'])
async def subscribe_news(message):
	db.update_subscription_news(message.chat.id,True)
	await message.answer("You subscribed on news csgo.", reply_markup=keyboard)


# Unsubscribed from news
@bot.message_handler(commands=['unsubscribe_news', 'UN'])
async def unsubscribe_news(message):
	db.update_subscription_news(message.chat.id,False)
	await message.answer("You unsubscribed from news csgo.", reply_markup=keyboard)

# Get matches results today
@bot.message_handler(commands=['matches_results', 'MR'])
async def matches_results(message):
	results = CSGOresult.get_result()
	result = ''
	if results[0]:
		teams = results[2]['teams']
		tournaments = results[2]['tournaments']
		scores = results[2]['scores']
		view = results[2]['view']
		url = results[2]['url']
		for i in range(len(teams)):
			w = teams[i].split("|")[0]
			l = teams[i].split("|")[1]
			team = ' \tVS\t '.join(teams[i].split("|"))
			result =  result + f"Played {team}\nWon - {w}, Lose - {l} \nFinaly score - {scores[i]} in {view[i]} \nTournament - {tournaments[i]}\nUrl on match - {url[i]}\n\n"
	await message.answer(f"{results[1]}\n\n{result}", reply_markup=keyboard)

a = types.KeyboardButton('/author')
h = types.KeyboardButton('/help')
su = types.KeyboardButton('/subscribe_updates')
uu = types.KeyboardButton('/unsubscribe_updates')
sm = types.KeyboardButton('/subscribe_matches')
um = types.KeyboardButton('/unsubscribe_matches')
sn = types.KeyboardButton('/subscribe_news')
un = types.KeyboardButton('/unsubscribe_news')
mr = types.KeyboardButton('/matches_results')

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) # .add(su,uu,sm, sm, sn, un, mr)

keyboard.row(a, h)
keyboard.row(su, uu)
keyboard.row(sm, sm)
keyboard.row(sn, un, mr)

# start - Quick start
# help - Commands
# subscribe_updates - Subscribe to news updates
# unsubscribe_updates - Unsubscribe from news updates
# subscribe_matches - Subscribe to matches
# unsubscribe_matches - Unsubscribe from matches
# unsubscribe_news - Unsubscribe from news
# matches_results - Get matches result today

async def get_matches(wait_for):
	print("Function \"get_matches\" is working")
	while True:
		await asyncio.sleep(wait_for)
		subscriptions = list(db.get_subscriptions_matches())
		matches = CSGOmatches.get_matches()
		result = ''
		if matches[0]:
			teams = matches[2]['teams']
			tournaments = matches[2]['tournament']
			time = matches[2]['time']
			view = matches[2]['view']
			url_match = matches[2]['url_match']
			url_analitic = matches[2]['url_analitic']

			for i in range(len(teams)):
				team = ' \tVS\t '.join(teams[i].split("|"))
				result =  result + f"Play {team} in {time[i]}\nMatch meta - {view[i]} \nTournament - {tournaments[i]}\nUrl on match - {url_match[i]}\nUrl on analytics - {url_analitic[i]}\n\n"

			for i in range(len(subscriptions)):
				await myapibot.send_message(subscriptions[i][1], f"{matches[1]}\n\n{result}")
	print("Matches is send")

async def get_news(wait_for):
	print("Function \"get_news\" is working")
	while True:
		await asyncio.sleep(wait_for)
		result = []
		subscriptions = list(db.get_subscriptions_news())
		news = CSGOnews.get_news()
		if news[0]:
			for i in range(len(news[2]['name'])):
				result.append(f"{news[1]}\n\n{news[2]['name'][i]}\n\n{news[2]['content'][i]}\nRead more:\n{news[2]['url'][i]}")
			for i in range(len(subscriptions)):
				for a in range(len(result)):
					res = result[a]
					await myapibot.send_message(subscriptions[i][1], res)

async def get_updates(wait_for):
	print("Function \"get_updates\" is working")
	while True:
		await asyncio.sleep(wait_for)
		subscriptions = list(db.get_subscriptions_updates())
		update = CSGOupdate.get_updates()
		if update[0]:
			content = ''
			for i in update[1]['content']:
				content= content + i + "\n\n"
			result = f"{update[1]['name'][0]}\n{update[1]['date'][0]}\n\n{content}Read on blog csgo:\n{update[1]['url']}"
			for i in range(len(subscriptions)):
				await myapibot.send_message(subscriptions[i][1], result)

async def startup(x):
	asyncio.create_task(get_news(10*60))
	asyncio.create_task(get_matches(4*60*60))
	asyncio.create_task(get_updates(2*60*60))

if __name__ == '__main__':
	executor.start_polling(bot, skip_updates=True, on_startup=startup)