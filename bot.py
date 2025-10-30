import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import random
from datetime import datetime
import certifi

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
MONGO_URI = os.environ.get('MONGO_URI')
CHANNEL_ID = os.environ.get('PRIVATE_CHANNEL_ID')

client = MongoClient(
    MONGO_URI,
    server_api=ServerApi('1'),
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    socketTimeoutMS=10000
)

try:
    client.admin.command('ping')
    logger.info("MongoDB connection successful!")
except Exception as e:
    logger.error(f"MongoDB connection failed: {e}")
    raise

db = client['telegram_file_bot']
files_collection = db['files']
users_collection = db['users']

files_collection.create_index('unique_id', unique=True)
users_collection.create_index('user_id', unique=True)

LANGUAGES = {
    'en': {
        'name': '🇬🇧 English',
        'welcome': '👋 Welcome, {}! 🌸\n\n✨ I am your personal file manager bot.\n\n📁 Send me any file and I will:\n• Forward it to a secure channel\n• Generate a unique 9-digit ID\n• Let you retrieve it anytime with /file <id>\n\n🚀 Fast, secure, and always available!',
        'file_saved': '✅ File saved successfully!\n\n🆔 Your unique ID: `{}`\n\n📥 Use /file {} to retrieve it anytime.',
        'file_not_found': '❌ File not found with ID: {}',
        'file_retrieved': '📥 Here is your file (ID: {}).',
        'send_file': '📁 Please send me a file to save.',
        'choose_language': '🌍 Please choose your language:',
        'language_set': '✅ Language set to English!'
    },
    'he': {
        'name': '🇮🇱 עברית',
        'welcome': '👋 ברוך הבא, {}! 🌸\n\n✨ אני בוט ניהול הקבצים האישי שלך.\n\n📁 שלח לי כל קובץ ואני:\n• אעביר אותו לערוץ מאובטח\n• אייצר מזהה ייחודי בן 9 ספרות\n• אאפשר לך לשלוף אותו בכל זמן עם /file <id>\n\n🚀 מהיר, מאובטח ותמיד זמין!',
        'file_saved': '✅ הקובץ נשמר בהצלחה!\n\n🆔 המזהה הייחודי שלך: `{}`\n\n📥 השתמש ב-/file {} כדי לשלוף אותו בכל זמן.',
        'file_not_found': '❌ קובץ לא נמצא עם מזהה: {}',
        'file_retrieved': '📥 הנה הקובץ שלך (מזהה: {}).',
        'send_file': '📁 אנא שלח לי קובץ לשמירה.',
        'choose_language': '🌍 בחר את השפה שלך:',
        'language_set': '✅ השפה הוגדרה לעברית!'
    },
    'es': {
        'name': '🇪🇸 Español',
        'welcome': '👋 ¡Bienvenido, {}! 🌸\n\n✨ Soy tu bot personal de gestión de archivos.\n\n📁 Envíame cualquier archivo y yo:\n• Lo reenviaré a un canal seguro\n• Generaré una ID única de 9 dígitos\n• Te permitiré recuperarlo en cualquier momento con /file <id>\n\n🚀 ¡Rápido, seguro y siempre disponible!',
        'file_saved': '✅ ¡Archivo guardado con éxito!\n\n🆔 Tu ID único: `{}`\n\n📥 Usa /file {} para recuperarlo en cualquier momento.',
        'file_not_found': '❌ Archivo no encontrado con ID: {}',
        'file_retrieved': '📥 Aquí está tu archivo (ID: {}).',
        'send_file': '📁 Por favor envíame un archivo para guardar.',
        'choose_language': '🌍 Por favor elige tu idioma:',
        'language_set': '✅ ¡Idioma establecido en Español!'
    },
    'ko': {
        'name': '🇰🇷 한국어',
        'welcome': '👋 환영합니다, {}님! 🌸\n\n✨ 저는 당신의 개인 파일 관리 봇입니다.\n\n📁 파일을 보내주시면:\n• 안전한 채널로 전달합니다\n• 고유한 9자리 ID를 생성합니다\n• /file <id>로 언제든지 검색할 수 있습니다\n\n🚀 빠르고 안전하며 항상 사용 가능합니다!',
        'file_saved': '✅ 파일이 성공적으로 저장되었습니다!\n\n🆔 고유 ID: `{}`\n\n📥 언제든지 /file {}로 검색하세요.',
        'file_not_found': '❌ ID로 파일을 찾을 수 없습니다: {}',
        'file_retrieved': '📥 파일입니다 (ID: {}).',
        'send_file': '📁 저장할 파일을 보내주세요.',
        'choose_language': '🌍 언어를 선택하세요:',
        'language_set': '✅ 언어가 한국어로 설정되었습니다!'
    },
    'fr': {
        'name': '🇫🇷 Français',
        'welcome': '👋 Bienvenue, {} ! 🌸\n\n✨ Je suis votre bot personnel de gestion de fichiers.\n\n📁 Envoyez-moi un fichier et je vais :\n• Le transférer vers un canal sécurisé\n• Générer un ID unique à 9 chiffres\n• Vous permettre de le récupérer à tout moment avec /file <id>\n\n🚀 Rapide, sécurisé et toujours disponible !',
        'file_saved': '✅ Fichier enregistré avec succès !\n\n🆔 Votre ID unique : `{}`\n\n📥 Utilisez /file {} pour le récupérer à tout moment.',
        'file_not_found': '❌ Fichier introuvable avec l\'ID : {}',
        'file_retrieved': '📥 Voici votre fichier (ID : {}).',
        'send_file': '📁 Veuillez m\'envoyer un fichier à enregistrer.',
        'choose_language': '🌍 Veuillez choisir votre langue :',
        'language_set': '✅ Langue définie en Français !'
    },
    'zh': {
        'name': '🇨🇳 中文',
        'welcome': '👋 欢迎，{}！🌸\n\n✨ 我是您的个人文件管理机器人。\n\n📁 发送任何文件给我，我将：\n• 将其转发到安全频道\n• 生成唯一的9位数字ID\n• 让您随时使用 /file <id> 检索它\n\n🚀 快速、安全、随时可用！',
        'file_saved': '✅ 文件保存成功！\n\n🆔 您的唯一ID：`{}`\n\n📥 随时使用 /file {} 检索它。',
        'file_not_found': '❌ 未找到ID为 {} 的文件',
        'file_retrieved': '📥 这是您的文件（ID：{}）。',
        'send_file': '📁 请发送文件给我保存。',
        'choose_language': '🌍 请选择您的语言：',
        'language_set': '✅ 语言已设置为中文！'
    }
}

