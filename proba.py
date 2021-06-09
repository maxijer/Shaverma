from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN, first_phrase, star_option
from callback_datas_2 import shaverma_callback, choice_callback, full_itog
from vse_chto_nuzhno import Shaverma

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def get_inline_keyboard(call_type, list_of_values, star, location):
    inline_keyboard = InlineKeyboardMarkup(row_width=1)
    count = 0
    for value in list_of_values:
        count += 1
        if call_type == 1:
            inline_keyboard.insert(InlineKeyboardButton(text=value, callback_data=shaverma_callback.new(star=count)))
        elif call_type == 2:
            inline_keyboard.insert(
                InlineKeyboardButton(text=value[1], callback_data=choice_callback.new(name=value[1], star=star)))
    if call_type == 2:
        inline_keyboard.insert(
            InlineKeyboardButton(text="Назад", callback_data=choice_callback.new(name="Назад", star=star)))
        inline_keyboard.insert(
            InlineKeyboardButton(text="Отмена", callback_data=choice_callback.new(name="Отмена", star=star)))
    elif call_type == 3:
        inline_keyboard.insert(
            InlineKeyboardButton(text="Показать локацию", callback_data=full_itog.new(location=location, star=star)))
        inline_keyboard.insert(
            InlineKeyboardButton(text="Назад", callback_data=full_itog.new(location="Назад", star=star)))
        inline_keyboard.insert(
            InlineKeyboardButton(text="Отмена", callback_data=full_itog.new(location="Отмена", star=star)))
    return inline_keyboard


def get_choice_keyboard(data):
    shava = Shaverma("main.db")
    list_of_values = shava.get_all_in_this_level(int(data))
    new_keyboard = get_inline_keyboard(2, list_of_values, int(data), None)
    return new_keyboard


@dp.callback_query_handler()
async def go_callback(call: CallbackQuery):
    data = str(call.data).split(":")
    type_of_callback = data[0]
    value = data[1]
    if type_of_callback == "shaverma":
        await call.message.edit_text("Вот, что я могу тебе предложить", reply_markup=get_choice_keyboard(value))
    elif type_of_callback == "you_choice":
        if value == "Назад":
            star_keyboard = get_inline_keyboard(1, star_option, 0, None)
            await call.message.edit_text("На что ты готов ради этого?", reply_markup=star_keyboard)
        elif value == "Отмена":
            await call.message.edit_text("Я сделал всё, что смог", reply_markup=None)
        else:
            shav = Shaverma("main.db")
            list_of_val = shav.get_by_name(value)
            new_keyboard = get_inline_keyboard(3, [], str(list_of_val[0][0]), str(list_of_val[0][-1]))
            await call.message.delete()
            await call.message.answer_photo(photo=list_of_val[0][-2], caption=list_of_val[0][2],
                                            reply_markup=new_keyboard)
    else:
        if str(data[2]) == "Назад":
            await call.message.delete()
            await call.message.answer("Тогда вот, что вам подойдёт", reply_markup=choice_callback(data[1]))
        elif str(data[2]) == "Отмена":
            await call.message.delete()
            await call.message.answer("Я сделал всё, что смог", reply_markup=None)
        else:
            await call.message.delete()
            await call.message.answer_location(float(str(data[2]).split()[0]), float(str(data[2]).split()[1]),
                                               reply_markup=None)


@dp.message_handler(content_types=["location"])
async def get_location(message: types.Message):
    print(message.location.latitude)
    print(message.location.longitude)
    star_keyboard = get_inline_keyboard(1, star_option, 0, None)
    await bot.send_message(message.from_user.id, "На что ты готов ради этого?", reply_markup=star_keyboard)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup()
    shaverma = KeyboardButton("Хочу шаверму", request_location=True)
    keyboard.insert(shaverma)
    await bot.send_message(message.from_user.id, first_phrase, reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp)
