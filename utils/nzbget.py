import xmlrpc.client

from . import misc


class Nzbget:
    def __init__(self, url):
        self.url = "%s/xmlrpc" % url
        self.xmlrpc = xmlrpc.client.ServerProxy(self.url)

    def get_download_total(self):
        total_bytes = 0
        try:
            data = self.xmlrpc.status()
            if type(data) == dict and 'DownloadedSizeHi' in data and 'DownloadedSizeLo' in data:
                total_bytes = (data['DownloadedSizeHi'] << 32) + data['DownloadedSizeLo']
        except Exception:
            pass
        return misc.bytes_to_string(total_bytes)

    def get_download_rate(self):
        total_rate = 0
        try:
            data = self.xmlrpc.status()
            if type(data) == dict and 'DownloadRate' in data:
                total_rate = data['DownloadRate']
        except Exception:
            pass
        return "%sps" % misc.bytes_to_string(total_rate).replace('B', 'b')

    def get_nzb_counts(self):
        total_nzbs = 0
        total_paused = 0
        total_downloading = 0
        total_repairing = 0
        total_unpacking = 0
        total_verifying = 0

        try:
            data = self.xmlrpc.listgroups(0)
            if type(data) == list:
                total_nzbs = len(data)
                for nzb in data:
                    if 'Status' not in nzb:
                        continue
                    elif nzb['Status'].startswith("VERIFYING"):
                        total_verifying += 1
                    elif nzb['Status'].startswith("REPAIRING"):
                        total_repairing += 1
                    elif nzb['Status'].startswith("UNPACKING"):
                        total_unpacking += 1
                    elif nzb['Status'].startswith("PAUSED"):
                        total_paused += 1
                    elif nzb['Status'].startswith("DOWNLOADING"):
                        total_downloading += 1
        except Exception:
            pass
        return total_nzbs, total_downloading, total_paused, total_unpacking, total_repairing, total_verifying
