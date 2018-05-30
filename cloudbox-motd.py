#!/usr/bin/env python3
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

import utils

############################################################
# INIT
############################################################

# Logging
log_format = '%(asctime)s - %(levelname)-10s - %(name)-35s - %(funcName)-35s - %(message)s'

log_formatter = logging.Formatter(log_format)
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.ERROR)

log_file_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "activity.log")

file_handler = RotatingFileHandler(
    log_file_path,
    maxBytes=1024 * 1024 * 5,
    backupCount=5
)
file_handler.setFormatter(log_formatter)
root_logger.addHandler(file_handler)
root_logger.setLevel(logging.DEBUG)

log = root_logger.getChild("cloudbox-motd")

############################################################
# MAIN
############################################################

if __name__ == "__main__":
    # Load config
    from utils.config import Config

    cfg = Config(config_path=os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "config.json"),
                 logger=log).cfg

    # Parse args
    if len(sys.argv) < 3:
        print("ERROR: Not enough arguments")
        exit(1)

    cmd_type = sys.argv[1].lower()
    cmd_func = sys.argv[2].lower()

    # Process types
    if cmd_type == 'config':

        # Process funcs
        if cmd_func == 'upgrade':
            exit(0)

    elif cmd_type == 'autoscan':
        autoscan = utils.Autoscan(cfg.autoscan.url, cfg.autoscan.api_key)

        # Process funcs
        if cmd_func == 'get_queue_count':
            print(autoscan.get_queue_count())
            exit(0)

    elif cmd_type == 'disk':

        # Process funcs
        if cmd_func == 'usage':
            if len(sys.argv) < 4:
                total_space, used_space, used_percent, free_space = utils.disk.get_disk_usage("/")
                print("%s|%s|%s|%s" % (total_space, used_space, used_percent, free_space))
            else:
                total_space, used_space, used_percent, free_space = utils.disk.get_disk_usage(sys.argv[3])
                print("%s|%s|%s|%s" % (total_space, used_space, used_percent, free_space))
            exit(0)

    elif cmd_type == 'rtorrent':
        rtorrent = utils.Rtorrent(cfg.rtorrent.url)

        # Process funcs
        if cmd_func == 'get_download_total':
            print(rtorrent.get_download_total())
            exit(0)
        elif cmd_func == 'get_upload_total':
            print(rtorrent.get_upload_total())
            exit(0)
        elif cmd_func == 'get_download_rate':
            print(rtorrent.get_download_rate())
            exit(0)
        elif cmd_func == 'get_upload_rate':
            print(rtorrent.get_upload_rate())
            exit(0)
        elif cmd_func == 'get_torrent_counts':
            torrent_count, downloading_count, seeding_count = rtorrent.get_torrent_counts()
            print("%d.%d.%d" % (torrent_count, downloading_count, seeding_count))
            exit(0)

    elif cmd_type == 'nzbget':
        nzbget = utils.Nzbget(cfg.nzbget.url)

        # Process funcs
        if cmd_func == "get_download_total":
            print(nzbget.get_download_total())
            exit(0)
        elif cmd_func == "get_download_rate":
            print(nzbget.get_download_rate())
            exit(0)
        elif cmd_func == "get_nzb_counts":
            nzb_count, downloading_count, paused_count, unpacking_count, repairing_count, verifying_count = \
                nzbget.get_nzb_counts()
            print("%d.%d.%d.%d.%d.%d" % (nzb_count, downloading_count, paused_count, unpacking_count, repairing_count,
                                         verifying_count))
            exit(0)

    elif cmd_type == 'plexpy':
        plexpy = utils.Plexpy(cfg.plexpy.url, cfg.plexpy.api_key)

        # Process funcs
        if cmd_func == "get_stream_bandwidth":
            print(plexpy.get_stream_bandwidth())
            exit(0)
        elif cmd_func == "get_stream_counts":
            transcodes, direct_play, direct_streams = plexpy.get_stream_counts()
            print("%d.%d.%d" % (transcodes, direct_play, direct_streams))
            exit(0)

    print("ERROR: Unknown cmd=%r, func=%r" % (cmd_type, cmd_func))
    exit(1)
