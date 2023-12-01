Push support
============


Introduction
~~~~~~~~~~~~

Extrawest OCPI supports push. This means that changes in objects and
new objects are sent (semi) real-time to the receiver.

As for now you are able to specify on application initialization two parameters:
`http_push` or `websocket_push`.

If set `http_push=True` new endpoint will be added into the schema:
 - PUSH_PREFIX/{version}

which you'll be able to use for sending the updates about your objects to.

.. warning::

    It's advised not to expose this endpoint (For internal usage only).

.. note::

    Uses authorization header!

If set `websocket_push=True` new websocket endpoint will be added into the schema:
 - PUSH_PREFIX/ws/{version}

which you'll be able to use for sending the updates about your objects to.

.. note::
    Uses `token` query_parameter for authentication!


Extended initialization example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

main.py

.. code-block:: python

    from py_ocpi import get_application
    from py_ocpi.core.enums import RoleEnum, ModuleID
    from py_ocpi.modules.versions.enums import VersionNumber

    from auth import ClientAuthenticator
    from crud import Crud


    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[RoleEnum.cpo],
        modules=[ModuleID.locations],
        authenticator=ClientAuthenticator,
        crud=Crud,
        http_push=True,
        websocket_push=True,
    )


Http push url example
~~~~~~~~~~~~~~~~~~~~~

`http://127.0.0.1:8000/push/2.1.1`

Connect to ws url example
~~~~~~~~~~~~~~~~~~~~~~~~~

`ws://127.0.0.1:8000/push/ws/2.1.1?token=<your-valid-token>`
