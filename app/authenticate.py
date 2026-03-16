import shopify
from convert_request import request_to_shopify_req
from convert_response import shopify_result_to_response

def app_home(request):
    req = request_to_shopify_req(request)

    result = shopify.verify_app_home_req(
        req,
        app_home_patch_id_token_path="/auth/patch-id-token",
    )

    # The request should not be trusted
    if not result.ok:
        return shopify_result_to_response(result)
    
    # Your database logic here
    access_token = get_access_token(shop=result.shop, mode="offline")

    if access_token:
        refresh_result = shopify.refresh_token_exchanged_access_token(access_token)

        if not refresh_result.ok:
            return shopify_result_to_response(refresh_result)

        if refresh_result.access_token:
            # Package returned a refreshed token — save it
            save_access_token(refresh_result.access_token)

    if not access_token:
        exchange_result = shopify.exchange_using_token_exchange(
            access_mode="offline",
            id_token=result.id_token,
            invalid_token_response=result.new_id_token_response,
        )

        if not exchange_result.ok:
            return shopify_result_to_response(exchange_result)

        # Save the new token
        save_access_token(exchange_result.access_token)

    # Copy headers from result to your response
    for header, value in result.response.headers.items():
        result.response[header] = value
    
    
