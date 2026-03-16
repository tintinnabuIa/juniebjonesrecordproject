from shopify_app import ShopifyApp
import os

shopify = ShopifyApp(
    client_id=os.getenv("SHOPIFY_API_KEY"),
    client_secret=os.getenv("SHOPIFY_API_SECRET"),
)