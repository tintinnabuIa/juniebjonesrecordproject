# this file doesn't actually do anything, but it would be of use for future developers
# who would want to authenticate, so it stays (since my project doesn't actually need
# any permissions, there is nothing to authenticate for)

from fastapi import Request

async def request_to_shopify_req(request: Request):
    body = await request.body()
    return {
        "method": request.method,
        "headers": dict(request.headers),
        "url": str(request.url),
        "body": body.decode("utf-8") if body else "",
    }