from telegram import Update
from telegram.ext import ContextTypes
from database.db_manager import db
from llm.generator import generator
from utils.keyboards import question_keyboard, main_menu_keyboard, session_complete_keyboard
import json
import html
import random

async def start_custom_practice(update: Update, context: ContextTypes.DEFAULT_TYPE, pattern_ids: list):
    # Initialize session
    context.user_data['session_patterns'] = pattern_ids
    context.user_data['session_score'] = 0
    context.user_data['session_total_target'] = 5
    context.user_data['session_current_index'] = 0
    context.user_data['question_pool'] = [] # Pool for batched questions
    
    # Selection Summary
    pattern_names = []
    for pid in pattern_ids:
        rows = db.execute_query("SELECT name FROM patterns WHERE id = %s", (pid,))
        if rows:
            pattern_names.append(rows[0]['name'])
    
    summary_text = "📋 <b>Your Selection:</b>\n"
    summary_text += "\n".join([f"• {html.escape(name)}" for name in pattern_names])
    summary_text += f"\n\n🚀 Starting a session of 5 questions!"
    
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id, summary_text, parse_mode='HTML')
        
    await trigger_next_question(update, context)

import time

async def trigger_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_count = context.user_data.get('session_current_index', 0)
    target_count = context.user_data.get('session_total_target', 5)
    
    if current_count >= target_count:
        # Session Complete
        score = context.user_data.get('session_score', 0)
        final_msg = (
            f"🏁 <b>Session Complete!</b>\n\n"
            f"Your Final Score: <b>{score}/{target_count}</b>\n\n"
            f"What would you like to do next?"
        )
        chat_id = update.effective_chat.id
        await context.bot.send_message(chat_id, final_msg, reply_markup=session_complete_keyboard(), parse_mode='HTML')
        return

    # Check question pool
    if not context.user_data.get('question_pool'):
        # Generate batch of 5
        chat_id = update.effective_chat.id
        status_msg = await context.bot.send_message(chat_id, "<i>Generating a batch of questions to speed up your session... ⏳</i>", parse_mode='HTML')
        
        pattern_ids = context.user_data['session_patterns']
        
        # Prepare patterns for the batch (try to be diverse)
        selected_for_batch = []
        if len(pattern_ids) >= 5:
            selected_for_batch = random.sample(pattern_ids, 5)
        else:
            # Cycle through available patterns to fill 5 slots
            selected_for_batch = (pattern_ids * (5 // len(pattern_ids) + 1))[:5]
            
        batch_patterns_info = []
        user_id = update.effective_user.id
        for pid in selected_for_batch:
            res = db.execute_query("SELECT p.id, p.name, p.description, p.difficulty_level, t.name as topic_name FROM patterns p JOIN topics t ON p.topic_id = t.id WHERE p.id = %s", (pid,))
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
        
        questions, error = generator.generate_batch(batch_patterns_info, count=5)
        await status_msg.delete()
        
        if not questions:
            await context.bot.send_message(chat_id, f"❌ <b>Batch Generation Error:</b>\n\n{html.escape(error or 'Empty response')}", parse_mode='HTML')
            return
            
        context.user_data['question_pool'] = questions

    # Get next question from pool
    q_data = context.user_data['question_pool'].pop(0)
    
    # Save to context for answer checking
    context.user_data['current_question'] = q_data
    # Use pattern_id from LLM response if provided, else fallback to random from session
    pattern_id = q_data.get('pattern_id') or random.choice(context.user_data['session_patterns'])
    context.user_data['current_pattern_id'] = pattern_id
    
    safe_question = html.escape(q_data['question_text'])
    safe_options = [html.escape(opt) for opt in q_data['options']]
    
    # Save to DB for uniqueness tracking
    db.save_question(
        pattern_id, 
        q_data['question_text'], 
        q_data['options'], 
        q_data['correct_option_index'], 
        q_data['explanation'], 
        q_data.get('difficulty', 3)
    )

    msg = f"<b>Question {current_count + 1}:</b>\n\n{safe_question}"
    chat_id = update.effective_chat.id
    context.user_data['q_start_time'] = time.time() # Record start time
    await context.bot.send_message(chat_id, msg, reply_markup=question_keyboard(safe_options), parse_mode='HTML')

async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Calculate time taken
    start_time = context.user_data.get('q_start_time', time.time())
    time_taken = time.time() - start_time
    
    user_ans = int(query.data.split('_')[1])
    q_data = context.user_data.get('current_question')
    
    if not q_data:
        await query.message.reply_text("No active question found.")
        return

    is_correct = (user_ans == q_data['correct_option_index'])
    correct_option = q_data['options'][q_data['correct_option_index']]
    
    if is_correct:
        context.user_data['session_score'] += 1
        res_msg = "✅ <b>Correct!</b>"
    else:
        res_msg = f"❌ <b>Incorrect.</b>\n\nCorrect Answer: {html.escape(correct_option)}"
    
    context.user_data['session_current_index'] += 1
    
    # Update DB Progress (SRS)
    db.update_user_progress(
        update.effective_user.id,
        context.user_data['current_pattern_id'],
        is_correct,
        5 if is_correct else 2,
        time_taken=time_taken
    )
    
    explanation = f"\n\n<b>Explanation:</b>\n{html.escape(q_data['explanation'])}"
    time_msg = f"\n\n⏱️ <b>Time taken:</b> {time_taken:.1f}s"
    
    # Send feedback
    try:
        await query.message.edit_text(f"{res_msg}{time_msg}{explanation}", parse_mode='HTML')
    except Exception:
        # Fallback if text is too long or other issues
        await query.message.reply_text(f"{res_msg}{time_msg}{explanation}", parse_mode='HTML')
    
    # Auto trigger next
    if context.user_data.get('is_daily'):
        from handlers.daily_practice_handler import trigger_daily_question
        await trigger_daily_question(update, context)
    else:
        await trigger_next_question(update, context)