def generate_unique_id():
    while True:
        unique_id = str(random.randint(100000000, 999999999))
        if not files_collection.find_one({'unique_id': unique_id}):
            return unique_id

def get_user_language(user_id):
    user = users_collection.find_one({'user_id': user.id})
    return user.get('language', 'en') if user else 'en'

def get_text(user_id, key):
    lang = get_user_language(user_id)
    return LANGUAGES[lang].get(key, LANGUAGES['en'][key])

def get_channel_identifier():
    channel = CHANNEL_ID.strip()
    if channel.startswith('@'):
        return channel
    elif channel.startswith('-100'):
        return int(channel)
    else:
        try:
            return int(channel)
        except ValueError:
            return channel

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    existing_user = users_collection.find_one({'user_id': user.id})
    
    if existing_user and 'language' in existing_user:
        await send_welcome(update, context)
    else:
        keyboard = [
            [InlineKeyboardButton(LANGUAGES['en']['name'], callback_data='lang_en'),
             InlineKeyboardButton(LANGUAGES['he']['name'], callback_data='lang_he')],
            [InlineKeyboardButton(LANGUAGES['es']['name'], callback_data='lang_es'),
             InlineKeyboardButton(LANGUAGES['ko']['name'], callback_data='lang_ko')],
            [InlineKeyboardButton(LANGUAGES['fr']['name'], callback_data='lang_fr'),
             InlineKeyboardButton(LANGUAGES['zh']['name'], callback_data='lang_zh')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            '🌍 Please choose your language:\n请选择您的语言\nבחר את השפה שלך\nChoisissez votre langue\n언어를 선택하세요\nElige tu idioma',
            reply_markup=reply_markup
        )

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    language = query.data.split('_')[1]
    
    users_collection.update_one(
        {'user_id': user.id},
        {'$set': {
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'language': language,
            'created_at': datetime.utcnow()
        }},
        upsert=True
    )
    
    await query.edit_message_text(get_text(user.id, 'language_set'))
    await send_welcome_after_lang(update, context)

async def send_welcome_after_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    
    welcome_text = get_text(user.id, 'welcome').format(user.first_name)
    
    await context.bot.send_message(
        chat_id=user.id,
        text=welcome_text
    )
    
    try:
        await context.bot.forward_message(
            chat_id=user.id,
            from_chat_id='@sourceui',
            message_id=5
        )
    except Exception as e:
        logger.error(f"Could not forward welcome video: {e}")

async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = get_text(user.id, 'welcome').format(user.first_name)
    
    await update.message.reply_text(welcome_text)
    
    try:
        await context.bot.forward_message(
            chat_id=user.id,
            from_chat_id='@sourceui',
            message_id=5
        )
    except Exception as e:
        logger.error(f"Could not forward welcome video: {e}")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message
    
    file_id = None
    file_type = None
    file_name = None
    file_size = None
    
    if message.document:
        file_id = message.document.file_id
        file_type = 'document'
        file_name = message.document.file_name
        file_size = message.document.file_size
    elif message.photo:
        file_id = message.photo[-1].file_id
        file_type = 'photo'
        file_size = message.photo[-1].file_size
    elif message.video:
        file_id = message.video.file_id
        file_type = 'video'
        file_name = message.video.file_name if hasattr(message.video, 'file_name') else None
        file_size = message.video.file_size
    elif message.audio:
        file_id = message.audio.file_id
        file_type = 'audio'
        file_name = message.audio.file_name if hasattr(message.audio, 'file_name') else None
        file_size = message.audio.file_size
    elif message.voice:
        file_id = message.voice.file_id
        file_type = 'voice'
        file_size = message.voice.file_size
    elif message.video_note:
        file_id = message.video_note.file_id
        file_type = 'video_note'
        file_size = message.video_note.file_size
    elif message.animation:
        file_id = message.animation.file_id
        file_type = 'animation'
        file_name = message.animation.file_name if hasattr(message.animation, 'file_name') else None
        file_size = message.animation.file_size
    elif message.sticker:
        file_id = message.sticker.file_id
        file_type = 'sticker'
        file_size = message.sticker.file_size
    
    if not file_id:
        await message.reply_text(get_text(user.id, 'send_file'))
        return
    
    try:
        channel_identifier = get_channel_identifier()
        
        forwarded = await context.bot.forward_message(
            chat_id=channel_identifier,
            from_chat_id=message.chat_id,
            message_id=message.message_id
        )
        
        unique_id = generate_unique_id()
        
        files_collection.insert_one({
            'unique_id': unique_id,
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'file_id': file_id,
            'file_type': file_type,
            'file_name': file_name,
            'file_size': file_size,
            'channel_message_id': forwarded.message_id,
            'original_message_id': message.message_id,
            'created_at': datetime.utcnow()
        })
        
        confirmation_text = get_text(user.id, 'file_saved').format(unique_id, unique_id)
        await message.reply_text(confirmation_text, parse_mode='Markdown')
        
        logger.info(f"File {unique_id} saved for user {user.id}")
        
    except Exception as e:
        logger.error(f"Error handling file: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")

async def get_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if not context.args:
        await update.message.reply_text(get_text(user.id, 'send_file'))
        return
    
    unique_id = context.args[0]
    
    file_data = files_collection.find_one({'unique_id': unique_id})
    
    if not file_data:
        await update.message.reply_text(get_text(user.id, 'file_not_found').format(unique_id))
        return
    
    try:
        channel_identifier = get_channel_identifier()
        
        await context.bot.forward_message(
            chat_id=user.id,
            from_chat_id=channel_identifier,
            message_id=file_data['channel_message_id']
        )
        
        await update.message.reply_text(get_text(user.id, 'file_retrieved').format(unique_id))
        logger.info(f"File {unique_id} retrieved by user {user.id}")
        
    except Exception as e:
        logger.error(f"Error retrieving file: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("file", get_file))
    application.add_handler(CallbackQueryHandler(language_callback, pattern='^lang_'))
    application.add_handler(MessageHandler(
        filters.Document.ALL | filters.PHOTO | filters.VIDEO | 
        filters.AUDIO | filters.VOICE | filters.VIDEO_NOTE | 
        filters.ANIMATION | filters.Sticker.ALL,
        handle_file
    ))
    
    logger.info("Bot started successfully on Heroku Standard-2X dyno with stack-24")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
