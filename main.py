from aiogram import types, Bot, Dispatcher, executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from callback_datas import shaverma_callback, full_callback, pokaz_callback
from vse_chto_nuzhno import Shaverma

TOKEN = "1805292951:AAG-Zwvy4vyXoPBLulQ3qrBbG1lYIslXyRc"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def get_inline_keyboard(call_type, list_of_values, what, location):
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    count = 0
    for i in list_of_values:
        count += 1
        if call_type == 1:
            inline_keyboard.insert(InlineKeyboardButton(text=i, callback_data=shaverma_callback.new(what=count)))
        elif call_type == 2:
            inline_keyboard.insert(
                InlineKeyboardButton(text=i[1], callback_data=full_callback.new(list_of_choice=i[1], what=what)))
    if call_type == 3:
        inline_keyboard.insert(
            InlineKeyboardButton(text="Посмотреть локацию",
                                 callback_data=pokaz_callback.new(location=str(location), what=what)))
        inline_keyboard.insert(
            InlineKeyboardButton(text="Назад", callback_data=pokaz_callback.new(location="Назад", what=what)))
        inline_keyboard.insert(
            InlineKeyboardButton(text="Отмена", callback_data=pokaz_callback.new(location="Отмена", what=what)))
    if call_type == 2:
        inline_keyboard.insert(
            InlineKeyboardButton(text="Назад", callback_data=full_callback.new(list_of_choice="Назад", what=what)))
        inline_keyboard.insert(
            InlineKeyboardButton(text="Отмена", callback_data=full_callback.new(list_of_choice="Отмена", what=what)))
    return inline_keyboard


def get_2_key(data):
    shava = Shaverma("main.db")
    list_of_values = shava.get_all_in_this_level(int(data))
    new_keyboard = get_inline_keyboard(2, list_of_values, int(data), None)
    print(new_keyboard)
    return new_keyboard


@dp.callback_query_handler()
async def callback_ret(call: CallbackQuery):
    data = str(call.data).split(":")
    print(data)
    if data[0] == "shaverma":
        await call.message.edit_text("Тогда вот, что вам подойдёт", reply_markup=get_2_key(data[1]))
    elif data[0] == "you_choice":
        if data[1] == "Назад":
            inline_keyboard = get_inline_keyboard(1,
                                                  ["Готов отравиться", "Хочу новых ощущений", "Пойдёт средняя шаурма",
                                                   "Я ем только достойную шаурму",
                                                   "Я человек высоких нравов и хочу съесть лучшую шаверму в этом городе"],
                                                  0, None)
            await call.message.edit_text("Каков твой выбор?", reply_markup=inline_keyboard)
        elif data[1] == "Отмена":
            await call.message.edit_text("Я сделал всё, что смог.", reply_markup=None)
        else:
            shav = Shaverma("main.db")
            list_of_val = shav.get_by_name(data[1])
            new_inline_keyboard = get_inline_keyboard(3, [], str(list_of_val[0][0]), str(list_of_val[0][-1]))
            await call.message.delete()
            await call.message.answer_photo(photo=list_of_val[0][-2], caption=list_of_val[0][2],
                                            reply_markup=new_inline_keyboard)
    else:
        if data[1] == "Назад":
            await call.message.delete()
            await call.message.answer("Тогда вот, что вам подойдёт", reply_markup=get_2_key(data[2]))
        elif data[1] == "Отмена":
            await call.message.delete()
            await call.message.answer("Я сделал всё, что смог.", reply_markup=None)
        else:
            await call.message.delete()
            await call.message.answer_location(float(data[1].split()[0]), float(data[1].split()[1]), reply_markup=None)


@dp.message_handler(content_types=["location"])
async def go_shav(message: types.Message):
    print(message.location.latitude)
    print(message.location.longitude)
    inline_keyboard = get_inline_keyboard(1, ["Готов отравиться", "Хочу новых ощущений", "Пойдёт средняя шаурма",
                                              "Я ем только достойную шаурму",
                                              "Я человек высоких нравов и хочу съесть лучшую шаверму в этом городе"], 0,
                                          None)
    await bot.send_message(message.from_user.id, "Каков твой выбор?", reply_markup=inline_keyboard)


@dp.message_handler(commands=["start", "shaverma"])
async def start(message: types.Message):
    print(message.from_user.id)
    klava = ReplyKeyboardMarkup()
    knopka = KeyboardButton("Хочу шаверму", request_location=True)
    klava.add(knopka)
    await bot.send_message(message.from_user.id,
                           "Я готов помочь тебе сделать правильный выбор, брат мой меньший, чего ты хочешь?",
                           reply_markup=klava)

#
# async def shedule():
#     await bot.send_message("896895871", "1")
#

if __name__ == '__main__':
    # dp._loop_create_task(shedule())
    executor.start_polling(dp)
