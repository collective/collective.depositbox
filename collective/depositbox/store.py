import logging
import time
import random
from persistent import Persistent
from BTrees.IOBTree import IOBTree
from zope.interface import implements

from collective.depositbox.interfaces import IDepositBox

MAX_ID = 2 ** 31
logger = logging.getLogger('collective.depositbox')


class Item(Persistent):

    def __init__(self, token, value, confirmed=False):
        self.token = token
        self.value = value
        self.confirmed = confirmed
        self.timestamp = int(time.time())


class Box(Persistent):
    implements(IDepositBox)

    max_age = 7

    def __init__(self):
        self.data = IOBTree()
        self._last_purge = int(time.time())

    def _generate_new_id(self):
        """Generate new id.
        """
        id = random.randint(1, MAX_ID)
        while id in self.data.keys():
            id = random.randint(1, MAX_ID)
        return id

    def put(self, value, token=None):
        """Put value in box, with optional token, and return generated id.

        Calling this method also does a purge once a day (well, when
        the last purge was at least 24 hours ago).
        """
        cutoff = int(time.time()) - 86400
        if self._last_purge < cutoff:
            # Purge each day
            self.purge()

        if value is None:
            raise ValueError
        id = self._generate_new_id()
        self.data[id] = Item(token, value, confirmed=False)
        return id

    def edit(self, secret, value, token=None):
        """Edit value in the box, when secret and optional token match.
        """
        if value is None:
            raise ValueError
        stored = self.get(secret, token=None)
        if value == stored:
            # No change
            return
        self.data[secret] = Item(token, value, confirmed=True)

    def get(self, secret, token=None):
        stored = self.data.get(secret)
        if stored is None:
            return None
        if stored.token != token:
            # raise Exception
            return None
        if not stored.confirmed:
            cutoff = int(time.time()) - self.max_age * 86400
            if stored.timestamp < cutoff:
                del self.data[secret]
                return None
        return stored.value

    def pop(self, secret, token=None):
        stored = self.get(secret, token=token)
        if stored is None:
            return None
        self.data.pop(secret)
        return stored

    def purge(self):
        """Purge items that have expired.

        Confirmed items are not purged.
        """
        cutoff = int(time.time()) - self.max_age * 86400
        logger.info("Started purging data.")
        for key, stored in self.data.items():
            if not stored.confirmed and stored.timestamp < cutoff:
                logger.info("Purged data with secret %r", key)
                del self.data[key]
        self._last_purge = int(time.time())
        logger.info("Finished purging data.")