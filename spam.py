import asyncio
import random
from pyrogram import Client, filters

# Инициализация юзербота (подставь свои api_id и api_hash)
app = Client("hikka_session", api_id=123456, api_hash="your_api_hash")

# Глобальные переменные управления
spam_active = False
target_group_id = None
message_interval = 180  # Интервал по умолчанию: 3 минуты (180 секунд)
message_limit = 0       # Лимит по умолчанию: 0 (бесконечно)

# База из 170 жестких оскорблений
PHRASES = [
    "ты сын тупой шлюхи", "выблядок ебаный", "мать твою в канаве ебали", "сын мертвой бляди", "гнида конченая",
    "мразь тупорылая", "ублюдок кусок говна", "родители от тебя в ахуе", "потомок сифилитички", "сын подзаборной шалавы",
    "уебище лесное", "хуесос малолетний", "биомусор ебаный", "ошибка абортыша", "выродок тупой",
    "чмо ебаное", "петушара парашная", "шлюхин сын", "укроп ебаный", "говноед конченый",
    "параша ходячая", "отброс общества", "швабра ебаная", "ебанат тупой", "дегенерат конченый",
    "имбецил ебаный", "даун парашный", "овощ тупорылый", "хуесос косоглазый", "глиномес ебаный",
    "петух позорный", "опущенка ебаная", "петушиный хвост", "мать ебал твою", "сестру твою в рот ебал",
    "бабка твоя сдохла в канаве", "родня твоя бомжи ебаные", "отец твой алкаш подзаборный", "семья у тебя шлюх ебаных", "дед твой под шконкой сидел",
    "хуйло ебаное", "пидор конченый", "гандон штопаный", "черт ебаный", "мразь кусок дерьма",
    "гниль ебаная", "тварь подзаборная", "шлюха ты тупорылая", "шмара ебаная", "блядина конченая",
    "потаскуха ебаная", "профурсетка парашная", "шалава тупорылая", "подстилка ментовская", "хуеплет ебаный",
    "пиздобол конченый", "балабол ебаный", "пустозвон тупой", "трепло ебаное", "долбоеб кусок",
    "кретин ебаный", "дебил парашный", "идиот конченый", "тупица ебаная", "баклан тупорылый",
    "лох ебаный", "чмырь парашный", "пёс ебаный", "сука конченая", "тварь дрожащая",
    "выкидыш ебаный", "недоносок тупой", "недоразумение природы", "биоробот ебаный", "npc тупорылый",
    "бот ебаный", "унтерменш ебаный", "недочеловек парашный", "низшая форма жизни", "кусок мяса тупого",
    "говнюк ебаный", "засранец тупой", "вонючка конченая", "чушка ебаная", "чучело огородное",
    "урод моральный", "уродина ебаная", "страшила ебаный", "убожество конченое", "ущерб ебаный",
    "неудачник по жизни", "жизненный тупик", "абсосок ебаный", "выживший после аборта", "залупа конченая",
    "моча ебаная", "кал ходячий", "параша ебаная", "блевотина тупая", "рыготина ебаная",
    "помои конченые", "помойка ходячая", "мусор ебаный", "отстойник тупой", "шлак ебаный",
    "балласт ебаный", "паразит тупорылый", "клещ ебаный", "глист конченый", "острица ебаная",
    "таракан тупой", "клоп ебаный", "вошь парашная", "гнида паршивая", "блоха ебаная",
    "хуета ебаная", "херня конченая", "параша тупая", "срань господня", "хуеплет парашный",
    "петушок комнатный", "маменькин сынок ебаный", "подсос ебаный", "терпила позорный", "лопух тупорылый",
    "фантик ебаный", "пустышка тупая", "ноль без палочки", "место пустое", "никчемыш ебаный",
    "жалкое зрелище", "позорище ебаное", "стыд семьи", "разочарование родителей", "грех презерватива",
    "дырявый ебаный", "очкошник тупой", "трус конченый", "ссыкло ебаное", "тряпка половая",
    "половик тупой", "коврик дверной", "подстилка ебаная", "половая тряпка", "шнурок ебаный",
    "ботинок стоптанный", "носок дырявый", "стелька ебаная", "калоша тупая", "галоша конченая",
    "прокладка ебаная", "тампакс тупой", "бинт грязный", "пластырь ебаный", "тряпка тупая",
    "тряпка помойная", "поломоина ебаная", "помойная крыса", "грязный ублюдок", "вонючий хуесос"
]

@app.on_message(filters.command("setgroup", prefixes="!") & filters.me)
async def set_group(client, message):
    global target_group_id
    try:
        args = message.text.split()
        if len(args) > 1:
            target_group_id = int(args[1])
            await message.edit(f"Целевая группа установлена: {target_group_id}")
        else:
            target_group_id = message.chat.id
            await message.edit(f"Текущая группа установлена как целевая: {target_group_id}")
    except Exception as e:
        await message.edit(f"Ошибка установки группы: {e}")

@app.on_message(filters.command("setlimit", prefixes="!") & filters.me)
async def set_limit(client, message):
    global message_limit
    try:
        args = message.text.split()
        message_limit = int(args[1])
        await message.edit(f"Лимит сообщений установлен: {message_limit}")
    except Exception:
        await message.edit("Использование: !setlimit [число]")

@app.on_message(filters.command("setdelay", prefixes="!") & filters.me)
async def set_delay(client, message):
    global message_interval
    try:
        args = message.text.split()
        message_interval = int(args[1])
        await message.edit(f"Интервал между сообщениями установлен: {message_interval} секунд")
    except Exception:
        await message.edit("Использование: !setdelay [секунды]")

@app.on_message(filters.command("startspam", prefixes="!") & filters.me)
async def start_spam(client, message):
    global spam_active, target_group_id
    
    if target_group_id is None:
        target_group_id = message.chat.id
        
    if spam_active:
        await message.edit("Спам уже запущен.")
        return
    
    spam_active = True
    await message.edit(f"Спам запущен в группе {target_group_id}. Лимит: {message_limit if message_limit > 0 else '∞'}. Интервал: {message_interval}с.")
    
    sent_count = 0
    try:
        while spam_active:
            if message_limit > 0 and sent_count >= message_limit:
                spam_active = False
                await client.send_message(target_group_id, "Лимит сообщений исчерпан. Спам завершен.")
                break

            phrase = random.choice(PHRASES)
            await client.send_message(target_group_id, phrase)
            sent_count += 1
            
            for _ in range(message_interval):
                if not spam_active:
                    break
                await asyncio.sleep(1)
                
    except Exception as e:
        print(f"Ошибка в спам-цикле: {e}")
        spam_active = False

@app.on_message(filters.command("stopspam", prefixes="!") & filters.me)
async def stop_spam(client, message):
    global spam_active
    spam_active = False
    await message.edit("Спам остановлен.")

@app.on_message(filters.command("spamhelp", prefixes="!") & filters.me)
async def spam_help(client, message):
    help_text = (
        "Команды управления спамом:\n"
        "!setgroup [ID] - задать чат для спама\n"
        "!setlimit [число] - лимит сообщений (0 = ∞)\n"
        "!setdelay [секунды] - интервал задержки\n"
        "!startspam - запустить рассылку\n"
        "!stopspam - остановить рассылку"
    )
    await message.edit(help_text)

app.run()
  
