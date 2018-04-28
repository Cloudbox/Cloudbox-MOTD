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
                total_bytes = proxy.get_down_total()
        except Exception:
            pass
        return misc.bytes_to_string(total_bytes)

    def get_upload_total(self):
        total_bytes = 0
        try:
            with self.xmlrpc as proxy:
                total_bytes = proxy.get_up_total()
        except Exception:
            pass
        return misc.bytes_to_string(total_bytes)

    def get_download_rate(self):
        total_rate = 0
        try:
            with self.xmlrpc as proxy:
                total_rate = proxy.get_down_rate()
        except Exception:
            pass
        return "%sps" % misc.bytes_to_string(total_rate).replace('B', 'b')

    def get_upload_rate(self):
        total_rate = 0
        try:
            with self.xmlrpc as proxy:
                total_rate = proxy.get_up_rate()
        except Exception:
            pass
        return "%sps" % misc.bytes_to_string(total_rate).replace('B', 'b')

    def get_torrent_counts(self):
        total_seeding = 0
        total_downloading = 0
        total_torrents = 0
        try:
            with self.xmlrpc as proxy:
                torrents = proxy.d.multicall("main", "d.get_name=", "d.get_custom1=", "d.get_ratio=",
                                             "d.get_up_rate=", "d.get_down_rate=")
                total_torrents = len(torrents)
                for torrent in torrents:
                    if int(torrent[-2]):
                        total_seeding += 1
                    if int(torrent[-1]):
                        total_downloading += 1
        except Exception:
            pass
        return total_torrents, total_downloading, total_seeding
