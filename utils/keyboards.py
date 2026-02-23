from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def main_menu_keyboard():
    keyboard = [
        [KeyboardButton("Daily Practice 🕒"), KeyboardButton("Custom Practice 🛠️")],
        [KeyboardButton("Add a topic ➕"), KeyboardButton("My Profile 👤")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def category_keyboard(categories):
    keyboard = []
    for cat in categories:
        keyboard.append([InlineKeyboardButton(cat['name'], callback_data=f"cat_{cat['id']}")])
    return InlineKeyboardMarkup(keyboard)

def topic_keyboard(topics):
    keyboard = []
    for topic in topics:
        keyboard.append([InlineKeyboardButton(topic['name'], callback_data=f"topic_{topic['id']}")])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="back_to_cats")])
    return InlineKeyboardMarkup(keyboard)

def pattern_keyboard(patterns, selected_ids=None):
    if selected_ids is None:
        selected_ids = []
    
    keyboard = []
    for p in patterns:
        is_selected = p['id'] in selected_ids
        btn_text = f"{'✅ ' if is_selected else ''}{p['name']}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"togglepattern_{p['id']}_{patterns[0]['topic_id']}")])
    
    # Selection Controls
    if selected_ids:
        keyboard.append([InlineKeyboardButton("🚀 Generate 20 Questions", callback_data="start_practice_session")])
        keyboard.append([InlineKeyboardButton("➕ Add More Topics", callback_data="back_to_cats")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Topic", callback_data=f"back_to_topics_{patterns[0]['topic_id'] if patterns else ''}")])
    return InlineKeyboardMarkup(keyboard)

def session_complete_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔄 Retest (Same Topics)", callback_data="retest_session")],
        [InlineKeyboardButton("🔍 Reselect Topics", callback_data="back_to_cats")]
    ]
    return InlineKeyboardMarkup(keyboard)

def question_keyboard(options):
    keyboard = []
    labels = ['A', 'B', 'C', 'D', 'E']
    for i, opt in enumerate(options):
        keyboard.append([InlineKeyboardButton(f"{labels[i]}: {opt}", callback_data=f"ans_{i}")])
    return InlineKeyboardMarkup(keyboard)
