from datetime import datetime
import pytz

def convert_ist_to_timezone(ist_datetime_str, target_timezone):
    ist = pytz.timezone('Asia/Kolkata')
    target = pytz.timezone(target_timezone)
    
    dt = datetime.strptime(ist_datetime_str, '%Y-%m-%d %H:%M:%S')
    dt = ist.localize(dt).astimezone(target)
    return dt.strftime('%Y-%m-%d %H:%M:%S')
