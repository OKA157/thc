Trustable homomorphic computation
=================================

THC is a Python package that provides a practical framework for cost-effective trustable homomorphic computation.

It leverages the *modular extension* technique, which was developed to protect embedded cryptographic implementations against fault injection attacks, to ensure the integrity of a computation delegated to an untrusted third-party.

The paper describing THC has been accepted at [CANS 2021](https://cans2021.at/).
It can be found on the IACR ePrint Archive as [report 2021/1118](https://eprint.iacr.org/2021/1118).

## Installation

You can either install THC from [PyPI](https://pypi.org/project/thc/) using pip with the following command:

    $ pip3 install thc

Or you can download its [source code](https://code.up8.edu/pablo/thc) and run the following command in the root directory of the repository:

    $ pip3 install .

You can check that the installation went well by running the included test demo:

    $ python3 -m thc.demo.faults

## Dependencies

THC depends on the [pycryptodomex](https://pypi.org/project/pycryptodomex/) package to generate prime numbers.

You can probably install it using your distribution's package manager: it's the `python3-pycryptodome` package on Debian and derivatives.

If you choose to let pip install `pycryptodomex`, you will need to have some Python development packages installed as it needs to compile C extensions.
On Debian and derivatives, the necessary packages are named `python3-dev` and `python3-wheel`.

## Demo

In addition to the previously mentioned test demo of THC, an electronic voting software (server and client) is provided in the `thc.demo.evoting` package.

Please refer to its [README](https://code.up8.edu/pablo/thc/-/tree/master/thc/demo/evoting) for more information.
