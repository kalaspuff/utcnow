def test_init() -> None:
    import utcnow
    from utcnow import __version__, __version_info__

    assert utcnow

    assert isinstance(utcnow.__version_info__, tuple)
    assert utcnow.__version_info__
    assert isinstance(utcnow.__version__, str)
    assert len(utcnow.__version__)

    assert isinstance(__version_info__, tuple)
    assert __version_info__
    assert isinstance(__version__, str)
    assert len(__version__)

    from utcnow.__version__ import __version__ as __version2__, __version_info__ as __version_info2__  # noqa  # isort:skip

    assert isinstance(__version_info2__, tuple)
    assert __version_info2__
    assert isinstance(__version2__, str)
    assert len(__version2__)
