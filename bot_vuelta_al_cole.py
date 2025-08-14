# -*- coding: utf-8 -*- 

# === IMPORTACIÓN DE LIBRERÍAS ===
# Librerías estándar de Python
import time
import asyncio
import logging
import random
import threading
import os

# Librerías de terceros (requieren instalación con `pip install ...`)
import schedule                   # Para programar tareas (pip install schedule)
import telegram                   # API de Telegram (pip install python-telegram-bot)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from amazon_paapi import AmazonApi  # API de Afiliados de Amazon (pip install python-amazon-paapi)
from dotenv import load_dotenv      # Para cargar variables de entorno desde un archivo (pip install python-dotenv)

# --- CARGA DE VARIABLES DE ENTORNO ---
# Carga la configuración desde el archivo `config.env`.
# Este archivo es local y NUNCA debe subirse a GitHub.
load_dotenv('config.env')

# --- CONFIGURACIÓN GLOBAL DEL BOT ---
# Las credenciales se cargan de forma segura desde las variables de entorno.
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
AMAZON_ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY')
AMAZON_SECRET_KEY = os.getenv('AMAZON_SECRET_KEY')
AMAZON_ASSOCIATE_TAG = os.getenv('AMAZON_ASSOCIATE_TAG')
AMAZON_COUNTRY = os.getenv('AMAZON_COUNTRY', 'ES') # 'ES' es el valor por defecto si no se especifica

# --- VALIDACIÓN INICIAL DE LA CONFIGURACIÓN ---
# Comprueba que todas las variables de configuración han sido cargadas correctamente.
if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOCIATE_TAG]):
    raise ValueError("Error: Faltan una o más credenciales. Asegúrate de crear y rellenar tu archivo 'config.env'.")


# --- 📚 ESTRATEGIAS DE BÚSQUEDA PRINCIPAL: VUELTA AL COLE 📚 ---
# El bot se centrará en estas búsquedas la mayor parte del tiempo.
ESTRATEGIAS_VUELTA_AL_COLE = [
    {'type': 'keyword', 'value': 'mochilas escolares', 'name': 'Mochilas Escolares', 'min_saving': 15},
    {'type': 'keyword', 'value': 'estuches escolares', 'name': 'Estuches', 'min_saving': 10},
    {'type': 'keyword', 'value': 'libros de texto', 'name': 'Libros de Texto', 'min_saving': 5},
    {'type': 'keyword', 'value': 'material escolar', 'name': 'Material Escolar', 'min_saving': 20},
    {'type': 'keyword', 'value': 'calculadoras cientificas', 'name': 'Calculadoras Científicas', 'min_saving': 10},
    {'type': 'keyword', 'value': 'agendas escolares 2025 2026', 'name': 'Agendas Escolares', 'min_saving': 15},
    {'type': 'keyword', 'value': 'portatiles para estudiantes', 'name': 'Portátiles para Estudiantes', 'min_saving': 20},
    {'type': 'keyword', 'value': 'monitores para ordenador', 'name': 'Monitores', 'min_saving': 25},
    {'type': 'keyword', 'value': 'uniforme escolar', 'name': 'Uniformes Escolares', 'min_saving': 15},
    {'type': 'keyword', 'value': 'zapatos colegiales', 'name': 'Zapatos Colegiales', 'min_saving': 20},
]

# --- 👕 ESTRATEGIAS DE BÚSQUEDA SECUNDARIA: ROPA JUVENIL 👕 ---
# Estas búsquedas se realizarán con menos frecuencia para dar variedad.
ESTRATEGIAS_ROPA_JUVENIL = [
    {'type': 'keyword', 'value': 'sudaderas con capucha joven', 'name': 'Sudaderas con Capucha', 'min_saving': 25},
    {'type': 'keyword', 'value': 'zapatillas casual mujer', 'name': 'Zapatillas Casual (Mujer)', 'min_saving': 30},
    {'type': 'keyword', 'value': 'zapatillas casual hombre', 'name': 'Zapatillas Casual (Hombre)', 'min_saving': 30},
    {'type': 'keyword', 'value': 'vaqueros slim fit hombre', 'name': 'Vaqueros Slim Fit', 'min_saving': 20},
    {'type': 'keyword', 'value': 'vestidos juveniles', 'name': 'Vestidos Juveniles', 'min_saving': 25},
    {'type': 'keyword', 'value': 'ropa deportiva niño', 'name': 'Ropa Deportiva (Niño)', 'min_saving': 20},
]

