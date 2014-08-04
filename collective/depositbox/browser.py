import csv
from AccessControl import Unauthorized
from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import _checkPermission
from StringIO import StringIO
from collective.depositbox.interfaces import IDepositBox


class DepositBoxView(BrowserView):
    """Simple browser view that knows how to interact with the deposit box.

    Simply a front end for the adapter really.
    """

    # Character set to use for exporting to csv.  Excel likes
    # iso-8859-1: when you use 'utf-8' as export charset excel will
    # show wrong characters for names with c-cedille or other such
    # characters.  So we want to send iso-8859-1 here.
    export_charset = 'iso-8859-1'

    def put(self, value, token=None):
        context = aq_inner(self.context)
        box = IDepositBox(context)
        secret = box.put(value, token=token)
        return secret

    def confirm(self, secret, token=None):
        context = aq_inner(self.context)
        box = IDepositBox(context)
        confirmed = box.confirm(secret, token=token)
        return confirmed

    def get(self, secret, token=None):
        context = aq_inner(self.context)
        box = IDepositBox(context)
        stored = box.get(secret, token=token)
        return stored

    def pop(self, secret, token=None):
        context = aq_inner(self.context)
        box = IDepositBox(context)
        stored = box.pop(secret, token=token)
        return stored

    def edit(self, secret, value, token=None):
        context = aq_inner(self.context)
        box = IDepositBox(context)
        box.edit(secret, value, token=token)

    def get_all_confirmed(self, raise_exceptions=True):
        context = aq_inner(self.context)
        if not _checkPermission("collective.depositbox: View Data", context):
            if raise_exceptions:
                raise Unauthorized("Not allowed to get confirmed data.")
            return []
        box = IDepositBox(context)
        return box.get_all_confirmed()

    def confirmed_as_csv(self):
        out = StringIO()
        writer = csv.writer(out, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for values in self.get_all_confirmed():
            print values
            writer.writerow(values)
        response = self.request.response
        response.setHeader('content-type',
                           'application/vnd.ms-excel; charset=%s' %
                           self.export_charset)
        filename = 'deposit-box-data.csv'
        response.setHeader('content-disposition',
                           'attachment; filename=%s' % filename)

        # Some values may have characters that cannot be translated
        # into the chosen charset, like \u2018 which Microsoft is so
        # fond of...  So replace faulty characters with a question
        # mark.
        return out.getvalue().encode(self.export_charset, 'replace')
