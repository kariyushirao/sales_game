# consent form in oTree

This module should be inserted as a first app in a sequence.
It does the following:

1. It does not allow the user to proceed without confirming that he/she 
agrees to give the consent.

2. If a person does not sign the consent in _n_ minutes, it forwards the user
to the dead end page. It is useful to filter out in mTurk 
those participants who accepted the HIT but did not proceed further.

the timeout for consent form is set in Constants:

```python
    consent_timeout = int(environ.get('CONSENT_TIMEOUT', 15))
``` 
So you either can change the last number (15 seconds in this case),
or you can set the environmental variable. In heroku it is:

```
heroku config:set CONSENT_TIMEOUT=150
```

In this case it will be set to 150 seconds.

Author: Filipp Chapkovski, University of Zurich
