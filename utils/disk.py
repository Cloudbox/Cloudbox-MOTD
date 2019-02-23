import os

from . import misc


def get_disk_usage(path):
    total_space = "0 GB"
    free_space = "0 MB"
    used_space = "0 MB"
    used_percent = "0%"

    try:
        stat_res = os.statvfs(path)
        total = stat_res.f_blocks * stat_res.f_bsize
        free = stat_res.f_bfree * stat_res.f_bsize
        used = (stat_res.f_blocks - stat_res.f_bfree) * stat_res.f_bsize

        total_space = misc.bytes_to_string(total)
        free_space = misc.bytes_to_string(free)
        used_space = misc.bytes_to_string(used)
        used_percent = "%.2f%%" % (100 * (float(used) / float(total)))
    except Exception:
        pass
    return total_space, used_space, used_percent, free_space
