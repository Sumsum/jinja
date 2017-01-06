import pytest
from jinja2 import Markup, Environment
from jinja2._compat import text_type, implements_to_string
from jinja2.filters import do_map


class ThingTest:
    def __init__(self):
        self.foo = 0

    def __str__(self):
        return "woot: {}".format(self.foo)

    def whatever(self):
        return str(self)

    def to_liquid(self):
        self.foo += 1


@pytest.mark.liquid_filter
class TestLiquidFilter():

    def test_abs(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L407
        """
        tmpl = env.from_string('{{ 17 | abs }}')
        assert tmpl.render() == '17'
        tmpl = env.from_string('{{ -17 | abs }}')
        assert tmpl.render() == '17'
        tmpl = env.from_string("{{ '17' | abs }}")
        assert tmpl.render() == '17'
        tmpl = env.from_string("{{ '-17' | abs }}")
        assert tmpl.render() == '17'
        tmpl = env.from_string("{{ 0 | abs }}")
        assert tmpl.render() == '0'
        tmpl = env.from_string("{{ '0' | abs }}")
        assert tmpl.render() == '0'
        tmpl = env.from_string("{{ 17.42 | abs }}")
        assert tmpl.render() == '17.42'
        tmpl = env.from_string("{{ -17.42 | abs }}")
        assert tmpl.render() == '17.42'
        tmpl = env.from_string("{{ '17.42' | abs }}")
        assert tmpl.render() == '17.42'
        tmpl = env.from_string("{{ '-17.42' | abs }}")
        assert tmpl.render() == '17.42'

    def test_append(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L486
        """
        ctx = {'a': 'bc', 'b': 'd'}
        tmpl = env.from_string("{{ a | append: 'd'}}")
        assert tmpl.render(**ctx) == 'bcd'
        tmpl = env.from_string("{{ a | append: b}}")
        assert tmpl.render(**ctx) == 'bcd'

    def test_capitalize(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/64fca66ef5dfd7cf1acef0a7b8cdd825756eb681/test/integration/filter_test.rb#L128
        """
        tmpl = env.from_string("{{ var | capitalize }}")
        assert tmpl.render(var='blub') == 'Blub'

    def test_ceil(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L466
        """
        tmpl = env.from_string("{{ input | ceil }}")
        assert tmpl.render(input=4.6) == '5'
        tmpl = env.from_string("{{ 4.3 | ceil }}")
        assert tmpl.render() == '5'
        tmpl = env.from_string("{{ 1.0 | divided_by: 0.0 | ceil }}")
        pytest.raises(ZeroDivisionError)
        tmpl = env.from_string("{{ price | ceil }}")
        assert tmpl.render(price='4.6') == '5'

    def test_divided_by(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L430
        """
        tmpl = env.from_string("{{ 12 | divided_by:3 }}")
        assert tmpl.render() == '4'
        tmpl = env.from_string("{{ 14 | divided_by:3 }}")
        assert tmpl.render() == '4'
        tmpl = env.from_string("{{ 15 | divided_by:3 }}")
        assert tmpl.render() == '5'
        tmpl = env.from_string("{{ 5 | divided_by:0 }}")
        pytest.raises(ZeroDivisionError)
        tmpl = env.from_string("{{ 2.0 | divided_by:4 }}")
        assert tmpl.render() == '0.5'
        tmpl = env.from_string("{{ 1 | modulo: 0 }}")
        pytest.raises(ZeroDivisionError)
        tmpl = env.from_string("{{ price | divided_by:2 }}")
        assert tmpl.render(price='10') == '5'

    def test_compact(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/64fca66ef5dfd7cf1acef0a7b8cdd825756eb681/test/integration/filter_test.rb#L101
        """
        tmpl = env.from_string("{{words | compact | join}}")
        assert tmpl.render(words=['a', None, 'b', None, 'c']) == 'a b c'
        tmpl = env.from_string("{{hashes | compact: 'a' | map: 'a' | join}}")
        assert tmpl.render(hashes=[{'a': 'A'}, {'a': None}, {'a': 'C'}]) == 'A C'

    def test_map(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L241
        """
        assert do_map([{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}], 'a') == [1, 2, 3, 4]
        tmpl = env.from_string("{{ ary | map:'foo' | map:'bar' }}")
        assert tmpl.render(ary=[{'foo': {'bar': 'a'}}, {'foo': {'bar': 'b'}}, {'foo': {'bar': 'c'}}]) == 'abc'

    def test_map_doesnt_call_arbitrary_stuff(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L247
        """
        tmpl = env.from_string('{{ "foo" | map: "__id__" }}')
        assert tmpl.render() == ''
        tmpl = env.from_string('{{ "foo" | map: "inspect" }}')
        assert tmpl.render() == ''

    def test_map_calls_to_liquid(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L252
        """
        tmpl = env.from_string('{{ foo | map: "whatever" }}')
        assert tmpl.render(foo=[ThingTest()]) == 'woot: 1'

    def test_map_on_dicts(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L257
        """
        tmpl = env.from_string('{{ thing | map: "foo" | map: "bar" }}')
        assert tmpl.render(thing={"foo": [{"bar": 42}, {"bar": 17}]}) == '4217'
