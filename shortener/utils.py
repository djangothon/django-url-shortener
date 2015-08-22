"""
Utility Methods.

* get_ip_from_request = returns the IP address of remote client.
"""


def get_ip_from_request(request):
    """
    Extract IP from request.

    Look into HTTP_X_FORWARDED_FOR in case a reverse proxy is present, else
    look into REMOTE_ADDR.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_addr = x_forwarded_for.split(',')[0]
    else:
        ip_addr = request.META.get('REMOTE_ADDR')
    return ip_addr
