
from services.strategy import run_strategy_for_user
from services.report import generate_user_report
from services.notifier import send_admin_alert
from app.db import get_all_users
import time
from datetime import datetime

def log_error(msg):
    timestamp = datetime.now().isoformat()
    with open('logs/errors.log', 'a') as f:
        f.write(f'''[{timestamp}] {msg}
''')

def run_user_strategy(user, retries=2):
    for attempt in range(1, (retries + 1)):
        try:
            run_strategy_for_user(user.id)
            return
        except Exception as e:
            if (attempt == retries):
                raise e
            time.sleep(2)

def run_daily_strategy_check():
    users = get_all_users()
    errors = []
    for user in users:
        try:
            run_user_strategy(user)
            report = generate_user_report(user.id)
        except Exception as e:
            error_msg = f'User {user.id} failed: {str(e)}'
            log_error(error_msg)
            errors.append(error_msg)
    if errors:
        send_admin_alert('Daily run completed with errors', errors)
