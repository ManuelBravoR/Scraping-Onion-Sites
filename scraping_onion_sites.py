import sys
import re
import time
import random
from requests_tor import RequestsTor
from bs4 import BeautifulSoup
import asyncio
from telegram import Bot
import telegram_config
import os

# Configuraciones
MAX_DEPTH = 2
DELAY = 5  # segundos entre requests para no saturar
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]

# Inicializar requests a través de TOR
rtor = RequestsTor(tor_ports=(9050,), tor_cport=9051, autochange_id=5)

# Cargar keywords
def load_keywords(filepath):
    with open(filepath, 'r') as f:
        return [line.strip().lower() for line in f if line.strip()]

# Cargar seeds
def load_seeds(filepath):
    with open(filepath, 'r') as f:
        return [line.strip() for line in f if line.strip()]

# Detectar enlaces .onion en HTML (de <a>, <code>, <li>, texto, etc.)
def extract_onion_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()
    found = set()

    # <a href>
    for tag in soup.find_all(href=True):
        href = tag['href']
        if '.onion' in href:
            found.add(href)

    # Otros tags (ej. <code>, <li>, etc.)
    for tag in soup.find_all(['code', 'li', 'span', 'div']):
        urls = re.findall(r'https?://[^\s"]+\.onion[^\s"]*', tag.get_text())
        found.update(urls)

    # Texto libre
    urls_text = re.findall(r'https?://[^\s"]+\.onion[^\s"]*', text)
    found.update(urls_text)

    return {normalize_url(u, base_url) for u in found}

# Normaliza URLs relativas o sin esquema
def normalize_url(url, base):
    if url.startswith('//'):
        return 'http:' + url
    if url.startswith('/'):
        return base.rstrip('/') + url
    if not url.startswith('http'):
        return 'http://' + url
    return url

# Scrapea una página, busca keywords y extrae links
def scrape(url, depth, keywords, visited, report):
    if depth > MAX_DEPTH or url in visited:
        return

    visited.add(url)
    print(f"[+] Visitando ({depth}): {url}")

    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        response = rtor.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"[!] Error {response.status_code} en {url}")
            return
    except Exception as e:
        print(f"[!] Fallo al conectar con {url} -> {e}")
        return

    html = response.text
    found = False
    for keyword in keywords:
        if keyword in html.lower():
            with open("report.txt", "a") as rep:
                rep.write(f"{keyword} | {url}\n")
            print(f"    [✓] Keyword encontrada: {keyword}")
            found = True

    # Extraer links y seguir si no ha alcanzado profundidad máxima
    onion_links = extract_onion_links(html, url)
    time.sleep(DELAY)

    for link in onion_links:
        if ".onion" in link:
            scrape(link, depth + 1, keywords, visited, report)

#Enviar el reporte a Telegram automáticamente
async def send_report_telegram(path='report.txt'):
    try:
        # Verificar que el archivo existe y no está vacío
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            print("[!] El archivo no existe o está vacío. No se envió nada.")
            return

        # Leer el contenido
        with open(path, 'r') as f:
            contenido = f.read()

        # Crear instancia del bot
        bot = Bot(token=telegram_config.BOT_TOKEN)

        # Dividir el contenido en bloques de 4000 caracteres si es muy largo
        max_length = 4000
        partes = [contenido[i:i+max_length] for i in range(0, len(contenido), max_length)]

        for parte in partes:
            await bot.send_message(chat_id=telegram_config.CHAT_ID, text=parte)

        print("[✓] Reporte enviado por Telegram.")

    except Exception as e:
        print(f"[!] Error al enviar el reporte: {e}")

# ======================= MAIN =======================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 scraping_onion_sites.py identifiers.txt")
        sys.exit(1)

    keywords_file = sys.argv[1]
    keywords = load_keywords(keywords_file)
    seeds = load_seeds("seeds.txt")

    visited = set()
    open("report.txt", "w").close()  # Limpiar salida anterior

    for seed_url in seeds:
        scrape(seed_url, 0, keywords, visited, "report.txt")

    print("\n[✔] Análisis completado. Revisa report.txt")
    asyncio.run(send_report_telegram())
    print("\n[✔] Reporte enviado a Telegram")