# --- 🎁 PROMOCIONES ESPECIALES DE AMAZON PRIME (PUBLICACIÓN DIARIA) 🎁 ---
# Estos son los mensajes que se publicarán una vez al día.
PROMOCIONES_PRIME = [
    {
        'name': 'Prime Student',
        'text': '🎓 **¡Atención, Estudiante! 90 DÍAS GRATIS de Amazon Prime** 🎓\n\nConsigue todas las ventajas de Prime y ahorra como nunca:\n\n✅ **90 días de prueba GRATIS**\n✅ 50% de descuento tras la prueba (solo 24,95 €/año)\n✅ Envíos rápidos y GRATIS en millones de productos\n✅ Acceso a Prime Video, Music, Reading y más\n✅ Descuentos exclusivos en productos para estudiantes\n\n¡Prepárate para el curso y ahorra a lo grande!',
        'url': f'http://www.amazon.es/joinstudent?tag={AMAZON_ASSOCIATE_TAG}',
        'image_url': 'https://i.imgur.com/O515d1f.png'
    },
    {
        'name': 'Amazon Prime (Prueba Gratuita)',
        'text': '🔥 **Prueba Amazon Prime GRATIS durante 30 días** 🔥\n\nDescubre un mundo de ventajas sin coste alguno:\n\n✅ Envíos GRATIS y rápidos (en 1 día para millones de productos)\n✅ Acceso a miles de películas y series en **Prime Video**\n✅ Más de 2 millones de canciones sin anuncios con **Prime Music**\n✅ Cientos de eBooks gratis con **Prime Reading**\n✅ Ofertas Flash exclusivas\n\n¿A qué esperas para disfrutar de todo esto?',
        'url': f'https://www.amazon.es/tryprime?tag={AMAZON_ASSOCIATE_TAG}',
        'image_url': 'https://i.imgur.com/2E35Y1e.png'
    },
]


# --- CONFIGURACIÓN DEL LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# === FUNCIONES DEL BOT ===

def inicializar_apis():
    """Inicializa las conexiones con las APIs de Amazon y Telegram."""
    try:
        amazon_api = AmazonApi(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOCIATE_TAG, AMAZON_COUNTRY, 
                               search_url_options={"Resources": [
                                   "Images.Primary.Large", 
                                   "ItemInfo.Title", 
                                   "Offers.Listings.Price", 
                                   "Offers.Listings.Saving"
                               ]})
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        logger.info("APIs de Amazon y Telegram inicializadas correctamente.")
        return amazon_api, bot
    except Exception as e:
        logger.error(f"Error fatal al inicializar las APIs: {e}")
        return None, None

def buscar_productos(amazon_api, estrategia):
    """Realiza una búsqueda de productos en Amazon basada en una estrategia."""
    try:
        logger.info(f"Buscando en la categoría: '{estrategia['name']}' con la palabra clave: '{estrategia['value']}'")
        params = {
            'item_count': 10,
            'delivery_flags': ['Prime']
        }
        pagina_aleatoria = random.randint(1, 5)
        if 'min_saving' in estrategia:
            params['min_saving_percent'] = estrategia['min_saving']
        if estrategia['type'] == 'keyword':
            params['keywords'] = estrategia['value']
        search_result = amazon_api.search_items(item_page=pagina_aleatoria, **params)
        if search_result is None or not search_result.items:
            logger.warning("La API de Amazon no devolvió ninguna oferta para esta búsqueda.")
            return []
        logger.info("Búsqueda de ofertas en Amazon completada.")
        productos_encontrados = search_result.items
        random.shuffle(productos_encontrados)
        return productos_encontrados
    except Exception as e:
        logger.error(f"Error inesperado al buscar productos en Amazon: {e}")
        return []

def formatear_mensaje(producto, tipo_busqueda):
    """Crea el texto y el botón para el mensaje de Telegram."""
    title = producto.item_info.title.display_value
    url = producto.detail_page_url
    try:
        price = producto.offers.listings[0].price.display_amount
        saving = None
        if hasattr(producto.offers.listings[0], 'saving') and producto.offers.listings[0].saving is not None:
            saving = producto.offers.listings[0].saving.display_amount
    except (AttributeError, IndexError):
        return None, None, None
    if len(title) > 150:
        title = title[:150] + '...'
    if tipo_busqueda == 'VUELTA_AL_COLE':
        emoji_titulo = "📚"
        texto_boton = "🎒 Ver en Amazon 🎒"
    elif tipo_busqueda == 'ROPA_JUVENIL':
        emoji_titulo = "👕"
        texto_boton = "👟 Ver en Amazon 👟"
    else:
        emoji_titulo = "✨"
        texto_boton = "🔥 ¡Ver Oferta AHORA! 🔥"
    mensaje_texto = (
        f"{emoji_titulo} **¡OFERTA A LA VISTA!** {emoji_titulo}\n\n"
        f"✨ {title}\n\n"
        f"💸 **Precio Actual:** {price}"
    )
    if saving:
        mensaje_texto += f"\n📉 **¡Ahorras {saving}!**"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton(texto_boton, url=url)]])
    imagen_url = producto.images.primary.large.url if producto.images else None
    return mensaje_texto, imagen_url, keyboard

