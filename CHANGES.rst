Changelog
=========


1.3 (unreleased)
----------------

- Added documentation about using the ``IDepositBox`` adapter.
  [maurits]


1.2 (2014-08-04)
----------------

- Add locales, with Dutch translations.
  [maurits]

- Add simple ``deposit-box-data`` view to see confirmed data.  You may
  want to override this in your own code with some view that presents
  it in a nicer way because it knows what kind of values are stored.
  [maurits]

- Add permission ``collective.depositbox: View Data``.  Allow access
  to ``get_all_confirmed`` data when the user has this permission.
  We do not grant the permission explicitly, so by default only a
  Manager has it.
  [maurits]


1.1 (2012-09-13)
----------------

- Moved to github: https://github.com/collective/collective.depositbox
  [maurits]


1.0 (2011-08-13)
----------------

- Initial release.
  [maurits]
