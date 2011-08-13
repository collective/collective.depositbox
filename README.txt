Introduction
============

This is a small package for Zope2 that does something similar to a
part of what the PasswordResetTool from Plone does.  It stores a
value, with a possible validation token, and guards it with a secret.

The PasswordResetTool uses a similar technique to store password reset
requests; it then sends an email with a link and a generated secret to
a given email address.  When the recipient follows the link and fills
in the secret (this is actually part of the link so this is done
implicitly) and his user name (the validation token) he is allowed to
set a fresh password.

This package is meant to support this and similar use cases.  You
could use this to store an email address that needs to be confirmed
before adding it to a mailing list.  Or you generate 1,000 secrets,
print them, hand them out on a trade show, and give a people 5 euro
when they register on your website with this secret; perhaps you could
cobble something like this together in combination with PloneFormGen.

The part this package does is:

- storing the value (done with annotations)

- possibly confirming in case there is a validation token

- getting the value

- editing the value

- removing the value

No emails are sent.  If that is needed for a use case, that is the
responsibility of integrators.


Dependencies
============

Tested with Plone 3.3.5, 4.0.9, 4.1.  Might work in Plone 2.5 already.
Probably works in plain Zope2 as well.


Install
=======

Add this to the eggs of your buildout.  On Plone 3.2 or lower also
load the zcml (done automatically in 3.3 or higher).


Sample usage
============

There are some sample browser views in the sample directory of the
package.  If you want to use them in a test instance, load their
zcml; in a buildout config that would be something like this::

  [instance]
  ...
  zcml =
      ...
      collective.depositbox.sample

Rerun buildout, start the instance, and in the root of the site (or
somewhere else) visit ``@@deposit-simple`` or ``@@deposit-add``.  If
you follow the instructions of the last one you will add, confirm,
edit and delete an item.


Sample code
===========

    >>> from collective.depositbox.store import Box
    >>> box = Box()
    >>> secret = box.put(object())
    >>> box.get(secret)
    <object object at ...>
    >>> box.edit(secret, 42)
    >>> box.get(secret)
    42
    >>> box.pop(secret)
    42
    >>> box.pop(secret)
    >>> secret = box.put('my data', token='maurits@example.com')
    >>> box.get(secret, token='maurits@example.com') is None
    True
    >>> box.confirm(secret, token='maurits@example.com')
    True
    >>> box.get(secret, token='maurits@example.com')
   'my data'
    >>> box.get(secret, token='bad@example.com') is None
    True
    >>> box.pop(secret) is None
    True
    >>> box.pop(secret, token='maurits@example.com')
    'my data'


Expiring
========

Note that after a while (7 days by default) the secret expires and the
data is removed.


Integrators
===========

The default adapter is registered for anything that is
IAttributeAnnotatable, which is true for any content item in Plone.
It adds one deposit box on the context.  This may be fine for your use
case, but maybe you want something else.  So here are a few ideas.

- Look in config.py for some settings you could easily override in a
  monkey patch.

- You could register your own adapter that inherits from
  ``BoxAdapter``.  You can then override ``ANNO_KEY`` so you can store
  a box under a different name.  With ``max_age`` you can determine
  the number of days before a secret expires.  Similarly, with
  purge_days you can determine how often old items get purged.  Maybe
  register this adapter specifically for IPloneSiteRoot.

- You can add a value in the deposit box and get the secret back in a
  page template with a TAL definition like this::

    depositview context/@@deposit-box;
    secret python:depositview.put('foobar');

  For a slightly bigger example see
  ``collective/depositbox/sample/templates/simple.pt``.
