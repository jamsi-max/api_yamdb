from rest_framework.routers import Route, SimpleRouter


class CustomRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list'},
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/$',
            mapping={'post': 'create'},
            name='{basename}-create',
            initkwargs={'suffix': 'Create'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'put': 'update'},
            name='{basename}-update',
            initkwargs={'suffix': 'Update'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'delete': 'destroy'},
            name='{basename}-destroy',
            initkwargs={'suffix': 'Destroy'}
        ),
    ]
