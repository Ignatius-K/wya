"""
This module contains helper functions for validating data.
"""

from urllib.parse import urlparse


def url_has_allowed_host_and_scheme(url, allowed_host):
    """
    Check if the URL is allowed to be used.
    """
    if not url:
        return False
    parsed_url = urlparse(url)
    return (not parsed_url.netloc or parsed_url.netloc == allowed_host) and \
           (parsed_url.scheme in ('http', 'https') if parsed_url.scheme else True)
