from typing import Optional, Callable
from itertools import chain
from pathlib import Path

import logging

from ..filedb import file_db
from ..config import config
from .stitch import stitch
from .tangle import tangle


def _stitch_then_tangle():
    stitch()
    tangle()


def sync_action() -> Optional[Callable[[], None]]:
    input_file_list = list(chain.from_iterable(map(Path(".").glob, config.watch_list)))

    with file_db(readonly=True) as db:
        changed = set(db.changed())

        if not all(f in db for f in input_file_list):
            return tangle
        
        if not changed:
            logging.info("Nothing to be done")
            return None
        
        if changed.isdisjoint(db.managed):
            logging.info("Tangling")
            return tangle
        
        if changed.issubset(db.managed):
            logging.info("Stitching")
            return _stitch_then_tangle

        logging.error("changed: %s", [str(p) for p in changed])
        logging.error("Both markdown and code seem to have changed. "
                        "Don't know what to do now.")
        return None


def sync():
    """Be smart wether to tangle or stich"""
    action = sync_action()
    if action is not None:
        action()

