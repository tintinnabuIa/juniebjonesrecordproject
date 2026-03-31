# this file doesn't actually do anything, but it would be of use for future developers
# who would want to authenticate, so it stays (since my project doesn't actually need
# any permissions, there is nothing to authenticate for)
from shopify_app import ShopifyApp
import os

shopify = ShopifyApp(
    # these'll need to be acquired with the client
    client_id=os.getenv("SHOPIFY_API_KEY"),
    client_secret=os.getenv("SHOPIFY_API_SECRET"),
)