

def generate_user_report(user_id):
    return {'user_id': user_id, 'summary': 'Report generated successfully.', 'positions': []}

def format_position_output(position):
    return {'epic': position.epic, 'status': 'HOLD', 'profit': 0.0}
