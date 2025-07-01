import time
import asyncio
import telegram
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application
from amazon_paapi import AmazonApi
import logging
import random

# --- CARGA DE CONFIGURACIÓN SEGURA ---
load_dotenv()

# Leemos las claves desde el archivo .env
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
AMAZON_ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY')
AMAZON_SECRET_KEY = os.getenv('AMAZON_SECRET_KEY')
AMAZON_ASSOCIATE_TAG = os.getenv('AMAZON_ASSOCIATE_TAG')
AMAZON_COUNTRY = os.getenv('AMAZON_COUNTRY', 'ES')

# --- VALIDACIÓN DE CONFIGURACIÓN ---
if not all([TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOCIATE_TAG]):
    # Usamos print en lugar de raise para que no se cierre si se ejecuta sin .env
    print("ALERTA: Faltan una o más claves en el archivo .env. El bot no podrá funcionar correctamente.")

# --- ESTRATEGIAS DE BÚSQUEDA ---
ESTRATEGIAS_DE_VERANO = [
    {'type': 'keyword', 'value': 'imprescindibles verano', 'name': 'Imprescindibles Verano'},
    {'type': 'keyword', 'value': 'toallas de playa microfibra', 'name': 'Toallas de Playa'},
    {'type': 'keyword', 'value': 'sillas de playa plegables', 'name': 'Sillas de Playa'},
    {'type': 'browse_node', 'value': '1393162031', 'name': 'Moda de Verano'},
]
ESTRATEGIA_EROTICA = [
    {'type': 'browse_node', 'value': '2934899031', 'name': 'Salud Sexual y Erotismo'},
]
ESTRATEGIAS_DE_PRODUCTOS = ESTRATEGIAS_DE_VERANO + ESTRATEGIA_EROTICA

# --- Configuración del logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def buscar_productos(amazon_api, categoria):
    """Busca productos en Amazon."""
    try:
        logger.info(f"Buscando en la sección: '{categoria['name']}'")
        params = {'item_count': 10}
        pagina_aleatoria = random.randint(1, 5)
        logger.info(f"Explorando la página de resultados número {pagina_aleatoria}...")

        if categoria['type'] == 'browse_node':
            params['browse_node_id'] = categoria['value']
        elif categoria['type'] == 'keyword':
            params['keywords'] = categoria['value']

        search_result = amazon_api.search_items(item_page=pagina_aleatoria, **params)

        if not search_result or not search_result.items:
            logger.warning("La API de Amazon no devolvió ningún resultado.")
            return []
        
        logger.info("Búsqueda en Amazon completada.")
        productos_encontrados = search_result.items
        random.shuffle(productos_encontrados)
        return productos_encontrados
    except Exception as e:
        logger.error(f"Error al buscar productos en Amazon: {e}")
        return []

async def main():
    """Función principal del bot."""
    if not all([AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOCIATE_TAG]):
        logger.error("No se pueden inicializar las APIs sin las claves en el archivo .env")
        return

    try:
        amazon_api = AmazonApi(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOCIATE_TAG, AMAZON_COUNTRY, 
            search_url_options={"Resources": ["Images.Primary.Large", "ItemInfo.Title", "Offers.Listings.Price"]})
        logger.info("API de Amazon inicializada.")
    except Exception as e:
        logger.error(f"Error al inicializar la API de Amazon: {e}")
        return

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    bot = application.bot
    logger.info("Bot de Telegram inicializado.")

    posted_asins = set()
    while True:
        logger.info("--- Iniciando nuevo ciclo de publicación ---")
        publicados_en_este_ciclo = 0
        for i in range(5): # Intentar hasta 5 veces encontrar productos
            if publicados_en_este_ciclo >= 3:
                break
            
            tipo_de_busqueda = random.choice(ESTRATEGIAS_DE_PRODUCTOS)
            productos = buscar_productos(amazon_api, tipo_de_busqueda)
            
            if productos:
                for producto in productos:
                    if producto.asin not in posted_asins and publicados_en_este_ciclo < 3:
                        try:
                            title = producto.item_info.title.display_value
                            url = producto.detail_page_url
                            price = producto.offers.listings[0].price.display_amount
                            imagen_url = producto.images.primary.large.url
                            
                            mensaje_texto = f"☀️ **{title}**\n\n💸 **Precio:** {price}"
                            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔥 Ver en Amazon 🔥", url=url)]])
                            
                            logger.info(f"Publicando producto: {title}")
                            await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=imagen_url, caption=mensaje_texto,
                                                 parse_mode='Markdown', reply_markup=keyboard)
                            posted_asins.add(producto.asin)
                            publicados_en_este_ciclo += 1
                            await asyncio.sleep(15)
                        except (AttributeError, IndexError, TypeError) as e:
                            logger.warning(f"Producto saltado por datos incompletos o error: {e}")
                            continue

        sleep_duration = 30 * 60
        logger.info(f"--- Ciclo completado. Durmiendo durante {sleep_duration / 60} minutos. ---")
        await asyncio.sleep(sleep_duration)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot detenido manualmente.")
