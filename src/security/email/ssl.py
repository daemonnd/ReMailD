import ssl
def ssl_context() -> ssl.SSLContext:
    context: ssl.SSLContext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.maximum_version = ssl.TLSVersion.TLSv1_3
    return context
ssl_context()