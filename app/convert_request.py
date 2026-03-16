from fastapi import Request

async def request_to_shopify_req(request: Request):
    body = await request.body()
    return {
        "method": request.method,
        "headers": dict(request.headers),
        "url": str(request.url),
        "body": body.decode("utf-8") if body else "",
    }