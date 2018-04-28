import json
import os
import sys

from attrdict import AttrDict


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class AttrConfig(AttrDict):
    """
    Simple AttrDict subclass to return None when requested attribute does not exist
    """

    def __init__(self, config):
        super().__init__(config)

    def __getattr__(self, item):
        try:
            return super().__getattr__(item)
        except AttributeError:
            pass
        # Default behaviour
        return None


class Config(object, metaclass=Singleton):
    base_config = {
        'rtorrent': {
            'url': 'https://user:password@rutorrent.domain.com'
        },
        'nzbget': {
            'url': 'https://user:password@rutorrent.domain.com'
        },
        'plexpy': {
            'url': 'https://plexpy.domain.com',
            'api_key': 'YOUR_API_KEY'
        },
        'motd': {
            'show': {
                'plexpy': False,
                'rtorrent': False,
                'nzbget': False
            }
        }
    }

    def __init__(self, config_path, logger):
        """Initializes config"""
        self.conf = None

        self.config_path = config_path
        self.logger = logger

    @property
    def cfg(self):
        # Return existing loaded config
        if self.conf:
            return self.conf

        # Built initial config if it doesn't exist
        if self.build_config():
            self.logger.warning("Please edit the default configuration before running again!")
            sys.exit(0)
        # Load config, upgrade if necessary
        else:
            tmp = self.load_config()
            self.conf, upgraded = self.upgrade_settings(tmp)

            # Save config if upgraded
            if upgraded:
                self.dump_config()

            return self.conf

    def build_config(self):
        if not os.path.exists(self.config_path):
            self.logger.warning("Dumping default config to: %s" % self.config_path)
            with open(self.config_path, 'w') as fp:
                json.dump(self.base_config, fp, sort_keys=True, indent=2)
            return True
        else:
            return False

    def dump_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'w') as fp:
                json.dump(self.conf, fp, sort_keys=True, indent=2)
            return True
        else:
            return False

    def load_config(self):
        with open(self.config_path, 'r') as fp:
            return AttrConfig(json.load(fp))

    def upgrade_settings(self, currents):
        upgraded = False

        def inner_upgrade(default, current, key=None):
            sub_upgraded = False
            merged = current.copy()
            if isinstance(default, dict):
                for k, v in default.items():
                    # missing k
                    if k not in current:
                        merged[k] = v
                        sub_upgraded = True
                        if not key:
                            self.logger.info("Added %r config option: %s" % (str(k), str(v)))
                        else:
                            self.logger.info("Added %r to config option %r: %s" % (str(k), str(key), str(v)))
                        continue
                    # iterate children
                    if isinstance(v, dict) or isinstance(v, list):
                        merged[k], did_upgrade = inner_upgrade(default[k], current[k], key=k)
                        sub_upgraded = did_upgrade if did_upgrade else sub_upgraded

            elif isinstance(default, list) and key:
                for v in default:
                    if v not in current:
                        merged.append(v)
                        sub_upgraded = True
                        self.logger.info("Added to config option %r: %s" % (str(key), str(v)))
                        continue
            return merged, sub_upgraded

        upgraded_settings, upgraded = inner_upgrade(self.base_config, currents)
        return AttrConfig(upgraded_settings), upgraded
