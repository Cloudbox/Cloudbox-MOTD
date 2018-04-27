#!/usr/bin/env python3.5
import sys

import utils

############################################################
# MAIN
############################################################

if __name__ == "__main__":
    # Load config
    conf = utils.misc.load_config()

    # Parse args
    if len(sys.argv) < 3:
        print("ERROR: Not enough arguments")
        exit(1)

    cmd_type = sys.argv[1].lower()
    cmd_func = sys.argv[2].lower()

    # Process types
    if cmd_type == 'rtorrent':
        rtorrent = utils.Rtorrent(conf['rtorrent']['url'])

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
        nzbget = utils.Nzbget(conf['nzbget']['url'])

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
        plexpy = utils.Plexpy(conf['plexpy']['url'], conf['plexpy']['api_key'])

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
