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

This package is meant to support this and similar use cases.  The part
this package does is:

- storing the value (done with annotations)

- possibly confirming in case there is a validation token

- getting the value

- editing the value

- removing the value

No emails are sent.  If that is needed for a use case, that is the
responsibility of integrators.


Target audience
===============

Target audience is integrators, as the package does not really do
anything interesting for end users.  You will have to build something
around it.  This could be as easy as a PloneFormGen form.  Here are
some possible use cases.

- You could use this to store an email address that needs to be
  confirmed before adding it to a mailing list.

- Or you generate 1,000 secrets, print them, hand them out on a trade
  show, and give people 5 euro when they register on your website with
  this secret; perhaps you could cobble something like this together
  in combination with PloneFormGen.


Dependencies
============

Tested with Plone 3.3.5, 4.0.9, 4.1, 4.2, 4.3.6, 5.0.
Might work in Plone 2.5 already.
Probably works in plain Zope2 as well.


Install
=======

Add this to the eggs of your buildout.  On Plone 3.2 or lower also
load the zcml (done automatically in 3.3 or higher).
