import telebot
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# أدخل رمز الوصول الخاص بالبوت هنا
API_TOKEN = '7396221589:AAE_vtwgnFKgvpEwUbii3RzjVCqypwL4Ibo'
bot = telebot.TeleBot(API_TOKEN)

# تخزين بيانات المستخدمين (بديل عن قاعدة بيانات)
users_data = {}

# هدية يومية
daily_gift_amount = 10
# الحد الأدنى للسحب
min_withdrawal_points = 1000

# التحقق من الهدية اليومية
def can_claim_daily_gift(user_id):
    if user_id in users_data:
        last_claimed = users_data[user_id]['last_claimed']
        if datetime.now() >= last_claimed + timedelta(hours=24):
            return True
    return False

# تسجيل الهدية اليومية
def claim_daily_gift(user_id):
    if user_id not in users_data:
        users_data[user_id] = {'balance': 0, 'last_claimed': datetime.min}
    
    if can_claim_daily_gift(user_id):
        users_data[user_id]['balance'] += daily_gift_amount
        users_data[user_id]['last_claimed'] = datetime.now()
        return True
    return False

# ترحيب بالمستخدم مع الأزرار
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🎁 الهدية اليومية", callback_data="daily_gift"),
        InlineKeyboardButton("👑 دعوة الأصدقاء", callback_data="invite_friends"),
        InlineKeyboardButton("💰 مجموع نقاطي", callback_data="my_points"),
        InlineKeyboardButton("💸 سحب الرصيد", callback_data="withdraw_balance"),
        InlineKeyboardButton("تمت برمجة البوت بواسطة HZ", callback_data="about_bot")
    )
    bot.send_message(user_id, "مرحبًا بك في بوت ربح رصيد آسيا سيل! 🎉\nاختر من الخيارات أدناه:", reply_markup=markup)

# التعامل مع ضغطات الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.message.chat.id
    
    if call.data == "daily_gift":
        if claim_daily_gift(user_id):
            bot.send_message(user_id, f"🎁 لقد حصلت على {daily_gift_amount} رصيد! \nرصيدك الحالي هو {users_data[user_id]['balance']}.")
        else:
            time_left = timedelta(hours=24) - (datetime.now() - users_data[user_id]['last_claimed'])
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            bot.send_message(user_id, f"عذراً، لا يمكنك الحصول على هدية الآن. \nالوقت المتبقي: {hours} ساعة و {minutes} دقيقة.")
    
    elif call.data == "invite_friends":
        referral_link = f"https://t.me/xzzxxz_bot?start={user_id}"
        bot.send_message(user_id, f"👑 دعوة الأصدقاء: شارك هذا الرابط مع أصدقائك للحصول على رصيد إضافي!\n{referral_link}")
    
    elif call.data == "my_points":
        balance = users_data.get(user_id, {}).get('balance', 0)
        bot.send_message(user_id, f"💰 مجموع نقاطك الحالية هو: {balance} نقطة.")
    
    elif call.data == "withdraw_balance":
        balance = users_data.get(user_id, {}).get('balance', 0)
        if balance >= min_withdrawal_points:
            users_data[user_id]['balance'] -= min_withdrawal_points
            bot.send_message(user_id, f"💸 تم سحب {min_withdrawal_points} نقطة. رصيدك المتبقي هو {users_data[user_id]['balance']} نقطة.\nسيتم تحويل الرصيد إلى حسابك خلال 24 ساعة.")
        else:
            bot.send_message(user_id, f"⚠️ عذراً، لا يمكنك سحب الرصيد. الحد الأدنى للسحب هو {min_withdrawal_points} نقطة.")
    
    elif call.data == "about_bot":
        bot.send_message(user_id, "تمت برمجة البوت بواسطة HZ.")

# البدء في تشغيل البوت
bot.polling()
