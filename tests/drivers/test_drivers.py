import pytest

DRIVERS = ['sqlite']
DRIVER_CLASSES = {
    'sqlite': 'SQLiteDriver'
}


@pytest.mark.parametrize('provider', DRIVERS)
def test_creation(tmpdir, provider):
    from terracotta import drivers
    dbfile = tmpdir.join('test.sqlite')
    db = drivers.get_driver(str(dbfile), provider=provider)
    keys = ('some', 'keys')
    db.create(keys)

    assert db.key_names == keys
    assert db.get_datasets() == {}
    assert dbfile.isfile()


@pytest.mark.parametrize('provider', DRIVERS)
def test_creation_invalid(tmpdir, provider):
    from terracotta import drivers
    dbfile = tmpdir.join('test.sqlite')
    db = drivers.get_driver(str(dbfile), provider=provider)
    keys = ('invalid key',)

    with pytest.raises(ValueError):
        db.create(keys)


def test_creation_invalid_description(tmpdir, provider):
    from terracotta import drivers
    dbfile = tmpdir.join('test.sqlite')
    db = drivers.get_driver(str(dbfile), provider=provider)
    keys = ('some', 'keys')

    with pytest.raises(ValueError):
        db.create(keys, key_descriptions={'unknown_key': 'blah'})


@pytest.mark.parametrize('provider', DRIVERS)
def test_connect_before_create(tmpdir, provider):
    from terracotta import drivers, exceptions
    dbfile = tmpdir.join('test.sqlite')
    db = drivers.get_driver(str(dbfile), provider=provider)

    with pytest.raises(exceptions.InvalidDatabaseError):
        with db.connect():
            pass


@pytest.mark.parametrize('provider', DRIVERS)
def test_repr(tmpdir, provider):
    from terracotta import drivers
    dbfile = tmpdir.join('test.sqlite')
    db = drivers.get_driver(str(dbfile), provider=provider)
    assert repr(db) == f'{DRIVER_CLASSES[provider]}(\'{dbfile}\')'
