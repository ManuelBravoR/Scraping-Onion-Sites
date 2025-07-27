# Scraping-Onion-Sites
Scrapea sitios .onion usando la red Tor, detecta palabras clave específicas (exposión de información) y genera reportes a telegram.

<div align="center">
  <img src="https://github.com/ManuelBravoR/Resources/blob/main/Screenshot%202025-07-24%20214536.png" alt="Scraping .onion Sites" width="48%">
</div>

[Running scraping onion sites](https://www.youtube.com/watch?v=_pz2VE_hWFA)

# 🧅 Dark Web Keyword Scanner (TOR .onion Scraper)
**Scrapea sitios .onion usando la red Tor, detecta palabras clave específicas y genera reportes automáticos.**

> ⚠️ Este proyecto tiene fines estrictamente educativos y de análisis de seguridad. Su uso indebido podría violar leyes locales o internacionales.

---
<table align="center" width="100%">
  <tr>
    <td width="60%" valign="top">
      <h2>📌 Características principales</h2>
      <ul>
        <li>✅ Conexión vía Tor (SOCKS5 proxy)</li>
        <li>✅ Búsqueda de palabras clave definidas por el usuario (<code>identifiers.txt</code>)</li>
        <li>✅ Exploración profunda (con niveles de profundidad configurables)</li>
        <li>✅ Evita URLs duplicadas</li>
        <li>✅ Detección de URLs <code>.onion</code> en múltiples etiquetas HTML (no solo <code>&lt;a&gt;</code>)</li>
        <li>✅ Soporte para envío de reportes vía <strong>Telegram Bot API</strong></li>
        <li>✅ Compatible con cronjobs</li>
      </ul>
    </td>
    <td width="40%" valign="top" align="center">
      <img src="https://github.com/ManuelBravoR/Resources/blob/main/L4CK_73x0wx4%20(2).png" alt="Scraping .onion Sites" width="300px">
    </td>
  </tr>
</table>


## ⚙️ Requisitos de instalación

### 🔐 Instalar Tor y dependencias
```bash
sudo apt update

sudo apt install tor torsocks -y

sudo systemctl start tor
sudo systemctl enable tor
sudo systemctl status tor

sudo apt install python3-venv tor -y
python3 -m venv venv
source venv/bin/activate
pip install requests[socks] beautifulsoup4 requests-tor
```
## ⚙️ Tecnologías utilizadas
🧱 Tor + SOCKS5 Proxy
Se uso Tor para enrutar las peticiones a través de la red anónima. Tor expone un proxy local en socks5h://127.0.0.1:9050, que se puede usar para acceder a sitios .onion desde Python.
🔄 requests_tor
```bash
rtor = RequestsTor(tor_ports=(9050,), tor_cport=9051, autochange_id=5)
```
Una capa encima de requests que permite:
✅ Conectar fácilmente usando Tor (SOCKS5)
✅ Cambiar identidad con autochange_id
✅ Mantener sesión persistente
<div align="center">
  <img src="https://github.com/ManuelBravoR/Resources/blob/main/Torsocks.png" alt="Scraping .onion Sites" width="48%">
</div>

🥣 BeautifulSoup
Utilizado para parsear el contenido HTML, buscar enlaces y extraer texto limpio de cualquier etiqueta HTML.
```bash
soup = BeautifulSoup(response.text, 'html.parser')
```
<p>
  Referencia Beautiful Soup:
  <a href="https://github.com/oxylabs/web-scraping-data-parsing-beautiful-soup">Oxylabs: Web Scraping con Beautiful Soup</a>.
</p>
<div align="center">
  <img src="https://oxylabs.io/_next/image?url=https%3A%2F%2Fimages.prismic.io%2Foxylabs-web%2FZpBvKB5LeNNTxEoc_NWNiMmRiN2MtNzlkNC00OGIxLTg4NGUtZjZlMWY1ZWQ4NmMz_using-python-and-beautiful-soup-to-parse-data-intro-tutorial2x-3.png%3Fauto%3Dformat%2Ccompress&w=1080&q=75" alt="Scraping .onion Sites" width="48%">
</div>
🤖 Envío de reportes con Telegram
Una vez generado report.txt, puedes enviarlo automáticamente a un canal o grupo de Telegram usando un bot.

Paso 1: Crea un bot con @BotFather
Obtén tu token de bot.

Paso 2: Obtén tu chat ID
Puedes usar bots como @userinfobot o leerlo desde la API.

Paso 3: Configura telegram_config.py
```bash
# telegram_config.py
BOT_TOKEN = 'TU_TOKEN_AQUI'
CHAT_ID = 'TU_CHAT_ID_AQUI'
```
Paso 4: Envía el reporte desde el script
```bash
import telegram_config
import telegram

def enviar_reporte_telegram(path='report.txt'):
    bot = telegram.Bot(token=telegram_config.BOT_TOKEN)
    with open(path, 'r') as f:
        contenido = f.read()
    bot.send_message(chat_id=telegram_config.CHAT_ID, text=f"Reporte de scraping:\n\n{contenido}")
```
🖥️ Ejecución
```bash
python3 scraping_onion_sites.py identifiers.txt
```
🧩 Automatización con cronjob
```bash
crontab -e
0 2 * * * cd /ruta/al/proyecto && /usr/bin/python3 scraping_onion_sites.py identifiers.txt
```
###🖥️ Anexos
⚙️ Ficheros Utilizados
<img src="https://img.notionusercontent.com/s3/prod-files-secure%2Fd92e52cd-8fc3-4a5d-997a-84ba8502467d%2F9c72534f-6a89-4e71-8f66-3443d6ef4184%2Fimage.png/size/w=2000?exp=1753637655&sig=70K5100yjBx-JlykDpV44j23cZe3jSNOLwp-nQm7NVI&id=23d1941a-b0eb-80a8-be93-dad6e25549b2&table=block&userId=51cd8123-09b0-4ad7-96c9-8485f0494bf3" alt="Ficheros Utilizados" width="500">

* `seed.txt`: Contiene las URLs de los sitios `.onion` semilla para iniciar la exploración.
* `identifiers.txt`: Define las palabras clave a buscar dentro de los sitios `.onion` (posible exposición de información).
* `torsocks`: Indica el uso de `torsocks` para asegurar que el tráfico se enruta a través de la red Tor, cambiando la IP pública a una IP de Tor.

⚙️ Reporte output
<img src="https://github.com/ManuelBravoR/Resources/blob/main/results.png" alt="Ficheros Utilizados" width="500">

* `report.txt`: Contiene los identifiers a buscar en los onion sites y las URLs donde estas fueron identificadas.
* `report.txt`: Contiene los resultados del escaneo, detallando la información sensible o las coincidencias encontradas según los identificadores definidos. Ayuda a los analistas de seguridad de la información en la identificación temprana de posibles amenazas o exposición de datos (nombre de empresas, personas, entidades, usuarios, etc).

