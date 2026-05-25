from telegram import Update
from telegram.ext import ContextTypes
from database.db_manager import db
from llm.generator import generator
from utils.keyboards import question_keyboard, main_menu_keyboard, session_complete_keyboard
import json
import html
import random
import asyncio

async def start_custom_practice(update: Update, context: ContextTypes.DEFAULT_TYPE, pattern_ids: list, target_count: int = 20):
    # Initialize session
    context.user_data['session_patterns'] = pattern_ids

    session_items = []
    pattern_names = []
    seen_names = set()
    for pid in pattern_ids:
        rows = db.execute_query("SELECT name FROM patterns WHERE id = %s", (pid,))
        if not rows:
            continue

        name = rows[0]['name']
        if name not in seen_names:
            seen_names.add(name)
            pattern_names.append(name)

        hybrid_variants = generator.get_hybrid_variants(name)
        if hybrid_variants:
            session_items.extend({'pattern_id': pid, 'hybrid_type': ht} for ht in hybrid_variants)
        else:
            session_items.append({'pattern_id': pid})

    if not session_items:
        session_items = [{'pattern_id': pid} for pid in pattern_ids]

    # Create a shuffled queue to ensure all underlying question types are covered fairly.
    shuffled_items = session_items.copy()
    random.shuffle(shuffled_items)
    context.user_data['session_pattern_items'] = session_items
    context.user_data['session_patterns_queue'] = shuffled_items
    
    context.user_data['session_score'] = 0
    context.user_data['session_total_target'] = max(target_count, len(session_items))
    context.user_data['session_current_index'] = 0
    context.user_data['custom_pool'] = [] # Pool for batched questions
    context.user_data['session_wrong_patterns'] = [] # Track wrong answers
    context.user_data['session_wrong_questions'] = [] # Track wrong question texts
    
    # Selection Summary
    summary_text = "📋 <b>Your Selection:</b>\n"
    summary_text += "\n".join([f"• {html.escape(name)}" for name in pattern_names])
    if len(session_items) > len(pattern_names):
        summary_text += f"\n\nCovers <b>{len(session_items)}</b> underlying question types."
    summary_text += f"\n\n🚀 Starting a session of {context.user_data['session_total_target']} questions!"
    
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id, summary_text, parse_mode='HTML')
        
    await trigger_next_question(update, context)

import time

