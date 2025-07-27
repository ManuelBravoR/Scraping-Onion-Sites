# Scraping-Onion-Sites
Scrapea sitios .onion usando la red Tor, detecta palabras clave específicas (exposión de información) y genera reportes automáticos.

<div align="center">
  <img src="https://img.notionusercontent.com/s3/prod-files-secure%2Fd92e52cd-8fc3-4a5d-997a-84ba8502467d%2F0ed9a6a2-3061-4df0-85a5-f670e04467ab%2Fimage.png/size/w=2000?exp=1753628919&sig=54LTeC7dDVsXCpSqP1oUhDj4tzoVYcHfz9IC63n8ZKk&id=23b1941a-b0eb-804c-a782-e3f3e2a71f75&table=block&userId=51cd8123-09b0-4ad7-96c9-8485f0494bf3" alt="Scraping .onion Sites" width="48%">
</div>

# 🧅 Dark Web Keyword Scanner (TOR .onion Scraper)
**Scrapea sitios .onion usando la red Tor, detecta palabras clave específicas y genera reportes automáticos.**

> ⚠️ Este proyecto tiene fines estrictamente educativos y de análisis de seguridad. Su uso indebido podría violar leyes locales o internacionales.

---

<table align="center" width="100%">
  <tr>
    <td width="60%" valign="top">
      ## 📌 Características principales

      - 🌐 Conexión vía Tor (SOCKS5 proxy)
      - 🔍 Búsqueda de palabras clave definidas por el usuario (`identifiers.txt`)
      - 🧭 Exploración profunda (con niveles de profundidad configurables)
      - 🧼 Evita URLs duplicadas
      - 🧠 Detección de URLs `.onion` en múltiples etiquetas HTML (no solo `<a>`)
      - 📤 Soporte para envío de reportes vía **Telegram Bot API**
      - ✅ Compatible con cronjobs
    </td>
    <td width="40%" valign="top" align="center">
      <img src="https://img.notionusercontent.com/s3/prod-files-secure%2Fd92e52cd-8fc3-4a5d-997a-84ba8502467d%2F6cb7da08-c23a-4f5f-bc4a-aaacaff0a41f%2FL4CK_73x0wx4.png/size/w=2000?exp=1753629444&sig=UmaInv3_q76gZNSlq-l2DGf7y7OhHKCYozP_AUmyAmM&id=23d1941a-b0eb-801b-a32a-f8fbd961faf5&table=block&userId=51cd8123-09b0-4ad7-96c9-8485f0494bf3" alt="Scraping .onion Sites" width="300px">
    </td>
  </tr>
</table>

---

## 📁 Estructura del proyecto


---

## ⚙️ Requisitos de instalación

### 🔐 Paso 1: Instalar Tor y dependencias
```bash
sudo apt update
sudo apt install python3-venv tor -y
python3 -m venv venv
source venv/bin/activate
pip install requests[socks] beautifulsoup4 requests-tor

