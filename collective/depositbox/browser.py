from Acquisition import aq_inner
from Products.Five import BrowserView
from collective.depositbox.interfaces import IDepositBox


class BaseView(BrowserView):

    # These variables should be available to the template:
    secret = None
    token = None
    value = None

    # Which form input should be taken as the token? (None works too)
    token_id = 'email'
    # Which form inputs should be taken as value?
    inputs = ['email', 'myinput']

    def __old_call__(self):
        self.secret = self.update()
        # Render whatever was set as the template in zcml:
        return self.index()

    def __call__(self):
        # Get the secret, token and value, when known.
        self.secret = self.get_secret()
        self.token = self.get_token()
        self.value = self.get_value()

        # Do the add/edit/confirm/delete/whatever.  This may update
        # self.secret and have other side effects as well.
        self.update()

        # Render whatever was set as the template in zcml:
        return self.index()

    def get_token(self):
        return self.request.form.get(self.token_id)

    def get_secret(self):
        return int(self.request.form.get('secret', 0))

    def get_value(self):
        form = dict()
        for input_id in self.inputs:
            value = self.request.form.get(input_id)
            if value is not None:
                form[input_id] = value
        return form


class Add(BaseView):

    def old_update(self):
        if self.token_id:
            token = self.request.form.get(self.token_id)
            if not token:
                return
        else:
            token = None
        form = dict()
        for input_id in self.inputs:
            value = self.request.form.get(input_id)
            form[input_id] = value

        context = aq_inner(self.context)
        box = IDepositBox(context)
        secret = box.put(form, token=token)
        return secret

    def update(self):
        if self.token_id and not self.token:
            # Token is required.
            return
        if not self.value:
            return

        context = aq_inner(self.context)
        box = IDepositBox(context)
        secret = box.put(self.value, token=self.token)
        self.secret = secret


class Edit(BaseView):

    def old_update(self):
        """Run any update code, and return the secret if it is valid.
        """
        try:
            secret = int(self.request.form.get('secret', 0))
        except ValueError:
            secret = None
        if not secret:
            return
        context = aq_inner(self.context)
        box = IDepositBox(context)
        stored = box.get(secret)
        if not stored:
            return
        mytext = self.request.form.get('mytext')
        if mytext and mytext != stored:
            box.edit(secret, mytext)
        self.value = box.get(secret)
        return secret

    def update(self):
        """Change the stored value when there are changes.

        And get the stored value when there is nothing in the request.
        """
        if not self.secret:
            return
        if self.token_id and not self.token:
            # Token is required.
            return

        context = aq_inner(self.context)
        box = IDepositBox(context)
        stored = box.get(self.secret, token=self.token)
        if not stored:
            return
        if not self.value:
            # for displaying
            self.value = stored
            return
        if self.value != stored:
            # XXX Store only changes?
            box.edit(self.secret, self.value, token=self.token)
