import os
import logging
import requests
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands=['chachong'])
async def chachong(message: types.Message):
	url = 'https://api.asoulcnki.asia/main/v1/check'
	# 切割, 合并
	msg = message.text.split(" ")
	if len(msg) == 1:
		await message.reply("没有要查重的小作文")
	text = " ".join(msg[1:])
	# 判断输入字数
	if len(text) < 10:
		await message.reply("小作文至少10个字符")

	result = requests.post(url, json={"text": text})
	print(result.json())
	rate = str(float(result.json()['data']['related'][0]['rate']) * 100) + "%"		# 重复率
	originCommentURL = result.json()['data']['related'][0]['reply_url']		# 原偷/原创链接
	originComment = result.json()['data']['related'][0]['reply']['content']		# 原文
	originCommentWriter = result.json()['data']['related'][0]['reply']['m_name']		# 昵称
	toSend = "枝网文本复制检测报告(简洁)\n总文字复制比: {}\n相似小作文: {}\n作者: {}\n原文链接: {}\n\n查重结果仅作参考，请注意辨别是否为原创".format(rate, originComment, originCommentWriter, originCommentURL)
	await message.reply(toSend)


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
