import logging

from zope.interface import implements
from zope.component import adapts
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from collective.depositbox.store import Box
from collective.depositbox.interfaces import IDepositBox

logger = logging.getLogger('collective.depositbox')


class BoxAdapter(object):
    """An adapter for our Box.
    """
    implements(IDepositBox)
    adapts(IAttributeAnnotatable)
    ANNO_KEY = 'collective.depositbox'

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        self.box = annotations.get(self.ANNO_KEY, None)
        if self.box is None:
            annotations[self.ANNO_KEY] = Box()
            self.box = annotations[self.ANNO_KEY]

    def put(self, value, token=None):
        return self.box.put(value, token=token)

    def edit(self, secret, value, token=None):
        return self.box.edit(secret, value, token=token)

    def get(self, secret, token=None):
        return self.box.get(secret, token=token)

    def confirm(self, secret, token=None):
        return self.box.confirm(secret, token=token)

    def pop(self, secret, token=None):
        return self.box.pop(secret, token=token)

    def get_all_confirmed(self):
        return self.box.get_all_confirmed()
