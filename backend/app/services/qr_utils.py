# backend/app/services/qr_utils.py

import qrcode, io, base64

def generate_text_qr(text: str) -> str:
    buf = io.BytesIO()
    qrcode.make(text).save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{b64}"