# --- FUNCIONES PARA TAREAS PROGRAMADAS (SCHEDULER) ---

async def publicar_promocion_prime(bot):
    """Publica las dos promociones de Prime, una después de la otra."""
    logger.info("--- [TAREA PROGRAMADA] Iniciando publicación diaria de promociones Prime ---")
    for promo in PROMOCIONES_PRIME:
        logger.info(f"Publicando promoción: {promo['name']}")
        try:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("👉 ¡Activar y Aprovechar! 👈", url=promo['url'])]])
            await bot.send_photo(
                chat_id=TELEGRAM_CHAT_ID,
                photo=promo['image_url'],
                caption=promo['text'],
                parse_mode='Markdown',
                reply_markup=keyboard
            )
            await asyncio.sleep(10)
        except Exception as e:
            logger.error(f"Error al enviar la promoción de Prime '{promo['name']}': {e}")
    logger.info("--- [TAREA PROGRAMADA] Publicación diaria de promociones Prime completada ---")

def run_scheduler(bot):
    """Configura y ejecuta el planificador de tareas en un bucle infinito."""
    schedule.every().day.at("12:00").do(lambda: asyncio.run(publicar_promocion_prime(bot)))
    logger.info("El planificador de tareas está activo. Esperando para ejecutar tareas programadas.")
    while True:
        schedule.run_pending()
        time.sleep(60)

# === FUNCIÓN PRINCIPAL DEL BOT ===

async def main():
    """Función principal que contiene el bucle de búsqueda y publicación de ofertas."""
    amazon_api, bot = inicializar_apis()
    if not all([amazon_api, bot]):
        return
    scheduler_thread = threading.Thread(target=run_scheduler, args=(bot,))
    scheduler_thread.daemon = True
    scheduler_thread.start()
    logger.info("Planificador de tareas para promociones Prime iniciado en segundo plano.")
    posted_asins = set()
    while True:
        logger.info("--- Iniciando nuevo ciclo de búsqueda de ofertas ---")
        publicados_en_este_ciclo = 0
        if random.random() < 0.80:
            estrategia_de_busqueda = random.choice(ESTRATEGIAS_VUELTA_AL_COLE)
            tipo_busqueda = 'VUELTA_AL_COLE'
        else:
            estrategia_de_busqueda = random.choice(ESTRATEGIAS_ROPA_JUVENIL)
            tipo_busqueda = 'ROPA_JUVENIL'
        productos = buscar_productos(amazon_api, estrategia_de_busqueda)
        if productos:
            for producto in productos:
                if producto.asin in posted_asins:
                    continue
                if publicados_en_este_ciclo < 2:
                    mensaje, imagen_url, boton = formatear_mensaje(producto, tipo_busqueda)
                    if mensaje and imagen_url and boton:
                        try:
                            logger.info(f"Publicando oferta de {tipo_busqueda}: ({publicados_en_este_ciclo + 1}/2) {producto.item_info.title.display_value}")
                            await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=imagen_url, caption=mensaje,
                                                 parse_mode='Markdown', reply_markup=boton)
                            posted_asins.add(producto.asin)
                            publicados_en_este_ciclo += 1
                            await asyncio.sleep(30)
                        except Exception as e:
                            logger.error(f"Error al enviar mensaje a Telegram: {e}")
        if publicados_en_este_ciclo == 0:
            logger.info("No se encontraron ofertas nuevas para publicar en este ciclo.")
        sleep_duration = 45 * 60 
        logger.info(f"--- Ciclo completado. Durmiendo durante {sleep_duration / 60} minutos. ---")
        await asyncio.sleep(sleep_duration)

# --- PUNTO DE ENTRADA DEL SCRIPT ---
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot detenido manualmente por el usuario.")
