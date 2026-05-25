import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

def main_menu_keyboard():
    web_app_url = os.getenv("WEB_APP_URL")
    keyboard = [
        [KeyboardButton("Daily Practice 🕒"), KeyboardButton("Custom Practice 🛠️")],
        [KeyboardButton("Add a topic ➕"), KeyboardButton("My Profile 👤")]
    ]
    if web_app_url:
        keyboard.insert(0, [KeyboardButton("Open Practice App", web_app=WebAppInfo(web_app_url))])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def category_keyboard(categories):
    keyboard = []
    for cat in categories:
        keyboard.append([InlineKeyboardButton(cat['name'], callback_data=f"cat_{cat['id']}")])
    return InlineKeyboardMarkup(keyboard)

def topic_options_keyboard(topic_id):
    keyboard = [
        [InlineKeyboardButton("🚀 Generate Questions", callback_data=f"topic_gen_opts_{topic_id}")],
        [InlineKeyboardButton("📂 See Patterns", callback_data=f"show_patterns_{topic_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data=f"back_to_cat_from_topic_{topic_id}")]
    ]
    return InlineKeyboardMarkup(keyboard)

def topic_gen_quantity_keyboard(topic_id):
    keyboard = [
        [InlineKeyboardButton("5 Questions", callback_data=f"start_topic_gen_{topic_id}_5")],
        [InlineKeyboardButton("10 Questions", callback_data=f"start_topic_gen_{topic_id}_10")],
        [InlineKeyboardButton("20 Questions", callback_data=f"start_topic_gen_{topic_id}_20")],
        [InlineKeyboardButton("🔙 Back", callback_data=f"topic_{topic_id}")]
    ]
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
    
    # Add Random/All Patterns button at the top
    if patterns:
        topic_id = patterns[0]['topic_id']
        keyboard.append([InlineKeyboardButton("🔀 Any Pattern (Random Mixed)", callback_data=f"start_random_topic_{topic_id}")])

    for p in patterns:
        is_selected = p['id'] in selected_ids
        btn_text = f"{'✅ ' if is_selected else ''}{p['name']}"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"togglepattern_{p['id']}_{patterns[0]['topic_id']}")])
    
    # Selection Controls
    if selected_ids:
        keyboard.append([InlineKeyboardButton("🚀 Generate 5 Questions", callback_data="start_practice_session_5")])
        keyboard.append([InlineKeyboardButton("🚀 Generate 10 Questions", callback_data="start_practice_session_10")])
        keyboard.append([InlineKeyboardButton("🚀 Generate 20 Questions", callback_data="start_practice_session_20")])
        keyboard.append([InlineKeyboardButton("➕ Add More Topics", callback_data="back_to_cats")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Topic", callback_data=f"back_to_topics_{patterns[0]['topic_id'] if patterns else ''}")])
    return InlineKeyboardMarkup(keyboard)

def session_complete_keyboard(target_count=20):
    keyboard = [
        [InlineKeyboardButton("🔄 Retest (Same Topics)", callback_data=f"retest_session_{target_count}")],
        [InlineKeyboardButton("🔍 Reselect Topics", callback_data="back_to_cats")]
    ]
    return InlineKeyboardMarkup(keyboard)

def question_keyboard(options):
    keyboard = []
    labels = [chr(ord('A') + i) for i in range(len(options))]
    
    # Process options in chunks of 2 for a 2x2 grid
    for i in range(0, len(options), 2):
        row = []
        for j in range(i, min(i + 2, len(options))):
            row.append(InlineKeyboardButton(f"{labels[j]}: {options[j]}", callback_data=f"ans_{j}"))
        keyboard.append(row)
        
    return InlineKeyboardMarkup(keyboard)
