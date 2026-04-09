# utils/qr.py

import qrcode
import os
import uuid

def generate_qr(base_url: str, token: str):
    # ✅ Create scan URL (dynamic)
    scan_url = f"{base_url}/qr/scan?token={token}"

    # ✅ Ensure folder exists
    folder = "static/qr_codes"
    os.makedirs(folder, exist_ok=True)

    # ✅ Unique file name
    file_name = f"{uuid.uuid4()}.png"
    file_path = os.path.join(folder, file_name)

    # ✅ Generate QR
    img = qrcode.make(scan_url)
    img.save(file_path)

    return file_path