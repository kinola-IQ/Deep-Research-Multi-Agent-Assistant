"""module to log system events"""
import logging
import time

# instantiating logger
logger = logging.getLogger('uvicorn.error')


# keep track of responsiveness across endpoints
def register_http_logging(app):
    """processing time logger for HTTP requests"""
    @app.middleware("http")
    async def log_process_time(request, call_next):
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as error:
            abrupt_end = time.perf_counter() - start
            logger.error(f"{request.method} {request.url.path} \
                        failed in {abrupt_end:.3f}s: {error}")
            raise

        end = time.perf_counter() - start
        logger.info(f"{request.method} {request.url.path}\
                   completed in {end:.3f}s")
        return response
