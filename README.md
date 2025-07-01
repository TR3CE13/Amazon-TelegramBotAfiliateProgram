Español | English

Español
🤖 Bot de  Multi-idioma para Telegram
Este es un bot automatizado para Telegram, desarrollado en Python, que busca y publica ofertas de productos de Amazon directamente en un canal. El bot ahora es multi-idioma, permitiendo configurar búsquedas y publicaciones para diferentes mercados de Amazon (ej. España y Estados Unidos).

✨ Características Principales
Búsqueda Automatizada: Busca productos en Amazon utilizando la API de Afiliados (PA-API 5.0).

Publicación Multi-idioma: Publica ofertas en diferentes idiomas (ej. español e inglés) y con enlaces al mercado de Amazon correspondiente.

Estrategias Flexibles: Permite definir estrategias de búsqueda por idioma, país, palabras clave o categorías.

Gestión de Duplicados: Lleva un registro de los productos ya publicados para no repetir ofertas.

Seguridad: Gestiona las claves secretas de forma segura utilizando variables de entorno.

🚀 Tecnologías Utilizadas
Python 3.12

python-telegram-bot: Librería para interactuar con la API de Bot de Telegram.

python-amazon-paapi: Wrapper para facilitar las llamadas a la API de Product Advertising de Amazon.

python-dotenv: Para la gestión segura de las variables de entorno.

⚙️ Guía de Instalación y Puesta en Marcha
1. Prerrequisitos
Python 3.10 o superior.

Una cuenta de Afiliado de Amazon con acceso a la PA-API 5.0. Nota: Necesitarás IDs de afiliado (Associate Tags) para cada región en la que quieras operar (ej. uno para España, otro para EEUU). Tus claves de API (Access y Secret Key) suelen funcionar para múltiples regiones.

Un bot de Telegram creado a través de @BotFather.

2. Clonar el Repositorio
git clone https://github.com/TR3CE13/Amazon-TelegramBotAfiliateProgram.git
cd Amazon-TelegramBotAfiliateProgram

3. Configurar el Entorno Virtual
# Crear el entorno
python3 -m venv venv

# Activar el entorno
source venv/bin/activate
# En Windows, usa: venv\Scripts\activate

4. Instalar Dependencias
pip install -r requirements.txt

5. Configurar las Claves Secretas
Crea un archivo llamado .env en la raíz del proyecto. Edítalo y rellena tus propias claves. Nota: Ahora hay dos IDs de afiliado, uno para cada región.

TELEGRAM_BOT_TOKEN="TU_TOKEN_SECRETO_DE_TELEGRAM"
TELEGRAM_CHAT_ID="@EL_ID_DE_TU_CANAL"

# Claves de la API de Amazon (suelen ser las mismas para varias regiones)
AMAZON_ACCESS_KEY="TU_ACCESS_KEY_DE_AMAZON"
AMAZON_SECRET_KEY="TU_SECRET_KEY_DE_AMAZON"

# IDs de Afiliado (Associate Tags) - ¡UNO PARA CADA REGIÓN!
AMAZON_ASSOCIATE_TAG_ES="TU_ID_DE_AFILIADO_ESPAÑA-21"
AMAZON_ASSOCIATE_TAG_US="TU_ID_DE_AFILIADO_USA-20"

6. Ejecutar el Bot
python lanzador.py

El bot se iniciará y comenzará a publicar ofertas de forma aleatoria de las estrategias en español e inglés que hayas configurado.

English
🤖 Multilingual Telegram Deals Bot
This is an automated bot for Telegram, developed in Python, that searches for and posts product deals from Amazon directly to a channel. The bot is now multilingual, allowing you to configure searches and posts for different Amazon marketplaces (e.g., Spain and the United States).

✨ Key Features
Automated Search: Searches for products on Amazon using the Affiliate API (PA-API 5.0).

Multilingual Posting: Publishes deals in different languages (e.g., Spanish and English) with links to the corresponding Amazon marketplace.

Flexible Strategies: Allows defining search strategies by language, country, keywords, or categories.

Duplicate Management: Keeps a record of already posted products to avoid repeating deals.

Security: Manages secret keys securely using environment variables.

🚀 Technologies Used
Python 3.12

python-telegram-bot: Library to interact with the Telegram Bot API.

python-amazon-paapi: A wrapper to facilitate calls to the Amazon Product Advertising API.

python-dotenv: For secure management of environment variables.

⚙️ Installation and Setup Guide
1. Prerequisites
Python 3.10 or higher.

An Amazon Affiliate account with access to the PA-API 5.0. Note: You will need Associate Tags for each region you want to operate in (e.g., one for Spain, one for the US). Your API keys (Access and Secret Key) usually work for multiple regions.

A Telegram bot created via @BotFather.

2. Clone the Repository
git clone https://github.com/TR3CE13/Amazon-TelegramBotAfiliateProgram.git
cd Amazon-TelegramBotAfiliateProgram

3. Set Up a Virtual Environment
# Create the environment
python3 -m venv venv

# Activate it
source venv/bin/activate
# On Windows, use: venv\Scripts\activate

4. Install Dependencies
pip install -r requirements.txt

5. Configure Secret Keys
Create a file named .env in the project's root directory. Edit it and fill in your own keys. Note: There are now two associate tags, one for each region.

TELEGRAM_BOT_TOKEN="YOUR_SECRET_TELEGRAM_TOKEN"
TELEGRAM_CHAT_ID="@YOUR_CHANNEL_ID"

# Amazon API Keys (usually the same for multiple regions)
AMAZON_ACCESS_KEY="YOUR_AMAZON_ACCESS_KEY"
AMAZON_SECRET_KEY="YOUR_AMAZON_SECRET_KEY"

# Associate Tags - ONE FOR EACH REGION!
AMAZON_ASSOCIATE_TAG_ES="YOUR_SPANISH_ASSOCIATE_TAG-21"
AMAZON_ASSOCIATE_TAG_US="YOUR_US_ASSOCIATE_TAG-20"

6. Run the Bot
python lanzador.py

The bot will start and begin randomly posting deals from the Spanish and English strategies you have configured.
