#!/usr/bin/env python3

# TODO: fix socks proxies

import init_django
from proxy_py import settings
from processor import Processor
from server.proxy_provider_server import ProxyProviderServer
from program_killer import ProgrammKiller
import collectors_list

proxies = []

killer = ProgrammKiller()

# TODO: fix closing of program when it's waiting for finish coroutines
if __name__ == "__main__":
    proxy_processor = Processor()
    for CollectorType in collectors_list.collectorTypes:
        proxy_processor.addCollectorOfType(CollectorType)

    proxy_provider_server = ProxyProviderServer.get_proxy_provider_server(
        settings.PROXY_PROVIDER_SERVER_ADDRESS['HOST'],
        settings.PROXY_PROVIDER_SERVER_ADDRESS['PORT'],
        proxy_processor,
    )
    proxy_provider_server.start()

    try:
        proxy_processor.exec(killer)
    except Exception as ex:
        print("Some shit happened: {}".format(ex))

    proxy_provider_server.stop()
