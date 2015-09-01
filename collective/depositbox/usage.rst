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

This should give you an idea of how you should use the code::

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


Storing data persistently
=========================

If you instantiate a ``Box()`` like above, but do not add the box to
some object in the database, then you will lose your data once your
Plone Site restarts.  The normal way to save the box is to use an
adapter to store it in annotations on the context::

    from collective.depositbox.interfaces import IDepositBox
    box = IDepositBox(context)

That context can be the Plone Site root, a folder, a document or
whatever you want.  You can have multiple boxes: different contexts
will have different boxes.  A secret for one box is not valid for
another box.


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

- Look in ``config.py`` for some settings you could easily override in a
  monkey patch.

- Maybe replace the random ``id_generator`` using a monkey patch if
  you don't like the secrets that are generated.  Secrets are
  currently 8 characters from the lowercase alphabet or digits.  We
  avoid accidentally creating (swear) words by excluding vowels, and
  avoid further confusion by excluding 0 and 1.  8 characters sampled
  from these 28 characters give 125 billion possible results.  That is
  enough for 1 random key every second for almost 4000 years.  If you
  want some uuid thingie instead that is fine.  I like that the secret
  is short so that you can safely include it as part of a url in an
  email without making the link too long, which can lead to problems
  in some email programs.

- You could register your own adapter that inherits from
  ``BoxAdapter``.  You can then override ``ANNO_KEY`` so you can store
  a box under a different name.  With ``max_age`` you can determine
  the number of days before a secret expires.  Similarly, with
  purge_days you can determine how often old items get purged.  Maybe
  register this adapter specifically for IPloneSiteRoot.

- You can add a value in the deposit box and get the secret back in a
  page template with a TAL definition like this::

    depositview nocall:context/@@deposit-box;
    secret python:depositview.put('foobar');

  For a slightly bigger example see
  ``collective/depositbox/sample/templates/simple.pt``.
