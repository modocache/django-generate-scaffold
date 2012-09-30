VERSION = (0, 0, 5, 'alpha', 0)

def get_version(version=None):
    """
    Derives a PEP386-compliant verison number
    from VERSION.
    """
    if version is None:
        version = VERSION
    assert len(version) == 5
    assert version[3] in ("alpha", "beta", "rc", "final")

    parts = 2 if version[2] == 0 else 3
    main = ".".join(str(digit) for digit in version[:parts])

    sub = ""
    if version[3] != "final":
        mapping = {"alpha": "a", "beta": "b", "rc": "rc"}
        sub = mapping[version[3]] + str(version[4])

    return main + sub
