from . import misc
from .xmlrpc import ServerProxy


class Rtorrent:
    def __init__(self, url):
        self.url = "%s/RPC2" % url
        self.xmlrpc = ServerProxy(self.url)

    def get_download_total(self):
        total_bytes = 0
        try:
            with self.xmlrpc as proxy:
                total_bytes = proxy.throttle.global_down.total()
        except Exception:
            pass
        return misc.bytes_to_string(total_bytes)

    def get_upload_total(self):
        total_bytes = 0
        try:
            with self.xmlrpc as proxy:
                total_bytes = proxy.throttle.global_up.total()
        except Exception:
            pass
        return misc.bytes_to_string(total_bytes)

    def get_download_rate(self):
        total_rate = 0
        try:
            with self.xmlrpc as proxy:
                total_rate = proxy.throttle.global_down.rate()
        except Exception:
            pass
        return "%sps" % misc.bytes_to_string(total_rate).replace('B', 'b')

    def get_upload_rate(self):
        total_rate = 0
        try:
            with self.xmlrpc as proxy:
                total_rate = proxy.throttle.global_up.rate()
        except Exception:
            pass
        return "%sps" % misc.bytes_to_string(total_rate).replace('B', 'b')

    def get_torrent_counts(self):
        total_seeding = 0
        total_downloading = 0
        total_torrents = 0
        try:
            with self.xmlrpc as proxy:
                torrents = proxy.d.multicall2("", "", "d.name=", "d.custom1=", "d.ratio=",
                                              "d.up.rate=", "d.down.rate=")
                total_torrents = len(torrents)
                for torrent in torrents:
                    if int(torrent[-2]):
                        total_seeding += 1
                    if int(torrent[-1]):
                        total_downloading += 1
        except Exception:
            pass
        return total_torrents, total_downloading, total_seeding
