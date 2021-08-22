import pytest
from myapp.run import app
from myapp.celery import async_request

@pytest.fixture(scope='session')
def app(request):
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app_


@pytest.fixture(scope='session')
def celery_app(app):
    from myapp import celery
    from celery.contrib.testing import tasks
    return celery    

def test_async_request_function(celery_app, celery_worker):
    async_result = async_request.delay()
    assert len(async_result.get()) == 3