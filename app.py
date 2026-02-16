from flask import Flask
import random
import os
from azure.cosmos import CosmosClient

app = Flask(__name__)

# Downloading connection string
connection_string = os.environ.get('COSMOS_DB_CONNECTION_STRING')

# Inicializing Cosmos DB client
client = CosmosClient.from_connection_string(connection_string)
database = client.get_database_client('bomba-db')
container = database.get_container_client('quotes')

@app.route('/')
def home():
    try:
        # Downloading all quotes form DB
        quotes = list(container.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        ))
        
        if quotes:
            quote = random.choice(quotes)
            quote_text = quote.get('text', 'No quote found')
        else:
            quote_text = "No quotes in database"
    except Exception as e:
        quote_text = f"Database error: {str(e)}"
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Captain Bomba Quotes</title>
        <style>
            body {{ font-family: Arial; text-align: center; margin: 50px; background: #f0f0f0; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: auto; }}
            h1 {{ color: #0078d4; }}
            .quote {{ font-size: 24px; margin: 30px 0; color: #333; }}
            button {{ background: #0078d4; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }}
            .db-status {{ color: green; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💣 Captain Bomba Quote Generator 💣</h1>
            <p class="db-status">✅ Connected to Azure Cosmos DB</p>
            <div class="quote">"{quote_text}"</div>
            <button onclick="window.location.reload()">New Quote 🔄</button>
            <p><small><a href="/healthz">Health Check</a> | Database: Azure Cosmos DB</small></p>
        </div>
    </body>
    </html>
    '''

@app.route('/healthz')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run()
