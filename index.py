from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from settings import *
from main import *

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def on_startup(_):
    await bot.send_message(adminId, "<b>бот запущен</b>!")

# /start
@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    i = 0
    for item in users:
        if users[i]['user']['id'] == message['from']['id']:
            count = i
        i += 1
    await message.answer('Этот бот преднозначен для накрутки лайков в таких сетях как\n<b>Instagram</b> и <b>Вконтакте</b>\nОтправьте ссылку для накрутки')
    users[count]['user']['link'] = ''
    users[count]['user']['type'] = ''
    users[count]['user']['message'] = False
    users[count]['user']['char'] = 0

# /prev
@dp.message_handler(commands=['prev'])
async def prev(message: types.Message):
    await message.answer('Введите ссылку')


@dp.message_handler()
async def echo(message: types.Message):
    i = 0
    isTrue = False
    for item in users:
        if users[i]['user']['id'] == message['from']['id']:
            count = i
            isTrue = True
        i += 1

    if isTrue:
        pass
    else:
        users.append({'user': {'id': message['from']['id'], 'link': '', 'message': False, 'type': '', 'char': 0}})
        count = len(users) - 1

    if len(users[count]['user']['link']) == 0:
        if 'https://vk.com' in message.text or 'https://www.instagram.com' in message.text:
            users[count]['user']['link'] = str(message.text)
            await message.answer(f'Укажите что хотите накрутить')
        else:
            await message.answer('Укажите корректную ссылку')
    
    if users[count]['user']['type'] == 'сообщения' and users[count]['user']['message'] == True: 
        temp = 0
        likeValue = users[count]['user']['char']
        await message.answer(f'{temp}/{likeValue}')
        for item in authList:
            isTrue =  auth(item['login'], item['password'], users[count]['user']['link'], users[count]['user']['type'], message.text)
            if isTrue:
                temp += 1
                await message.answer(f'{temp}/{likeValue}')
            else:
                await message.answer(f'error {temp}/{likeValue}')
            if temp == users[count]['user']['char']:
                break
        users[count]['user']['link'] = ''
        users[count]['user']['type'] = ''
        users[count]['user']['message'] = False
        users[count]['user']['char'] = 0
        await message.answer(f'готово')
        

    if len(users[count]['user']['type']) > 0 and users[count]['user']['message'] != True:
        if users[count]['user']['type'] == 'лайки': 
            try:
                users[count]['user']['char'] = int(message.text)
                if 0 < users[count]['user']['char'] <= maxLikesValue:
                    temp = 0
                    likeValue = users[count]['user']['char']
                    await message.answer(f'{temp}/{likeValue}')
                    for item in authList:
                        isTrue = auth(item['login'], item['password'], users[count]['user']['link'], users[count]['user']['type'], '')
                        if isTrue:
                            temp += 1
                            await message.answer(f'{temp}/{likeValue}')
                        else:
                            await message.answer(f'error {temp}/{likeValue}')
                        if temp == users[count]['user']['char']:
                            break
                    users[count]['user']['link'] = ''
                    users[count]['user']['type'] = ''
                    users[count]['user']['char'] = 0

                    await message.answer(f'готово')

                else:
                    await message.answer(f'Недопустимый деапозон')

            except:
                await message.answer('Укажите корректное колличество лайков')

        elif users[count]['user']['type'] == 'сообщения': 
            try:
                users[count]['user']['char'] = int(message.text)
                if 0 < users[count]['user']['char'] <= maxLikesValue:
                    users[count]['user']['message'] = True
                    await message.answer(f'Введите сообщение')

                else:
                    await message.answer(f'Недопустимый деапозон')

            except:
                await message.answer('Укажите корректное колличество сообщений')



    if len(users[count]['user']['link']) > 0 and len(users[count]['user']['type']) == 0:
        if message.text.lower() == 'лайки':
            users[count]['user']['type'] = message.text.lower()
            await message.answer(f'Укажите колличество лайков (до {maxLikesValue} лайков)')
        elif message.text.lower() == 'сообщения':
            users[count]['user']['type'] = message.text.lower()
            await message.answer(f'Укажите колличество сообщений (до {maxLikesValue} сообщений)')
        else: 
            await message.answer(f'<b>лайки</b> или <b>сообщения</b>')

    

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
