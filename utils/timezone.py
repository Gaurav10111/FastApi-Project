from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")
UTC = pytz.utc


def ist_to_utc(date_str: str, time_str: str):
    dt_str = f"{date_str} {time_str}"
    ist_dt = IST.localize(datetime.strptime(dt_str, "%Y-%m-%d %H:%M"))

    utc_dt = ist_dt.astimezone(pytz.utc)

    return utc_dt.replace(tzinfo=None)  


def get_current_utc():
    return datetime.utcnow()   # ✅ NAIVE UTC