async def _fill_custom_pool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Internal helper to fill the question pool via LLM batch."""
    session_items = context.user_data.get('session_pattern_items') or [
        {'pattern_id': pid} for pid in context.user_data.get('session_patterns', [])
    ]
    if not session_items:
        return
        
    # Prepare patterns for the batch using a fair queue
    queue = context.user_data.get('session_patterns_queue', [])
    selected_for_batch = []
    
    while len(selected_for_batch) < 5:
        if not queue:
            # Refill and reshuffle when empty
            queue = session_items.copy()
            random.shuffle(queue)

        if not queue:
            return False, "No session patterns available."

        selected_for_batch.append(queue.pop(0))
    
    # Save the remaining queue back
    context.user_data['session_patterns_queue'] = queue
        
    batch_patterns_info = []
    user_id = update.effective_user.id
    for item in selected_for_batch:
        if isinstance(item, dict):
            pid = item['pattern_id']
            hybrid_type = item.get('hybrid_type')
        else:
            pid = item
            hybrid_type = None

        res = db.execute_query("SELECT p.id, p.name, p.description, p.difficulty_level, t.name as topic_name FROM patterns p JOIN topics t ON p.topic_id = t.id WHERE p.id = %s", (pid,))
        if res:
            p = res[0]
            current_diff = db.get_current_difficulty(user_id, pid)
            pattern_info = {
                'id': p['id'],
                'name': p['name'],
                'topic_name': p['topic_name'],
                'description': p['description'],
                'difficulty': current_diff,
                'avoid_questions': db.get_recent_questions(p['id'])
            }
            if hybrid_type:
                pattern_info['hybrid_type'] = hybrid_type
            batch_patterns_info.append(pattern_info)
    
    questions, error = generator.generate_batch(batch_patterns_info, count=5)
    if questions:
        # Add to existing pool if any (unlikely to have any due to logic, but safer)
        if 'custom_pool' not in context.user_data:
            context.user_data['custom_pool'] = []
        context.user_data['custom_pool'].extend(questions)
        return True, None
    return False, error

async def trigger_next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_count = context.user_data.get('session_current_index', 0)
    target_count = context.user_data.get('session_total_target', 5)
    
    if current_count >= target_count:
        # Session Complete logic...
        score = context.user_data.get('session_score', 0)
        wrong_patterns = context.user_data.get('session_wrong_patterns', [])
        
        final_msg = (
            f"🏁 <b>Session Complete!</b>\n\n"
            f"Your Final Score: <b>{score}/{target_count}</b>\n\n"
        )
        
        if wrong_patterns:
            final_msg += "📉 <b>Areas for Improvement:</b>\n"
            from collections import Counter
            counts = Counter(wrong_patterns)
            
            # Fetch names
            names_msg = ""
            for pid, count in counts.items():
                res = db.execute_query("SELECT name FROM patterns WHERE id = %s", (pid,))
                if res:
                    names_msg += f"• {html.escape(res[0]['name'])}: {count} wrong\n"
            
            final_msg += names_msg + "\n"
            
        wrong_questions = context.user_data.get('session_wrong_questions', [])
        chat_id = update.effective_chat.id
        
        if wrong_questions:
            wq_msg = "❌ <b>Review Your Incorrect Answers:</b>\n"
            for idx, wq in enumerate(wrong_questions):
                # Ensure we don't exceed message limits, clip if needed
                wq_str = f"\n<b>Q{idx+1}:</b> {wq}\n"
                if len(wq_msg) + len(wq_str) > 4000:
                    wq_msg += "\n<i>...and more questions omitted.</i>"
                    break
                wq_msg += wq_str
                
            try:
                await context.bot.send_message(chat_id, wq_msg, parse_mode='HTML')
            except Exception as e:
                print(f"DEBUG: Failed to send wrong questions msg: {e}")
                
        final_msg += "What would you like to do next?"
        
        await context.bot.send_message(chat_id, final_msg, reply_markup=session_complete_keyboard(target_count=target_count), parse_mode='HTML')
        return

    # Check question pool
    pool = context.user_data.get('custom_pool', [])
    if not pool:
        # Generate batch of 5 synchronously
        chat_id = update.effective_chat.id
        status_msg = await context.bot.send_message(chat_id, "<i>Generating a batch of questions... ⏳</i>", parse_mode='HTML')
        
        success, error = await _fill_custom_pool(update, context)
        await status_msg.delete()
        
        if not success:
            await context.bot.send_message(chat_id, f"❌ <b>Batch Generation Error:</b>\n\n{html.escape(error or 'Empty response')}", parse_mode='HTML')
            return
        
        pool = context.user_data.get('custom_pool', [])

    # Get next question from pool
    q_data = pool.pop(0)
    context.user_data['custom_pool'] = pool # Update pool in context
    
    # Check if we should prefetch (if pool is empty and we have more questions to go)
    if not pool and (current_count + 1 < target_count):
        print("DEBUG: Prefetching next batch in background...")
        asyncio.create_task(_fill_custom_pool(update, context))
    
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
    print(f"DEBUG: handle_answer current_question: {bool(q_data)}")
    
    if not q_data:
        await query.message.reply_text("No active question found.")
        return

    is_correct = (user_ans == q_data['correct_option_index'])
    correct_option = q_data['options'][q_data['correct_option_index']]
    
    if is_correct:
        context.user_data.setdefault('session_score', 0)
        context.user_data['session_score'] += 1
        res_msg = "✅ <b>Correct!</b>"
    else:
        res_msg = f"❌ <b>Incorrect.</b>\n\nCorrect Answer: {html.escape(str(correct_option))}"
        
        pattern_id = context.user_data.get('current_pattern_id')
        if pattern_id:
            context.user_data.setdefault('session_wrong_patterns', []).append(pattern_id)
            
        context.user_data.setdefault('session_wrong_questions', []).append(html.escape(q_data['question_text']))
    
    context.user_data.setdefault('session_current_index', 0)
    context.user_data['session_current_index'] += 1
    
    pattern_id = context.user_data.get('current_pattern_id')
    print(f"DEBUG: handle_answer pattern_id: {pattern_id}, is_correct: {is_correct}")
    
    # Update DB Progress (SRS)
    if pattern_id:
        try:
            db.update_user_progress(
                update.effective_user.id,
                pattern_id,
                is_correct,
                5 if is_correct else 2,
                time_taken=time_taken
            )
            # Record explicit question attempt with timing
            db.record_question_attempt(
                update.effective_user.id, 
                pattern_id, 
                is_correct, 
                time_taken
            )
            if not is_correct:
                db.record_mistake(
                    update.effective_user.id,
                    pattern_id,
                    q_data['question_text'],
                    q_data['options'],
                    q_data['correct_option_index'],
                    user_ans,
                    q_data.get('explanation', ''),
                    q_data.get('difficulty', 3),
                )
        except Exception as db_err:
            print(f"DEBUG: db.update_user_progress error: {db_err}")
            await query.message.reply_text(f"⚠️ <b>Database Error:</b> {html.escape(str(db_err))}", parse_mode='HTML')
    else:
        print("DEBUG: Missing current_pattern_id in session")
    
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
        from handlers.daily_v2_handler import trigger_daily_question
        await trigger_daily_question(update, context)
    else:
        await trigger_next_question(update, context)
