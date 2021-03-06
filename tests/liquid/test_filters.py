import datetime
import dateutil.parser
import pytest
from jinja2.filters import FILTERS
from jinja2.nodes import EvalContext


class ThingTest:
    def __init__(self):
        self.foo = 0

    def __str__(self):
        return "woot: {}".format(self.foo)

    def whatever(self):
        return str(self)

    def to_liquid(self):
        self.foo += 1


class ObjectTest:
    def __init__(self, a):
        self.a = a


class DropTest:
    def test(self):
        return "testfoo"


def assert_equal(a, b):
    assert a == b


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

    def test_date(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L311
        """
        date = FILTERS['date']
        assert_equal('May', date(dateutil.parser.parse("2006-05-05 10:00:00"), "%B"))
        assert_equal('June', date(dateutil.parser.parse("2006-06-05 10:00:00"), "%B"))
        assert_equal('July', date(dateutil.parser.parse("2006-07-05 10:00:00"), "%B"))

        assert_equal('May', date("2006-05-05 10:00:00", "%B"))
        assert_equal('June', date("2006-06-05 10:00:00", "%B"))
        assert_equal('July', date("2006-07-05 10:00:00", "%B"))

        assert_equal('2006-07-05 10:00:00', date("2006-07-05 10:00:00", ""))
        assert_equal('2006-07-05 10:00:00', date("2006-07-05 10:00:00", None))

        assert_equal('07/05/2006', date("2006-07-05 10:00:00", "%m/%d/%Y"))

        assert_equal("07/16/2004", date("Fri Jul 16 01:00:00 2004", "%m/%d/%Y"))
        assert_equal(str(datetime.date.today().year), date('now', '%Y'))
        assert_equal(str(datetime.date.today().year), date('today', '%Y'))
        assert_equal(str(datetime.date.today().year), date('Today', '%Y'))

        assert_equal(None, date(None, "%B"))

        assert_equal('', date('', "%B"))

        assert_equal("07/05/2006", date(1152098955, "%m/%d/%Y"))
        assert_equal("07/05/2006", date("1152098955", "%m/%d/%Y"))

    def test_default(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L508
        """
        default = FILTERS['default']
        assert_equal("foo", default("foo", "bar"))
        assert_equal("bar", default(None, "bar"))
        assert_equal("bar", default("", "bar"))
        assert_equal("bar", default(False, "bar"))
        assert_equal("bar", default([], "bar"))
        assert_equal("bar", default({}, "bar"))

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
        assert FILTERS['map']([{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}], 'a') == [1, 2, 3, 4]
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

    def test_downcase(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L67
        """
        assert FILTERS['downcase']('Testing') == 'testing'
        assert FILTERS['downcase'](None) == ''

    def test_escape(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L129
        """
        assert FILTERS['escape']('<strong>') == '&lt;strong&gt;'
        assert FILTERS['escape'](None) is None

    def test_escape_once(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L135
        """
        assert FILTERS['escape_once']('&lt;strong&gt;Hulk</strong>') == '&lt;strong&gt;Hulk&lt;/strong&gt;'

    def test_floor(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L476
        """
        tmpl = env.from_string('{{ input | floor }}')
        assert tmpl.render(input=4.6) == '4'
        tmpl = env.from_string("{{ '4.3' | floor }}")
        assert tmpl.render() == '4'
        tmpl = env.from_string("{{ 1.0 | divided_by: 0.0 | floor }}")
        pytest.raises(ZeroDivisionError)

    def test_join(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L170
        """
        eval_ctx = EvalContext(env)
        assert FILTERS['join'](eval_ctx, [1, 2, 3, 4]) == '1 2 3 4'
        assert FILTERS['join'](eval_ctx, [1, 2, 3, 4], ' - ') == '1 - 2 - 3 - 4'

    def test_lstrip(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L374
        """
        tmpl = env.from_string('{{ source | lstrip }}')
        assert tmpl.render(source=' ab c  ') == 'ab c  '
        tmpl = env.from_string('{{ source | lstrip }}')
        assert tmpl.render(source=' \tab c  \n \t') == 'ab c  \n \t'

    def test_rstrip(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L379
        """
        tmpl = env.from_string('{{ source | rstrip }}')
        assert tmpl.render(source=' ab c  ') == ' ab c'
        tmpl = env.from_string('{{ source | rstrip }}')
        assert tmpl.render(source=' \tab c  \n \t') == ' \tab c'

    def test_minus(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L400
        """
        tmpl = env.from_string('{{ input | minus:operand }}')
        assert tmpl.render(input=5, operand=1) == '4'
        tmpl = env.from_string("{{ '4.3' | minus:'2' }}")
        assert tmpl.render() == '2.3'

    def test_modulo(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L445
        """
        tmpl = env.from_string("{{ 3 | modulo:2 }}")
        assert tmpl.render() == '1'
        tmpl = env.from_string("{{ 1 | modulo: 0 }}")
        pytest.raises(ZeroDivisionError)
        tmpl = env.from_string("{{ price | modulo:2 }}")
        assert tmpl.render(price='3') == '1'

    def test_newline_to_br(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L389
        """
        tmpl = env.from_string("{{ source | newline_to_br }}")
        assert tmpl.render(source='a\nb\nc') == 'a<br />\nb<br />\nc'

    def test_plus(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L393
        """
        tmpl = env.from_string('{{ 1 | plus:1 }}')
        assert tmpl.render() == '2'
        tmpl = env.from_string("{{ '1' | plus:'1.0' }}")
        assert tmpl.render() == '2.0'
        tmpl = env.from_string("{{ price | plus:'2' }}")
        assert tmpl.render(price='3') == '5'

    def test_prepend(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L502
        """
        tmpl = env.from_string("{{ a | prepend: 'a'}}")
        assert tmpl.render(a='bc', b='a') == 'abc'
        tmpl = env.from_string("{{ a | prepend: b}}")
        assert tmpl.render(a='bc', b='a') == 'abc'

    def test_remove(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L357
        """
        eval_ctx = EvalContext(env)
        remove = FILTERS['remove']
        assert remove(eval_ctx, "a a a a", 'a') == '   '
        assert remove(eval_ctx, "1 1 1 1", 1) == '   '

    def test_remove_first(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L360
        """
        eval_ctx = EvalContext(env)
        remove_first = FILTERS['remove_first']
        assert remove_first(eval_ctx, "a a a a", 'a ') == 'a a a'
        assert remove_first(eval_ctx, "1 1 1 1", 1) == ' 1 1 1'
        tmpl = env.from_string("{{ 'a a a a' | remove_first: 'a ' }}")
        assert tmpl.render() == 'a a a'

    def test_replace(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L349
        """
        eval_ctx = EvalContext(env)
        replace = FILTERS['replace']
        assert replace(eval_ctx, '1 1 1 1', '1', 2) == '2 2 2 2'
        assert replace(eval_ctx, '1 1 1 1', 1, 2) == '2 2 2 2'

    def test_replace_first(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L352
        """
        eval_ctx = EvalContext(env)
        replace_first = FILTERS['replace_first']
        assert replace_first(eval_ctx, '1 1 1 1', '1', 2) == '2 1 1 1'
        assert replace_first(eval_ctx, '1 1 1 1', 1, 2) == '2 1 1 1'
        tmpl = env.from_string("{{ '1 1 1 1' | replace_first: '1', 2 }}")
        assert tmpl.render() == '2 1 1 1'

    def test_reverse(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L233
        """
        reverse = FILTERS['reverse']
        assert reverse([1, 2, 3, 4]) == [4, 3, 2, 1]

    def test_round(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L454
        """
        tmpl = env.from_string("{{ input | round }}")
        assert tmpl.render(input=4.6) == '5'
        tmpl = env.from_string("{{ '4.3' | round }}")
        assert tmpl.render() == '4'
        tmpl = env.from_string("{{ input | round: 2 }}")
        assert tmpl.render(input=4.5612) == '4.56'
        tmpl = env.from_string("{{ 1.0 | divided_by: 0.0 | round }}")
        pytest.raises(ZeroDivisionError)

    def test_size(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L61
        """
        size = FILTERS['size']
        assert size([1, 2, 3]) == 3
        assert size([]) == 0
        assert size(None) == 0

    def test_slice(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L77
        """
        slice = FILTERS['slice']
        assert slice('foobar', 1, 3) == 'oob'
        assert slice('foobar', 1, 1000) == 'oobar'
        assert slice('foobar', 1, 0) == ''
        assert slice('foobar', 1, 1) == 'o'
        assert slice('foobar', 3, 3) == 'bar'
        assert slice('foobar', -2, 2) == 'ar'
        assert slice('foobar', -2, 1000) == 'ar'
        assert slice('foobar', -1) == 'r'
        assert slice(None, 0) == ''
        assert slice('foobar', 100, 10) == ''
        assert slice('foobar', -100, 10) == ''
        assert slice('foobar', '1', '3') == 'oob'
        with pytest.raises(TypeError):
            slice('foobar', None)
        with pytest.raises(ValueError):
            slice('foobar', 0, "")

    def test_sort(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L175
        """
        sort = FILTERS['sort']
        assert sort(env, [4, 3, 2, 1]) == [1, 2, 3, 4]
        assert sort(env, [{"a": 4}, {"a": 3}, {"a": 1}, {"a": 2}], "a") == [{"a": 1}, {"a": 2}, {"a": 3}, {"a": 4}]

    def test_sort_integration(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/64fca66ef5dfd7cf1acef0a7b8cdd825756eb681/test/integration/filter_test.rb#L72
        """
        context = {}
        context['value'] = 3
        context['numbers'] = [2, 1, 4, 3]
        context['words'] = ['expected', 'as', 'alphabetic']
        context['arrays'] = ['flower', 'are']
        context['case_sensitive'] = ['sensitive', 'Expected', 'case']

        tmpl = env.from_string("{{numbers | sort | join}}")
        assert tmpl.render(**context) == '1 2 3 4'
        tmpl = env.from_string("{{words | sort | join}}")
        assert tmpl.render(**context) == 'alphabetic as expected'
        tmpl = env.from_string("{{value | sort}}")
        assert tmpl.render(**context) == '3'
        tmpl = env.from_string("{{arrays | sort | join}}")
        assert tmpl.render(**context) == 'are flower'
        tmpl = env.from_string("{{case_sensitive | sort | join}}")
        assert tmpl.render(**context) == 'Expected case sensitive'

    def test_sort_natural(self, env):
        """
        Tests taken from: https://github.com/Shopify/liquid/blob/64fca66ef5dfd7cf1acef0a7b8cdd825756eb681/test/integration/filter_test.rb#L86
        """
        context = {}
        context['words'] = ['case', 'Assert', 'Insensitive']
        context['hashes'] = [{'a': 'A'}, {'a': 'b'}, {'a': 'C'}]
        context['objects'] = [ObjectTest('A'), ObjectTest('b'), ObjectTest('C')]

        tmpl = env.from_string("{{words | sort_natural | join}}")
        assert tmpl.render(**context) == 'Assert case Insensitive'
        tmpl = env.from_string("{{hashes | sort_natural: 'a' | map: 'a' | join}}")
        assert tmpl.render(**context) == 'A b C'
        tmpl = env.from_string("{{objects | sort_natural: 'a' | map: 'a' | join}}")
        assert tmpl.render(**context) == 'A b C'

    def test_split(self, env):
        """
        Test taken from; https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L121
        """
        split = FILTERS['split']
        assert split('12~34', '~') == ['12', '34']
        assert split('A? ~ ~ ~ ,Z', '~ ~ ~') == ['A? ', ' ,Z']
        assert split('A?Z', '~') == ['A?Z']
        assert split(None, ' ') == []
        assert split('A1Z', 1) == ['A', 'Z']

    def test_strip(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L369
        """
        tmpl = env.from_string("{{ source | strip }}")
        assert tmpl.render(source=" ab c  ") == 'ab c'
        tmpl = env.from_string("{{ source | strip }}")
        assert tmpl.render(source=" \tab c  \n \t") == 'ab c'

    def test_strip_html(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L160
        """
        strip_html = FILTERS['strip_html']
        assert strip_html("<div>test</div>") == 'test'
        assert strip_html("<div id='test'>test</div>") == 'test'
        assert strip_html("<script type='text/javascript'>document.write('some stuff');</script>") == ''
        assert strip_html("<style type='text/css'>foo bar</style>") == ''
        assert strip_html("<div\nclass='multiline'>test</div>") == 'test'
        assert strip_html("<!-- foo bar \n test -->test") == 'test'
        assert strip_html(None) == ''

    def test_strip_newlines(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L384
        """
        tmpl = env.from_string("{{ source | strip_newlines }}")
        assert tmpl.render(source="a\nb\nc") == 'abc'
        tmpl = env.from_string("{{ source | strip_newlines }}")
        assert tmpl.render(source="a\r\nb\nc") == 'abc'

    def test_times(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L420
        """
        def assert_template_result(res, s, **ctx):
            tmpl = env.from_string(s)
            assert tmpl.render(**ctx) == res

        assert_template_result("12", "{{ 3 | times:4 }}")
        assert_template_result("0", "{{ 'foo' | times:4 }}")
        # I have no plans to make such a stupid test work
        #assert_template_result("6", "{{ '2.1' | times:3 | replace: '.','-' | plus:0}}")
        assert_template_result("7.25", "{{ 0.0725 | times:100 }}")
        assert_template_result("-7.25", '{{ "-0.0725" | times:100 }}')
        assert_template_result("7.25", '{{ "-0.0725" | times: -100 }}')
        assert_template_result("4", "{{ price | times:2 }}", price='2')

    def test_truncate(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L112

        Tests have been changed to adapt to jinja truncate, where there is a
        default tolerance of 5 characters, that is strings that only exceed the
        length by the tolerance margin given in the leeway parameter will not
        be truncated.
        """

        truncate = FILTERS['truncate']
        assert_equal('1234567890', truncate(env, '1234567890', 7))
        assert_equal('1234...', truncate(env, '123456789012345678', 7))
        assert_equal('1234567890', truncate(env, '1234567890', 20))
        assert_equal('...', truncate(env, '1234567890', 0))
        assert_equal('1234567890', truncate(env, '1234567890'))
        assert_equal("测试...", truncate(env, "测试测试测试测试测试测试测试测试", 5))
        assert_equal('12341', truncate(env, "1234567890123456", 5, 1))

    def test_truncate_words(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L151
        """
        truncatewords = FILTERS['truncatewords']
        assert_equal('one two three', truncatewords('one two three', 4))
        assert_equal('one two...', truncatewords('one two three', 2))
        assert_equal('one two three', truncatewords('one two three'))
        assert_equal('Two small (13&#8221; x 5.5&#8221; x 10&#8221; high) baskets fit inside one large basket (13&#8221;...', truncatewords('Two small (13&#8221; x 5.5&#8221; x 10&#8221; high) baskets fit inside one large basket (13&#8221; x 16&#8221; x 10.5&#8221; high) with cover.', 15))
        assert_equal("测试测试测试测试", truncatewords('测试测试测试测试', 5))
        assert_equal('one two1', truncatewords("one two three", 2, 1))

    def test_uniq(self, env):
        """
        Test taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L217
        """
        uniq = FILTERS['uniq']
        assert_equal(["foo"], uniq("foo"))
        assert_equal([1, 3, 2, 4], uniq([1, 1, 3, 2, 3, 1, 4, 3, 2, 1]))
        assert_equal([{"a": 1}, {"a": 3}, {"a": 2}], uniq([{"a": 1}, {"a": 3}, {"a": 1}, {"a": 2}], "a"))
        droptest = DropTest()
        assert_equal([droptest], uniq([droptest, DropTest()], 'test'))

    def test_upcase(self, env):
        """
        Tests taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L72
        """
        upcase = FILTERS['upcase']
        assert_equal('TESTING', upcase("Testing"))
        assert_equal('', upcase(None))

    def test_url_decode(self, env):
        """
        Tests taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L144
        """
        url_decode = FILTERS['url_decode']
        assert_equal('foo bar', url_decode('foo+bar'))
        assert_equal('foo bar', url_decode('foo%20bar'))
        assert_equal('foo+1@example.com', url_decode('foo%2B1%40example.com'))
        assert_equal(None, url_decode(None))

    def test_url_encode(self, env):
        """
        Tests taken from: https://github.com/Shopify/liquid/blob/b2feeacbce8e4a718bde9bc9fa9d00e44ab32351/test/integration/standard_filter_test.rb#L139
        """
        url_encode = FILTERS['url_encode']
        assert_equal('foo%2B1%40example.com', url_encode('foo+1@example.com'))
        assert_equal(None, url_encode(None))
