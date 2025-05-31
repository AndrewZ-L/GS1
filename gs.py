import hashlib
import requests

def check_password_leak(password):
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return "Erro ao consultar HIBP (senhas)"
    
    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return f"Senha comprometida! Apareceu {count} vezes em vazamentos."
    return "Senha segura."

def check_email_cybernews(email):
    url = "https://cybernews.com/wp-json/cybernews/v1/leaked-check/"
    payload = {"leaked_data": email}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Erro ao consultar Cybernews: {e}"
    
    data = response.json()
    if data.get("leaked"):
        return f"Email comprometido! {email} foi encontrado em vazamentos."
    else:
        return "Email não encontrado em vazamentos."

def check_mozilla_monitor():
    return ("Mozilla Monitor não possui API pública para consulta automática.\n"
            "Acesse manualmente: https://monitor.firefox.com")

def check_fsecure():
    return ("F-Secure Identity Theft Checker não possui API pública para consulta automática.\n"
            "Acesse manualmente: https://www.f-secure.com/en/identity-theft-checker")

if __name__ == "__main__":
    email = input("Digite seu e-mail para verificação: ")
    password = input("Digite sua senha para verificação: ")
    
    print("\n--- Resultado da verificação ---")
    print("[HIBP] -", check_password_leak(password))
    print("[Cybernews] -", check_email_cybernews(email))
    print("[Mozilla Monitor] -", check_mozilla_monitor())
    print("[F-Secure] -", check_fsecure())
