#!/usr/bin/env python3
import secrets
import string
import json

def main():
    # Génère une chaîne de 12 caractères alphanumériques
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(12))
    print(json.dumps({"password": password}))

if __name__ == "__main__":
    main()
