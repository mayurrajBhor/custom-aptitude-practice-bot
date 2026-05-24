from telegram import Update
from telegram.ext import ContextTypes
from database.db_manager import db
import html

async def show_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    first_name = html.escape(update.effective_user.first_name)
    
    # Get user stats
    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text("User profile not found. Please type /start first.")
        return
    
    # Get overall accuracy, mastery and time
    stats = db.execute_query("""
        SELECT 
            COUNT(*) as total_patterns,
            SUM(total_attempts) as total_attempts,
            SUM(correct_attempts) as total_correct,
            AVG(mastery_score) as avg_mastery,
            AVG(avg_time_seconds) as avg_time
        FROM user_progress 
        WHERE user_id = %s
    """, (user_id,))
    
    s = stats[0] if stats else None
    
    # Get active 9-day cycles
    active_cycles = db.execute_query("""
        SELECT COUNT(*) as count 
        FROM user_added_patterns 
        WHERE user_id = %s AND added_at >= CURRENT_TIMESTAMP - interval '9 days'
    """, (user_id,))
    cycle_count = active_cycles[0]['count'] if active_cycles else 0

    # If no practice records, total_attempts will be None
    if not s or s['total_attempts'] is None or s['total_attempts'] == 0:
        await update.message.reply_text(f"👤 <b>Profile: {first_name}</b>\n\nYou haven't started practicing yet! Start now to see your stats.", parse_mode='HTML')
        return

    accuracy = (s['total_correct'] / s['total_attempts']) * 100 if s['total_attempts'] > 0 else 0
    
    # Get weak topics (top 3 with lowest mastery) + their current level
    weak_topics = db.execute_query("""
        SELECT t.name, up.mastery_score, up.last_difficulty_level
        FROM user_progress up
        JOIN patterns p ON up.pattern_id = p.id
        JOIN topics t ON p.topic_id = t.id
        WHERE up.user_id = %s
        ORDER BY up.mastery_score ASC
        LIMIT 3
    """, (user_id,))
    
    weak_msg = "\n".join([f"- {html.escape(t['name'])}: <b>{round(t['mastery_score']*100)}%</b> (Lvl {t['last_difficulty_level'] or 1})" for t in weak_topics])
    
    avg_speed = s['avg_time'] or 0
    speed_icon = "⚡" if avg_speed < 90 else "⏳"
    
    today_solved = db.get_today_solved_count(user_id)

    profile_msg = (
        f"👤 <b>Profile: {first_name}</b>\n\n"
        f"📊 <b>Core Performance:</b>\n"
        f"• Today's Solved: <b>{today_solved}</b>\n"
        f"• Total Questions: <b>{s['total_attempts']}</b>\n"
        f"• Accuracy: <b>{accuracy:.1f}%</b>\n"
        f"• Overall Mastery: <b>{round(s['avg_mastery']*100 if s['avg_mastery'] else 0)}%</b>\n"
        f"• {speed_icon} Avg Speed: <b>{avg_speed:.1f}s</b>/question\n\n"
        f"📅 <b>Intensive Cycles:</b>\n"
        f"• Active 9-Day Cycles: <b>{cycle_count}</b>\n\n"
        f"🧐 <b>Areas to Focus (Lowest Mastery):</b>\n{weak_msg if weak_msg else 'Keep practicing to identify weak spots!'}"
    )
    
    await update.message.reply_text(profile_msg, parse_mode='HTML')
