import pytest
from jinja2 import Environment


def assert_template_result(res, s, **ctx):
    tmpl = Environment().from_string(s)
    assert tmpl.render(**ctx) == res


@pytest.mark.liquid_unless
class TestLiquidUnless():
    """
    Tests taken from: https://github.com/Shopify/liquid/blob/64fca66ef5dfd7cf1acef0a7b8cdd825756eb681/test/integration/tags/unless_else_tag_test.rb
    """
    def test_unless(self, env):
        assert_template_result('  ', ' {% unless true %} this text should not go into the output {% endunless %} ')
        assert_template_result('  this text should go into the output  ',
        ' {% unless false %} this text should go into the output {% endunless %} ')
        assert_template_result('  you rock ?', '{% unless true %} you suck {% endunless %} {% unless false %} you rock {% endunless %}?')

    def test_unless_else(self, env):
        assert_template_result(' YES ', '{% unless true %} NO {% else %} YES {% endunless %}')
        assert_template_result(' YES ', '{% unless false %} YES {% else %} NO {% endunless %}')
        assert_template_result(' YES ', '{% unless "foo" %} NO {% else %} YES {% endunless %}')

    def test_unless_in_loop(self, env):
        assert_template_result('23', '{% for i in choices %}{% unless i %}{{ forloop.index }}{% endunless %}{% endfor %}', choices=[1, None, False])

    def test_unless_else_in_loop(self, env):
        assert_template_result(' TRUE  2  3 ', '{% for i in choices %}{% unless i %} {{ forloop.index }} {% else %} TRUE {% endunless %}{% endfor %}', choices=[1, None, False])
