# services/report.py

def generate_user_report(user_id):
    # Placeholder logic – later pull positions and build a real summary
    return {
        "user_id": user_id,
        "summary": "Report generated successfully.",
        "positions": []
    }

def format_position_output(position):
    # For now, just mock some content
    return {
        "epic": position.epic,
        "status": "HOLD",  # Replace with real strategy logic later
        "profit": 0.0,
    }
