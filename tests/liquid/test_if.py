import pytest
from jinja2 import Environment
from jinja2.exceptions import UndefinedError


def assert_template_result(res, s, **ctx):
    tmpl = Environment().from_string(s)
    assert tmpl.render(**ctx) == res


@pytest.mark.liquid_if
class TestLiquidIf():
    """
    Tests taken from: https://github.com/Shopify/liquid/blob/64fca66ef5dfd7cf1acef0a7b8cdd825756eb681/test/integration/tags/if_else_tag_test.rb
    """

    def test_if(self, env):
        assert_template_result('  ', ' {% if false %} this text should not go into the output {% endif %} ')
        assert_template_result('  this text should go into the output  ',
        ' {% if true %} this text should go into the output {% endif %} ')
        assert_template_result('  you rock ?', '{% if false %} you suck {% endif %} {% if true %} you rock {% endif %}?')

    def test_literal_comparisons(self, env):
        assert_template_result(' NO ', '{% assign v = false %}{% if v %} YES {% else %} NO {% endif %}')
        assert_template_result(' YES ', '{% assign v = nil %}{% if v == nil %} YES {% else %} NO {% endif %}')

    def test_if_else(self, env):
        assert_template_result(' YES ', '{% if false %} NO {% else %} YES {% endif %}')
        assert_template_result(' YES ', '{% if true %} YES {% else %} NO {% endif %}')
        assert_template_result(' YES ', '{% if "foo" %} YES {% else %} NO {% endif %}')

    def test_if_boolean(self, env):
        assert_template_result(' YES ', '{% if var %} YES {% endif %}', var=True)

    def test_if_or(self, env):
        assert_template_result(' YES ', '{% if a or b %} YES {% endif %}', a=True, b=True)
        assert_template_result(' YES ', '{% if a or b %} YES {% endif %}', a=True, b=False)
        assert_template_result(' YES ', '{% if a or b %} YES {% endif %}', a=False, b=True)
        assert_template_result('', '{% if a or b %} YES {% endif %}', a=False, b=False)

        assert_template_result(' YES ', '{% if a or b or c %} YES {% endif %}', a=False, b=False, c=True)
        assert_template_result('', '{% if a or b or c %} YES {% endif %}', a=False, b=False, c=False)

    def test_if_or_with_operators(self, env):
        assert_template_result(' YES ', '{% if a == true or b == true %} YES {% endif %}', a=True, b=True)
        assert_template_result(' YES ', '{% if a == true or b == false %} YES {% endif %}', a=True, b=True)
        assert_template_result('', '{% if a == false or b == false %} YES {% endif %}', a=True, b=True)

    def test_comparison_of_strings_containing_and_or_or(self, env):
        awful_markup = "a == 'and' and b == 'or' and c == 'foo and bar' and d == 'bar or baz' and e == 'foo' and foo and bar"
        assigns = {'a': 'and', 'b': 'or', 'c': 'foo and bar', 'd': 'bar or baz', 'e': 'foo', 'foo': True, 'bar': True}
        assert_template_result(' YES ', "{{% if {} %}} YES {{% endif %}}".format(awful_markup), **assigns)

    def test_comparison_of_expressions_starting_with_and_or_or(self, env):
        assigns = {'order': {'items_count': 0}, 'android': {'name': 'Roy'}}
        assert_template_result("YES", "{% if android.name == 'Roy' %}YES{% endif %}", **assigns)
        assert_template_result("YES", "{% if order.items_count == 0 %}YES{% endif %}", **assigns)

    def test_if_and(self, env):
        assert_template_result(' YES ', '{% if true and true %} YES {% endif %}')
        assert_template_result('', '{% if false and true %} YES {% endif %}')
        assert_template_result('', '{% if false and true %} YES {% endif %}')

    def test_hash_miss_generates_false(self, env):
        assert_template_result('', '{% if foo.bar %} NO {% endif %}', foo={})

    def test_if_from_variable(self, env):
        assert_template_result('', '{% if var %} NO {% endif %}', var=False)
        assert_template_result('', '{% if var %} NO {% endif %}', var=None)
        assert_template_result('', '{% if foo.bar %} NO {% endif %}', foo={'bar': False})
        assert_template_result('', '{% if foo.bar %} NO {% endif %}', foo={})
        assert_template_result('', '{% if foo.bar %} NO {% endif %}', foo=None)
        assert_template_result('', '{% if foo.bar %} NO {% endif %}', foo=True)

        assert_template_result(' YES ', '{% if var %} YES {% endif %}', var="text")
        assert_template_result(' YES ', '{% if var %} YES {% endif %}', var=True)
        assert_template_result(' YES ', '{% if var %} YES {% endif %}', var=1)
        #assert_template_result(' YES ', '{% if var %} YES {% endif %}', var={})
        # changed for expected result in jinja/python
        assert_template_result('', '{% if var %} YES {% endif %}', var={})
        #assert_template_result(' YES ', '{% if var %} YES {% endif %}', var=[])
        # changed for expected result in jinja/python
        assert_template_result('', '{% if var %} YES {% endif %}', var=[])
        assert_template_result(' YES ', '{% if "foo" %} YES {% endif %}')
        assert_template_result(' YES ', '{% if foo.bar %} YES {% endif %}', foo={'bar': True})
        assert_template_result(' YES ', '{% if foo.bar %} YES {% endif %}', foo={'bar': "text"})
        assert_template_result(' YES ', '{% if foo.bar %} YES {% endif %}', foo={'bar': 1})
        #assert_template_result(' YES ', '{% if foo.bar %} YES {% endif %}', foo={'bar': {}})
        # changed for expected result in jinja/python
        assert_template_result('', '{% if foo.bar %} YES {% endif %}', foo={'bar': {}})
        #assert_template_result(' YES ', '{% if foo.bar %} YES {% endif %}', foo={'bar': []})
        # changed for expected result in jinja/python
        assert_template_result('', '{% if foo.bar %} YES {% endif %}', foo={'bar': []})

        assert_template_result(' YES ', '{% if var %} NO {% else %} YES {% endif %}', var=False)
        assert_template_result(' YES ', '{% if var %} NO {% else %} YES {% endif %}', var=None)
        assert_template_result(' YES ', '{% if var %} YES {% else %} NO {% endif %}', var=True)
        assert_template_result(' YES ', '{% if "foo" %} YES {% else %} NO {% endif %}', var="text")

        assert_template_result(' YES ', '{% if foo.bar %} NO {% else %} YES {% endif %}', foo={'bar': False})
        assert_template_result(' YES ', '{% if foo.bar %} YES {% else %} NO {% endif %}', foo={'bar': True})
        assert_template_result(' YES ', '{% if foo.bar %} YES {% else %} NO {% endif %}', foo={'bar': "text"})
        assert_template_result(' YES ', '{% if foo.bar %} NO {% else %} YES {% endif %}', foo={'notbar': True})
        assert_template_result(' YES ', '{% if foo.bar %} NO {% else %} YES {% endif %}', foo={})
        with pytest.raises(UndefinedError):
            assert_template_result(' YES ', '{% if foo.bar %} NO {% else %} YES {% endif %}', notfoo={'bar': True})

    def test_nested_if(self, env):
        assert_template_result('', '{% if false %}{% if false %} NO {% endif %}{% endif %}')
        assert_template_result('', '{% if false %}{% if true %} NO {% endif %}{% endif %}')
        assert_template_result('', '{% if true %}{% if false %} NO {% endif %}{% endif %}')
        assert_template_result(' YES ', '{% if true %}{% if true %} YES {% endif %}{% endif %}')

        assert_template_result(' YES ', '{% if true %}{% if true %} YES {% else %} NO {% endif %}{% else %} NO {% endif %}')
        assert_template_result(' YES ', '{% if true %}{% if false %} NO {% else %} YES {% endif %}{% else %} NO {% endif %}')
        assert_template_result(' YES ', '{% if false %}{% if true %} NO {% else %} NONO {% endif %}{% else %} YES {% endif %}')

    # Not sure this is useful feature
    #def test_comparisons_on_null(self, env):
    #    assert_template_result('', '{% if None < 10 %} NO {% endif %}')
    #    assert_template_result('', '{% if None <= 10 %} NO {% endif %}')
    #    assert_template_result('', '{% if None >= 10 %} NO {% endif %}')
    #    assert_template_result('', '{% if None > 10 %} NO {% endif %}')

    #    assert_template_result('', '{% if 10 < None %} NO {% endif %}')
    #    assert_template_result('', '{% if 10 <= None %} NO {% endif %}')
    #    assert_template_result('', '{% if 10 >= None %} NO {% endif %}')
    #    assert_template_result('', '{% if 10 > None %} NO {% endif %}')

    def test_else_if(self, env):
        assert_template_result('0', '{% if 0 == 0 %}0{% elsif 1 == 1%}1{% else %}2{% endif %}')
        assert_template_result('1', '{% if 0 != 0 %}0{% elsif 1 == 1%}1{% else %}2{% endif %}')
        assert_template_result('2', '{% if 0 != 0 %}0{% elsif 1 != 1%}1{% else %}2{% endif %}')

        assert_template_result('elsif', '{% if false %}if{% elsif true %}elsif{% endif %}')

    def test_multiple_conditions(self, env):
        tpl = "{% if a or b and c %}true{% else %}false{% endif %}"

        tests = (
            ([True, True, True], True),
            ([True, True, False], True),
            ([True, False, True], True),
            ([True, False, False], True),
            ([False, True, True], True),
            ([False, True, False], False),
            ([False, False, True], False),
            ([False, False, False], False),
        )
        for vals, expected in tests:
            a, b, c = vals
            assigns = {'a': a, 'b': b, 'c': c}
            assert_template_result(str(expected).lower(), tpl, **assigns)
