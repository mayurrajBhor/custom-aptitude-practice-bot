from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_manager import db
from llm.generator import generator
from utils.keyboards import question_keyboard
import random
import html
import time
import asyncio

async def start_daily_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # 1. Fetch 9-Day New Patterns
    new_patterns = db.get_new_patterns_in_cycle(user_id)
    # 2. Fetch SRS Due Patterns
    srs_patterns = db.get_srs_due_patterns(user_id)
    
    if not new_patterns and not srs_patterns:
        await update.message.reply_text("✨ <b>Your Daily Practice is clear!</b>\n\nGo to 'Custom Practice' to add more topics or wait for your SRS reviews to become due.", parse_mode='HTML')
        return

    # 3. Build the Plan & Queue
    queue = []
    plan_text = "📅 <b>Your Daily Practice Plan</b>\n\n"
    
    if new_patterns:
        plan_text += "🆕 <b>9-Day New Topics:</b>\n"
        for p in new_patterns:
            # Logic: Easy (1-2) -> 2, Medium (3) -> 3, Hard (4-5) -> 4
            difficulty = p['difficulty_level']
            count = 2
            if difficulty == 3: count = 3
            elif difficulty >= 4: count = 4
            
            plan_text += f"• {html.escape(p['name'])}: {count} questions\n"
            for _ in range(count):
                queue.append(p['id'])
    
    if srs_patterns:
        if new_patterns: plan_text += "\n"
        plan_text += "🧠 <b>SRS Review Topics:</b>\n"
        for p in srs_patterns:
            # For SRS, we'll do 1 question per due topic to cover more ground
            plan_text += f"• {html.escape(p['name'])}: 1 question\n"
            queue.append(p['id'])
            
    plan_text += f"\nTotal Questions: <b>{len(queue)}</b>"
    
    # Store in context
    context.user_data['daily_queue'] = queue
    context.user_data['session_score'] = 0
    context.user_data['session_total_target'] = len(queue)
    context.user_data['session_current_index'] = 0
    # Clear any existing pools to ensure the new flat format is used
    context.user_data['daily_pool'] = []
    context.user_data['custom_pool'] = []
    context.user_data['is_daily'] = True
    
    keyboard = [[InlineKeyboardButton("Start Practice 🚀", callback_data="start_daily_session")]]
    await update.message.reply_text(plan_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def _fill_daily_pool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Helper to fill the daily question pool in background or foreground."""
    queue = context.user_data.get('daily_queue', [])
    if not queue:
        return True, None # Nothing to fill
        
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    batch_size = min(5, len(queue))
    selected_for_batch = [queue.pop(0) for _ in range(batch_size)]
    context.user_data['daily_queue'] = queue
    
    batch_patterns_info = []
    for pid in selected_for_batch:
        res = db.execute_query("SELECT p.id, p.name, p.description, t.name as topic_name FROM patterns p JOIN topics t ON p.topic_id = t.id WHERE p.id = %s", (pid,))
        if res:
            p = res[0]
            current_diff = db.get_current_difficulty(user_id, pid)
            batch_patterns_info.append({
                'id': p['id'],
                'name': p['name'],
                'topic_name': p['topic_name'],
                'description': p['description'],
                'difficulty': current_diff,
                'avoid_questions': db.get_recent_questions(p['id'])
            })

    questions, error_msg = generator.generate_batch(batch_patterns_info, count=batch_size)
    if not questions:
        # Put items back in queue if generation failed
        context.user_data['daily_queue'] = selected_for_batch + context.user_data['daily_queue']
        return False, error_msg
        
    pool = context.user_data.get('daily_pool', [])
    for q in questions:
        p_id = q.get('pattern_id') or selected_for_batch[0]
        db.save_question(
            p_id,
            q['question_text'],
            q['options'],
            q['correct_option_index'],
            q['explanation'],
            q.get('difficulty', 3)
        )
        # Add the question directly without wrapping it in a 'data' key
        pool.append(q)
    context.user_data['daily_pool'] = pool
    return True, None

async def trigger_daily_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("!!! TRACE ATTEMPT: trigger_daily_question in V2 HANDLER called !!!")
    queue = context.user_data.get('daily_queue', [])
    pool = context.user_data.get('daily_pool', [])
    total = context.user_data.get('session_total_target', 0)
    current_idx = context.user_data.get('session_current_index', 0) + 1
    
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    print(f"DEBUG: trigger_daily_question. Queue: {len(queue)}, Pool: {len(pool)}")

    if not pool and not queue:
        # Session Complete
        score = context.user_data.get('session_score', 0)
        await context.bot.send_message(
            chat_id,
            f"🏁 <b>Daily Practice Complete!</b>\n\nScore: <b>{score}/{total}</b>\nBoom! You're getting better every day. 🔥",
            parse_mode='HTML'
        )
        context.user_data['is_daily'] = False
        return

    # If pool is empty, generate a batch synchronously
    if not pool:
        status_msg = await context.bot.send_message(chat_id, f"<i>Batch generating {min(5, len(queue))} questions... ⏳</i>", parse_mode='HTML')
        success, error_msg = await _fill_daily_pool(update, context)
        await status_msg.delete()

        if not success:
            await context.bot.send_message(chat_id, f"❌ <b>Batch Generation Failed:</b>\n\n{html.escape(str(error_msg) or 'Unknown Error')}", parse_mode='HTML')
            return
        
        pool = context.user_data.get('daily_pool', [])

    # Serve from pool
    q_data = pool.pop(0)
    context.user_data['daily_pool'] = pool
    pattern_id = q_data.get('pattern_id')

    # PREFETCH: If pool is now empty but more items in queue, start fetching next batch
    if not pool and context.user_data.get('daily_queue'):
        print("DEBUG: Prefetching next daily batch in background...")
        asyncio.create_task(_fill_daily_pool(update, context))

    context.user_data['current_question'] = q_data
    context.user_data['current_pattern_id'] = pattern_id
    context.user_data['q_start_time'] = time.time()
    
    safe_question = html.escape(q_data['question_text'])
    safe_options = [html.escape(opt) for opt in q_data['options']]
    
    msg = f"<b>Question {current_idx}/{total}:</b>\n\n{safe_question}"
    await context.bot.send_message(chat_id, msg, reply_markup=question_keyboard(safe_options), parse_mode='HTML')
