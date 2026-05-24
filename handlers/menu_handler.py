from telegram import Update
from telegram.ext import ContextTypes
from database.db_manager import db
from utils.keyboards import category_keyboard, topic_keyboard, pattern_keyboard, topic_options_keyboard, topic_gen_quantity_keyboard
from handlers.practice_handler import start_custom_practice, handle_answer

async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categories = db.get_categories()
    if not categories:
        # If we got here without exception, database is connected but has no categories
        await update.message.reply_text("Database is connected but empty. Please run seed/migration scripts to populate categories.")
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

    elif data.startswith("topic_"):
        # Handle intermediate options for a topic
        parts = data.split('_')
        if len(parts) == 2: # topic_{id}
            topic_id = int(parts[1])
            await query.message.edit_text("Topic Options:", reply_markup=topic_options_keyboard(topic_id))
        elif parts[1] == "gen" and parts[2] == "opts": # topic_gen_opts_{id}
            topic_id = int(parts[3])
            await query.message.edit_text("Select Number of Questions:", reply_markup=topic_gen_quantity_keyboard(topic_id))

    elif data.startswith("show_patterns_"):
        topic_id = int(data.split('_')[2])
        patterns = db.get_patterns(topic_id)
        selected_ids = context.user_data.get('selected_patterns', [])
        await query.message.edit_text("Select Question Patterns:", reply_markup=pattern_keyboard(patterns, selected_ids))

    elif data.startswith("start_topic_gen_"):
        # start_topic_gen_{id}_{count}
        parts = data.split('_')
        topic_id = int(parts[3])
        count = int(parts[4])
        pattern_ids = db.get_all_pattern_ids_for_topic(topic_id)
        
        if not pattern_ids:
            await query.answer("No patterns found for this topic.", show_alert=True)
            return
            
        await start_custom_practice(update, context, pattern_ids, target_count=count)

    elif data.startswith("back_to_cat_from_topic_"):
        topic_id = int(data.split('_')[-1])
        res = db.execute_query("SELECT category_id FROM topics WHERE id = %s", (topic_id,))
        if res:
            topics = db.get_topics(res[0]['category_id'])
            await query.message.edit_text("Select a Topic:", reply_markup=topic_keyboard(topics))
        else:
            categories = db.get_categories()
            await query.message.edit_text("Choose a GMAT category:", reply_markup=category_keyboard(categories))

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

    elif data.startswith("start_random_topic_"):
        topic_id = int(data.split('_')[-1])
        pattern_ids = db.get_all_pattern_ids_for_topic(topic_id)
        
        if not pattern_ids:
            await query.answer("No patterns found for this topic.", show_alert=True)
            return
            
        await start_custom_practice(update, context, pattern_ids)

    elif data.startswith("start_practice_session_"):
        target_count = int(data.split('_')[-1])
        selected_ids = context.user_data.get('selected_patterns', [])
        if not selected_ids:
            await query.answer("Please select at least one pattern.", show_alert=True)
            return
        await start_custom_practice(update, context, selected_ids, target_count=target_count)

    elif data.startswith("retest_session_"):
        target_count = int(data.split('_')[-1])
        selected_ids = context.user_data.get('selected_patterns', [])
        await start_custom_practice(update, context, selected_ids, target_count=target_count)

    elif data == "start_daily_session":
        from handlers.daily_v2_handler import trigger_daily_question
        await trigger_daily_question(update, context)

    elif data.startswith("ans_"):
        await handle_answer(update, context)
