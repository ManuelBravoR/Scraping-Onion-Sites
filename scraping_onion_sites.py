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

# ==================== CONFIGURACIONES ====================
MAX_DEPTH = 2  # Profundidad máxima de rastreo
DELAY = 5      # Segundos entre requests
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]
TOR_PORTS = (9050,)
TOR_CPORT = 9051

# ==================== INICIALIZACIÓN ====================
# Inicializar requests a través de TOR
rtor = RequestsTor(tor_ports=TOR_PORTS, tor_cport=TOR_CPORT, autochange_id=5)

# ==================== FUNCIONES DE UTILIDAD ====================
def load_keywords(filepath):
    """Carga las palabras clave desde un archivo."""
    try:
        with open(filepath, 'r') as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Error: No se encontró el archivo de palabras clave: {filepath}")
        sys.exit(1)

def load_seeds(filepath):
    """Carga las URLs semilla desde un archivo."""
    try:
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[!] Error: No se encontró el archivo de semillas: {filepath}")
        sys.exit(1)

def normalize_url(url):
    """Normaliza y limpia URLs, asegurando que tengan el formato correcto."""
    # Quitar cualquier fragmento (#) o parámetros de consulta
    url = url.split('#')[0].split('?')[0]
    # Asegurar que termina en .onion y no tiene un path de archivo común
    if ".onion" in url and not url.endswith(('.css', '.js', '.png', '.jpg', '.gif', '.pdf')):
        # Si no tiene el esquema http:// o https://, lo añade.
        if not url.startswith(('http://', 'https://')):
            return f'http://{url}'
        return url
    return None

def extract_onion_links(html):
    """Detecta y extrae enlaces .onion válidos de un HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    found_links = set()

    # Enlaces de etiquetas <a>
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if ".onion" in href:
            normalized_link = normalize_url(href)
            if normalized_link:
                found_links.add(normalized_link)

    # Enlaces de texto libre y otros tags
    for text_content in soup.get_text().split():
        if ".onion" in text_content:
            urls = re.findall(r'https?://[^\s"]+\.onion[^\s"]*', text_content)
            for url in urls:
                normalized_link = normalize_url(url)
                if normalized_link:
                    found_links.add(normalized_link)
    
    return found_links

def check_tor_connection():
    """Verifica la conexión a Tor mostrando la IP pública."""
    print("--- Verificando conexión a Tor ---")
    try:
        response = rtor.get('https://icanhazip.com', timeout=15)
        if response.status_code == 200:
            print(f"[✓] Conectado a Tor. Tu IP de salida es: {response.text.strip()}")
        else:
            print(f"[!] Error al verificar la IP: Status Code {response.status_code}")
    except Exception as e:
        print(f"[!] Error al conectar a Tor para verificar la IP: {e}")
    print("--- Verificación completada ---")


def scrape(url, depth, keywords, visited, report_file):
    """
    Scrapea una página, busca palabras clave, extrae nuevos enlaces
    y realiza la llamada recursiva.
    """
    if depth > MAX_DEPTH or url in visited:
        if url in visited:
            print(f"[+] URL ya visitada, omitiendo: {url}")
        return

    visited.add(url)
    print(f"[+] Visitando ({depth}): {url}")

    headers = {"User-Agent": random.choice(USER_AGENTS)}
    try:
        response = rtor.get(url, headers=headers, timeout=30)
        if response.status_code != 200:
            print(f"[!] Error {response.status_code} en {url}")
            return
    except Exception as e:
        print(f"[!] Fallo al conectar con {url} -> {e}")
        return

    html = response.text
    found_keywords = []
    with open(report_file, "a") as rep:
        for keyword in keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', html, re.IGNORECASE):
                rep.write(f"{keyword} | {url}\n")
                found_keywords.append(keyword)

    if found_keywords:
        print(f"    [✓] Keywords encontradas: {', '.join(found_keywords)}")
    else:
        print("    [–] No se encontraron keywords en esta página.")

    onion_links = extract_onion_links(html)
    
    if onion_links:
        print(f"    [+] Se encontraron {len(onion_links)} enlaces .onion para seguir.")
    else:
        print(f"    [-] No se encontraron enlaces .onion en {url} para seguir.")

    time.sleep(DELAY)

    for link in onion_links:
        scrape(link, depth + 1, keywords, visited, report_file)


# Enviar el reporte a Telegram automáticamente
async def send_report_telegram(path):
    """
    Envía el contenido de un archivo de reporte a través de Telegram.
    """
    try:
        if not os.path.exists(path) or os.path.getsize(path) == 0:
            print("[!] El archivo no existe o está vacío. No se envió nada.")
            return

        with open(path, 'r') as f:
            contenido = f.read()

        bot = Bot(token=telegram_config.BOT_TOKEN)
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

    if not keywords or not seeds:
        print("[!] Palabras clave o URLs semilla vacías. No se puede continuar.")
        sys.exit(1)
    
    check_tor_connection()

    visited = set()
    open("report.txt", "w").close()

    for seed_url in seeds:
        print(f"\n--- Iniciando rastreo desde la semilla: {seed_url} ---")
        scrape(seed_url, 0, keywords, visited, "report.txt")
    
    print("\n[✔] Análisis completado.")
    if os.path.getsize("report.txt") == 0:
        print("[!] report.txt está vacío. No se encontraron keywords. No se enviará nada a Telegram.")
    else:
        asyncio.run(send_report_telegram("report.txt"))
    
    print("[✔] Script finalizado")
