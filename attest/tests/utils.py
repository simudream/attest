from __future__ import with_statement
from attest import Tests, assert_hook, utils, disable_imports, raises
import attest
from attest.utils import import_dotted_name

suite = Tests()


@suite.test
def terminal_size():
    size = utils.get_terminal_size()
    assert type(size) is tuple
    assert len(size) == 2
    assert type(size[0]) is int
    assert type(size[1]) is int

    with disable_imports('fcntl', 'termios'):
        size = utils.get_terminal_size()
        assert size == (80, 24)
        size = utils.get_terminal_size((1, 2))
        assert size == (1, 2)


@suite.test
def string_importing():
    assert import_dotted_name('attest') is attest
    assert import_dotted_name('attest.tests') is attest.tests
    assert import_dotted_name('attest.utils') is utils
    assert import_dotted_name('attest.utils:import_dotted_name') \
           is import_dotted_name
    assert import_dotted_name('attest.utils.import_dotted_name') \
           is import_dotted_name


    with raises(AttributeError):
        import_dotted_name('attest._nil')

    with raises(ImportError):
        with disable_imports('attest'):
            import_dotted_name('attest')


@suite.test
def iter_mods():
    core = ['attest.' + mod for mod in
            '''ast codegen collectors contexts deprecated hook __main__ reporters
               run statistics utils'''.split()]
    tests = ['attest.tests.' + mod for mod in
              '''asserts classy collectors contexts hook _meta reporters
                 utils'''.split()]

    found = list(utils.deep_iter_modules('attest'))
    expected = core + tests
    assert set(expected) == set(found)
    assert len(expected) == len(found)

    found = list(utils.deep_iter_modules('attest.tests'))
    expected = tests
    assert set(expected) == set(found)
    assert len(expected) == len(found)

    found = list(utils.deep_iter_modules('attest.ast'))
    assert found == ['attest.ast']

    with raises(AttributeError):
        list(utils.deep_iter_modules('attest._nil'))

    with disable_imports('attest'):
        with raises(ImportError):
            list(utils.deep_iter_modules('attest'))


@suite.test
def get_members_recursively():
    deepfunc = lambda x: getattr(x, '__name__', '').startswith('deep_')
    found = list(utils.deep_get_members('attest', deepfunc))
    expected = [utils.deep_get_members, utils.deep_iter_modules]
    assert found == expected


@suite.test
def reporter_options():
    opts = utils.parse_options([
        'style = dark',
        'verbose=yes',
        'quiet=no',
        'switch=on',
        'bigbutton=off',
        'bool=true',
        'lie=false',
        'num=3',
        'list=1,2,3',
        'pair=foo:bar',
        'dict=foo:bar,abc:123',
        'notopt',
        'empty=',
        'hyphens-are-ok=true',
    ])

    assert opts == dict(
        style='dark',
        verbose=True,
        quiet=False,
        switch=True,
        bigbutton=False,
        bool=True,
        lie=False,
        num=3,
        list=(1, 2, 3),
        pair=('foo', 'bar'),
        dict=dict(foo='bar', abc=123),
        empty=None,
        hyphens_are_ok=True,
    )