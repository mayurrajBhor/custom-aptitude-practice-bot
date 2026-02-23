from telegram import Update
from telegram.ext import ContextTypes
from database.db_manager import db
from utils.keyboards import category_keyboard, topic_keyboard, pattern_keyboard
from handlers.practice_handler import start_custom_practice, handle_answer

async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = db.get_categories()
    if not categories:
        # Fallback if DB is empty or connection fails
        await update.message.reply_text("Database connection issue. Please check your credentials.")
        return
    
    await update.message.reply_text("Choose a GMAT category:", reply_markup=category_keyboard(categories))

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("cat_"):
        cat_id = int(data.split('_')[1])
        topics = db.get_topics(cat_id)
        await query.message.edit_text("Select a Topic:", reply_markup=topic_keyboard(topics))

    elif data == "back_to_cats":
        categories = db.get_categories()
        await query.message.edit_text("Choose a GMAT category:", reply_markup=category_keyboard(categories))

    elif data.startswith("topic_"):
        topic_id = int(data.split('_')[1])
        patterns = db.get_patterns(topic_id)
        selected_ids = context.user_data.get('selected_patterns', [])
        await query.message.edit_text("Select Question Patterns:", reply_markup=pattern_keyboard(patterns, selected_ids))

    elif data.startswith("back_to_topics_"):
        # This needs a bit of logic to get the category_id from the topic_id
        # For simplicity, let's just show categories again or fetch cat_id
        topic_id_str = data.split('_')[-1]
        if topic_id_str:
            res = db.execute_query("SELECT category_id FROM topics WHERE id = %s", (int(topic_id_str),))
            if res:
                topics = db.get_topics(res[0]['category_id'])
                await query.message.edit_text("Select a Topic:", reply_markup=topic_keyboard(topics))
                return
        categories = db.get_categories()
        await query.message.edit_text("Choose a GMAT category:", reply_markup=category_keyboard(categories))

    elif data.startswith("togglepattern_"):
        parts = data.split('_')
        pattern_id = int(parts[1])
        topic_id = int(parts[2])
        
        if 'selected_patterns' not in context.user_data:
            context.user_data['selected_patterns'] = []
        
        if pattern_id in context.user_data['selected_patterns']:
            context.user_data['selected_patterns'].remove(pattern_id)
        else:
            context.user_data['selected_patterns'].append(pattern_id)
            
        patterns = db.get_patterns(topic_id)
        selected_ids = context.user_data['selected_patterns']
        await query.message.edit_text("Select Question Patterns:", reply_markup=pattern_keyboard(patterns, selected_ids))

    elif data == "start_practice_session":
        selected_ids = context.user_data.get('selected_patterns', [])
        if not selected_ids:
            await query.answer("Please select at least one pattern.", show_alert=True)
            return
        await start_custom_practice(update, context, selected_ids)

    elif data == "retest_session":
        selected_ids = context.user_data.get('selected_patterns', [])
        await start_custom_practice(update, context, selected_ids)

    elif data == "start_daily_session":
        from handlers.daily_practice_handler import trigger_daily_question
        await trigger_daily_question(update, context)

    elif data.startswith("ans_"):
        await handle_answer(update, context)
