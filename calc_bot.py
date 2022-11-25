import telebot
import rational_test as rt
import complex as c
import logger as lg
import json

API_TOKEN='' # необходимо вставить токен
bot = telebot.TeleBot(API_TOKEN)

value = ''
value2 = ''

def analytics(func:callable):
    total_messages = 0
    users = set()
    total_users = 0
    def analytics_wrapper(message):
        nonlocal total_messages, total_users
        total_messages += 1

        if message.chat.id not in users:
            users.add(message.chat.id)
            total_users += 1

        BD = ['New message:', message.text, 'Total messages:', total_messages, 'Unique users:', total_users]
        def save():
            with open('BD.json', 'w', encoding='utf-8') as fh:
                fh.write(json.dumps(BD, ensure_ascii=False))
        save()
        return func(message)

    return analytics_wrapper


# cоздам кнопки
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
            telebot.types.InlineKeyboardButton('2', callback_data='2'),
            telebot.types.InlineKeyboardButton('3', callback_data='3'),
            telebot.types.InlineKeyboardButton('+', callback_data='+'))

keyboard.row(telebot.types.InlineKeyboardButton('4', callback_data='4'),
            telebot.types.InlineKeyboardButton('5', callback_data='5'),
            telebot.types.InlineKeyboardButton('6', callback_data='6'),
            telebot.types.InlineKeyboardButton('-', callback_data='-'))

keyboard.row(telebot.types.InlineKeyboardButton('7', callback_data='7'),
            telebot.types.InlineKeyboardButton('8', callback_data='8'),
            telebot.types.InlineKeyboardButton('9', callback_data='9'),
            telebot.types.InlineKeyboardButton('/', callback_data='/'))

keyboard.row(telebot.types.InlineKeyboardButton('0', callback_data='0'),
            telebot.types.InlineKeyboardButton(',', callback_data='.'),
            telebot.types.InlineKeyboardButton('=', callback_data='='),
            telebot.types.InlineKeyboardButton('*', callback_data='*'))

keyboard.row(telebot.types.InlineKeyboardButton('c', callback_data='c'),
            telebot.types.InlineKeyboardButton('j', callback_data='j'),
            telebot.types.InlineKeyboardButton('(', callback_data='('),
            telebot.types.InlineKeyboardButton(')', callback_data=')'))

@bot.message_handler(commands=['start', 'calculater'])
@analytics
def start_message(message):
    global value
    lg.logging.info('The user has selected a command calculater')
    if value == '':
        bot.send_message(message.from_user.id, '0', reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)
           
# обработчик событий, который будет вызван при нажатии на кнопку
@bot.callback_query_handler(func=lambda call:True)
def callback_func(query):
    global value, value2
    data = query.data

    if data == 'no':
       pass
    elif data == 'c':
        value = ''      
    elif data == '=':
        lg.logging.info('The user has selected item = ')
        try:
            if value.count('j') > 0:
                value = c.list_complex(value)
                value = c.calculator(value) 
            else:
                value = rt.get_expression(value)
                value = rt.calculate(value)          
        except:
            value = 'Ошибка!'     
    else:
        value += data         

    if (value != value2 and value != '') or ('0' != value2 and value == '') :
        if value == '':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id =query.message.message_id, text='0', reply_markup=keyboard)    
            value2 = '0'
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id =query.message.message_id, text=value, reply_markup=keyboard)  
            value2 = value

    if value == 'Ошибка!': value =''


bot.polling(none_stop=False, interval=0)