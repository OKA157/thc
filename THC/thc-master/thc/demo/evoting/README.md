**NOTE:** This software is intended as a demo of the THC framework, it is **not** an endorsement of electronic voting in any particular form.

---

THC evoting
===========

THC evoting is an electronic voting platform which allows a group of agents (people or IoT devices) that are able to securely share a common secret to safely organize a secret ballot (i.e., no agent should be able to know what others voted) by making a third-party run the vote.

The idea is that the third-party is asked to run a server but is considered *completely untrustable*:

* vote metadata (e.g., the list of propositions) are protected using classic cryptography; and
* each agent's vote is protected using *homomorphic cryptography*, which allows the server to count the result of the vote.

THC is then used by the agents to verify the integrity of the vote count (i.e., that the third-party did not tamper with the vote results), and also to verify that each agent's vote is regular.


## Dependencies

### Server

The server has no dependencies other than the standard Python 3 library.

### Client

The client depends on:

* [PyNaCl](https://pynacl.readthedocs.io/)
* [requests](https://requests.readthedocs.io/)

It will also depend on a GUI toolkit soon, most likely [tkinter](https://docs.python.org/3/library/tkinter.html) as it comes bundled with Python.

If you plan to use the client, you can add the `evoting` extra to the pip install command in the root directory of the repository:

    $ pip3 install thc[evoting]


## Usage

If you specified the `evoting` extra when installing THC with pip, you can run the server with the following command (add `--help` to see options):

    $ thc_evoting-server

Otherwise, you can still run the server with (the same options are supported):

    $ python3 -m thc.demo.evoting.server

Similarly, the client can be called using the following command if you specified the `evoting` extra in the pip install command:

    $ thc_evoting-client --new # to create a new vote
    $ thc_evoting-client --file secret.thc # to participate to a vote

Otherwise, you can still call the client with:

    $ python3 -m thc.demo.evoting.client


## Server API

Responses are sent in JSON format with the `application/json` MIME type in the `Content-Type` header.

POST data is expected in standard `application/x-www-form-urlencoded` format, with an appropriate `Content-Length` header.

### `GET /`

Possible responses:

* 200 OK + server identity

Server identity:

<pre>
'THC demo e-voting server'
</pre>

### `POST /`

Required fields:

* `key`: unique string (urlsafe base64 valid)
* `mod`: modulus for server side computation (urlsafe base64 encoded)
* `title`: string (possibly encrypted, urlsafe base64 valid)
* `closing`: timestamp of vote closing date
* `expiry`: timestamp of vote expiring date
* `propositions`: string list (possibly encrypted, urlsafe base64 valid)

Possible responses:

* 303 See Other `/<vote_key>` + success message
* 400 Bad Request + error message
* 411 Length Required + error message
* 500 Internal Server Error + error message

### `GET /<vote_key>`

Possible responses:

* 200 OK + vote information
* 404 Not Found + error message

Vote information:

<pre>
{
    'title': '<i>vote title</i>',
    'closing': <i>timestamp of vote closing date</i>,
    'expiry': <i>timestamp of vote expiring date</i>,
    'propositions': [
        '<i>list</i>',
        '<i>of</i>',
        '<i>propositions</i>'
    ]
}
</pre>

### `POST /<vote_key>`

Required fields:

* `author`: string (possibly encrypted, urlsafe base64 valid)
* `votes`: vote list (Paillier encrypted, urlsafe base64 encoded values)
* `fingerprint`: string representation of JSON list of each vote's fingerprint (possibly encrypted, urlsafe base64 valid)

Possible responses:

* 303 See Other `/<vote_key>/ballot/<ballot_id>` + success message
* 400 Bad Request + error message
* 403 Forbidden + error message
* 404 Not Found + error message
* 411 Length Required + error message
* 500 Internal Server Error + error message

### `GET /<vote_key>/ballot/<ballot_id>`

Possible responses:

* 200 OK + ballot information
* 404 Not Found + error message

Ballot information:

<pre>
{
    'author': '<i>author</i>',
    'checksum': '<i>checksum</i>',
    'fingerprint': '<i>fingerprint</i>'
}
</pre>

Where *`checksum`* is the homomorphically computed sum of the votes in that ballot.

### `GET /<vote_key>/ballots`

Possible responses:

* 200 OK + list of ballots
* 403 Forbidden + error message
* 404 Not Found + error message

Ballots in the list are given in the same format as for individual ballot.

### `GET /<vote_key>/results`

Possible responses:

* 200 OK + results
* 403 Forbidden + error message
* 404 Not Found + error message

Results:

<pre>
[
    {
        'proposition': '<i>proposition</i>',
        'score': '<i>score</i>'
    },
    …
]
</pre>

Where *`score`* is the homomorphically computed sum of the votes for that proposition.
