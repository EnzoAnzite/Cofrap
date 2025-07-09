#!/usr/bin/env python3
import sys, json, io, base64
import pyotp, qrcode

def main():
    user_id = sys.stdin.read().strip()

    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    provisioning_uri = totp.provisioning_uri(name=user_id, issuer_name="YourAppName")

    # génère le QR code au format data URI
    img = qrcode.make(provisioning_uri)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    qr_uri = f"data:image/png;base64,{b64}"

    print(json.dumps({"secret": secret, "qr_uri": qr_uri}))


if __name__ == "__main__":
    main()
