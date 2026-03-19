# this file doesn't actually do anything, but it would be of use for future developers
# who would want to authenticate, so it stays (since my project doesn't actually need
# any permissions, there is nothing to authenticate for)

import logging
from fastapi.responses import Response

logger = logging.getLogger(__name__)

def shopify_result_to_response(result):
    logger.info("%s - %s", result.log.code, result.log.detail)

    return Response(
        content=result.response.body,
        status_code=result.response.status,
        headers=result.response.headers,
    )