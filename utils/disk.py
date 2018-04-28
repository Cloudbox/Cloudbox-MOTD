import os

from . import misc


def get_disk_usage(path):
    total_space = "0 GB"
    free_space = "0 MB"
    used_space = "0 MB"
    used_percent = "0%"

    try:
        stat_res = os.statvfs(path)
        total = stat_res.f_frsize * stat_res.f_blocks
        free = stat_res.f_frsize * stat_res.f_bavail
        used = total - free

        total_space = misc.bytes_to_string(total)
        free_space = misc.bytes_to_string(free)
        used_space = misc.bytes_to_string(used)
        used_percent = "%.2f%%" % (100 * (float(used) / float(total)))
    except Exception:
        pass
    return total_space, used_space, used_percent, free_space
