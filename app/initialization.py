from shopify_app import ShopifyApp
import os

shopify = ShopifyApp(
    # these'll need to be acquired with the client
    client_id=os.getenv("SHOPIFY_API_KEY"),
    client_secret=os.getenv("SHOPIFY_API_SECRET"),
)