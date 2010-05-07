Tests
-----

We create box to keep values in:

    >>> from collective.depositbox.store import Box
    >>> box = Box()

We put some value in it and get a secret back:

    >>> secret = box.put(42)

Using the secret as a key, we can get our value back:

    >>> box.get(secret)
    42

We can put any object in the box:

    >>> value = object()
    >>> secret = box.put(value)
    >>> box.get(secret) is value
    True

The secret is an integer:

    >>> isinstance(secret, int)
    True

We can get the item multiple times, but we can also pop the item,
which means we really take the item out of the box:

    >>> box.get(secret) is value
    True
    >>> box.get(secret) is value
    True
    >>> box.pop(secret) is value
    True
    >>> box.pop(secret) is None
    True
    >>> box.get(secret) is None
    True

The secret is a random integer.  When a generated random key is
already taken (small chance, but still a chance), we simply try
again.  This can be tested by seeding the random generator.  First we
check what the first three secrets are that will be generated:

    >>> import random
    >>> random.seed(42)
    >>> first_secret = box._generate_new_id()
    >>> first_secret
    1373158594
    >>> second_secret = box._generate_new_id()
    >>> second_secret
    53710188
    >>> third_secret = box._generate_new_id()
    >>> third_secret
    590620964

We reset the random generator with the same seed and put an item in
the box:

    >>> random.seed(42)
    >>> box.put('first') == first_secret
    True

Reseed and put a second item in the box; since the first secret is
already taken, this gets stored under the second secret:

    >>> random.seed(42)
    >>> box.put('second') == second_secret
    True

Remove the first item:

    >>> box.pop(first_secret)
    'first'

Reseed and put two more items in the box; only the second secret is
already taken now, so the third item gets the first secret and the
fourth item gets the third secret:

    >>> random.seed(42)
    >>> box.put('third') == first_secret
    True
    >>> box.put('fourth') == third_secret
    True

We can optionally store an item with an extra token.  Then we can only
get the item back when we supply both the secret and the token.  This
provides extra safety.

    >>> secret = box.put('my data', 'maurits@example.com')
    >>> box.get(secret) is None
    True
    >>> box.get(secret, 'wrong token') is None
    True
    >>> box.get(secret, 'maurits@example.com')
    'my data'

If we get None back, we always interpret this as meaning there was no
match.  So we should not accept None as a valid value to store in the
box:

    >>> box.put(None)
    Traceback (most recent call last):
    ValueError

TODO: maybe we can add a expiry period: periodically purge items that
have been in the box for too long.  Perhaps do this whenever someone
tries to get an item.
