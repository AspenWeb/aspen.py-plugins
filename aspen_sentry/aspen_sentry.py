"""Integrate Aspen with the Sentry exception logging service.
"""
import os
import sys

import aspen
import raven


__version__ = "1.0.0"


def install(website, client=None):
    """Takes a website object and installs an error_early hook.
    """
    sentry_dsn = os.environ.get('SENTRY_DSN')
    if sentry_dsn is not None:
        if client is None:
            client = raven.Client(sentry_dsn)
        website.hooks.error_early += [make_hook(client)]


def make_hook(client):
    """Takes a raven.Client, returns an Aspen error_early hook.
    """
    def tell_sentry(request):
        cls, response = sys.exc_info()[:2]
        if cls is aspen.Response:
            if response.code < 500:
                return

        kw = {'extra': { "filepath": request.fs
                       , "request": str(request).splitlines()
                        }}
        exc = client.captureException(**kw)
        ident = client.get_ident(exc)
        aspen.log_dammit("Exception reference: " + ident)
    return tell_sentry
