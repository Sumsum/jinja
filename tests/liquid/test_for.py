import pytest
from jinja2 import Environment
from jinja2.exceptions import TemplateSyntaxError


def assert_template_result(res, s, **ctx):
    tmpl = Environment().from_string(s)
    assert tmpl.render(**ctx) == res


class ThingWithValue:
    value = 3


@pytest.mark.liquid_for
class TestLiquidFor():
    """
    Tests taken from: https://github.com/Shopify/liquid/blob/64fca66ef5dfd7cf1acef0a7b8cdd825756eb681/test/integration/tags/for_tag_test.rb
    """

    def test_for(self, env):
        assert_template_result(' yo  yo  yo  yo ', '{%for item in array%} yo {%endfor%}', array=[1, 2, 3, 4])
        assert_template_result('yoyo', '{%for item in array%}yo{%endfor%}', array=[1, 2])
        assert_template_result(' yo ', '{%for item in array%} yo {%endfor%}', array=[1])
        assert_template_result('', '{%for item in array%}{%endfor%}', array=[1, 2])
        expected = """

  yo

  yo

  yo
"""
        template = """
{%for item in array%}
  yo
{%endfor%}
"""
        assert_template_result(expected, template, array=[1, 2, 3])

    def test_for_reversed(self, env):
        assigns = {'array': [1, 2, 3]}
        assert_template_result('321', '{%for item in array reversed %}{{item}}{%endfor%}', **assigns)

    def test_for_with_range(self, env):
        assert_template_result(' 1  2  3 ', '{%for item in (1..3) %} {{item}} {%endfor%}')
        with pytest.raises(TypeError):
            assert_template_result('', '{% for i in (a..2) %}{% endfor %}', a=[1, 2])
        assert_template_result(' 0  1  2  3 ', '{% for item in (a..3) %} {{item}} {% endfor %}', a="invalid integer")

    def test_for_with_variable_range(self, env):
        assert_template_result(' 1  2  3 ', '{%for item in (1..foobar) %} {{item}} {%endfor%}', foobar=3)

    def test_for_with_hash_value_range(self, env):
        foobar = {"value": 3}
        assert_template_result(' 1  2  3 ', '{%for item in (1..foobar.value) %} {{item}} {%endfor%}', foobar=foobar)

    def test_for_with_drop_value_range(self, env):
        foobar = ThingWithValue()
        assert_template_result(' 1  2  3 ', '{%for item in (1..foobar.value) %} {{item}} {%endfor%}', foobar=foobar)

    def test_for_with_variable(self, env):
        assert_template_result(' 1  2  3 ', '{%for item in array%} {{item}} {%endfor%}', array=[1, 2, 3])
        assert_template_result('123', '{%for item in array%}{{item}}{%endfor%}', array=[1, 2, 3])
        assert_template_result('123', '{% for item in array %}{{item}}{% endfor %}', array=[1, 2, 3])
        assert_template_result('abcd', '{%for item in array%}{{item}}{%endfor%}', array=['a', 'b', 'c', 'd'])
        assert_template_result('a b c', '{%for item in array%}{{item}}{%endfor%}', array=['a', ' ', 'b', ' ', 'c'])
        assert_template_result('abc', '{%for item in array%}{{item}}{%endfor%}', array=['a', '', 'b', '', 'c'])

    def test_for_helpers(self, env):
        assigns = {'array': [1, 2, 3]}
        assert_template_result(
            ' 1/3  2/3  3/3 ',
            '{%for item in array%} {{forloop.index}}/{{forloop.length}} {%endfor%}',
            **assigns
        )
        assert_template_result(' 1  2  3 ', '{%for item in array%} {{forloop.index}} {%endfor%}', **assigns)
        assert_template_result(' 0  1  2 ', '{%for item in array%} {{forloop.index0}} {%endfor%}', **assigns)
        assert_template_result(' 2  1  0 ', '{%for item in array%} {{forloop.rindex0}} {%endfor%}', **assigns)
        assert_template_result(' 3  2  1 ', '{%for item in array%} {{forloop.rindex}} {%endfor%}', **assigns)
        assert_template_result(' True  False  False ', '{%for item in array%} {{forloop.first}} {%endfor%}', **assigns)
        assert_template_result(' False  False  True ', '{%for item in array%} {{forloop.last}} {%endfor%}', **assigns)

    def test_for_and_if(self, env):
        assigns = {'array': [1, 2, 3]}
        assert_template_result(
            '+--',
            '{%for item in array%}{% if forloop.first %}+{% else %}-{% endif %}{%endfor%}',
            **assigns
        )

    def test_for_else(self, env):
        assert_template_result('+++', '{%for item in array%}+{%else%}-{%endfor%}', array=[1, 2, 3])
        assert_template_result('-', '{%for item in array%}+{%else%}-{%endfor%}', array=[])
        # Do we really need/want this?
        #assert_template_result('-', '{%for item in array%}+{%else%}-{%endfor%}', array=None)

    def test_limiting(self, env):
        assigns = {'array': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]}
        assert_template_result('12', '{%for i in array limit:2 %}{{ i }}{%endfor%}', **assigns)
        assert_template_result('1234', '{%for i in array limit:4 %}{{ i }}{%endfor%}', **assigns)
        assert_template_result('3456', '{%for i in array limit:4 offset:2 %}{{ i }}{%endfor%}', **assigns)
        assert_template_result('3456', '{%for i in array limit: 4 offset: 2 %}{{ i }}{%endfor%}', **assigns)

    def test_dynamic_variable_limiting(self, env):
        assigns = {'array': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]}
        assigns['limit'] = 2
        assigns['offset'] = 2

        assert_template_result('34', '{%for i in array limit: limit offset: offset %}{{ i }}{%endfor%}', **assigns)

    def test_nested_for(self, env):
        assigns = {'array': [[1, 2], [3, 4], [5, 6]]}
        assert_template_result('123456', '{%for item in array%}{%for i in item%}{{ i }}{%endfor%}{%endfor%}', **assigns)

    def test_offset_only(self, env):
        assigns = {'array': [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]}
        assert_template_result('890', '{%for i in array offset:7 %}{{ i }}{%endfor%}', **assigns)
#
#  def test_pause_resume
#    assigns = { 'array' => { 'items' => [1, 2, 3, 4, 5, 6, 7, 8, 9, 0] } }
#    markup = <<-MKUP
#      {%for i in array.items limit: 3 %}{{i}}{%endfor%}
#      next
#      {%for i in array.items offset:continue limit: 3 %}{{i}}{%endfor%}
#      next
#      {%for i in array.items offset:continue limit: 3 %}{{i}}{%endfor%}
#      MKUP
#    expected = <<-XPCTD
#      123
#      next
#      456
#      next
#      789
#      XPCTD
#    assert_template_result(expected, markup, assigns)
#  end
#
#  def test_pause_resume_limit
#    assigns = { 'array' => { 'items' => [1, 2, 3, 4, 5, 6, 7, 8, 9, 0] } }
#    markup = <<-MKUP
#      {%for i in array.items limit:3 %}{{i}}{%endfor%}
#      next
#      {%for i in array.items offset:continue limit:3 %}{{i}}{%endfor%}
#      next
#      {%for i in array.items offset:continue limit:1 %}{{i}}{%endfor%}
#      MKUP
#    expected = <<-XPCTD
#      123
#      next
#      456
#      next
#      7
#      XPCTD
#    assert_template_result(expected, markup, assigns)
#  end
#
#  def test_pause_resume_BIG_limit
#    assigns = { 'array' => { 'items' => [1, 2, 3, 4, 5, 6, 7, 8, 9, 0] } }
#    markup = <<-MKUP
#      {%for i in array.items limit:3 %}{{i}}{%endfor%}
#      next
#      {%for i in array.items offset:continue limit:3 %}{{i}}{%endfor%}
#      next
#      {%for i in array.items offset:continue limit:1000 %}{{i}}{%endfor%}
#      MKUP
#    expected = <<-XPCTD
#      123
#      next
#      456
#      next
#      7890
#      XPCTD
#    assert_template_result(expected, markup, assigns)
#  end
#
#  def test_pause_resume_BIG_offset
#    assigns = { 'array' => { 'items' => [1, 2, 3, 4, 5, 6, 7, 8, 9, 0] } }
#    markup = '{%for i in array.items limit:3 %}{{i}}{%endfor%}
#      next
#      {%for i in array.items offset:continue limit:3 %}{{i}}{%endfor%}
#      next
#      {%for i in array.items offset:continue limit:3 offset:1000 %}{{i}}{%endfor%}'
#    expected = '123
#      next
#      456
#      next
#      '
#    assert_template_result(expected, markup, assigns)
#  end
#
    def test_for_with_break(self, env):
        # items is a reserved attribute on dicts
        assigns = {'array': {'items_': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}}

        markup = '{% for i in array.items_ %}{% break %}{% endfor %}'
        expected = ""
        assert_template_result(expected, markup, **assigns)

        markup = '{% for i in array.items_ %}{{ i }}{% break %}{% endfor %}'
        expected = "1"
        assert_template_result(expected, markup, **assigns)

        markup = '{% for i in array.items_ %}{% break %}{{ i }}{% endfor %}'
        expected = ""
        assert_template_result(expected, markup, **assigns)

        markup = '{% for i in array.items_ %}{{ i }}{% if i > 3 %}{% break %}{% endif %}{% endfor %}'
        expected = "1234"
        assert_template_result(expected, markup, **assigns)

        # tests to ensure it only breaks out of the local for loop
        # and not all of them.
        assigns = {'array': [[1, 2], [3, 4], [5, 6]]}
        markup = (
            '{% for item in array %}'
            '{% for i in item %}'
            '{% if i == 1 %}'
            '{% break %}'
            '{% endif %}'
            '{{ i }}'
            '{% endfor %}'
            '{% endfor %}'
        )
        expected = '3456'
        assert_template_result(expected, markup, **assigns)

        # test break does nothing when unreached
        assigns = {'array': {'items_': [1, 2, 3, 4, 5]}}
        markup = '{% for i in array.items_ %}{% if i == 9999 %}{% break %}{% endif %}{{ i }}{% endfor %}'
        expected = '12345'
        assert_template_result(expected, markup, **assigns)

    def test_for_with_continue(self, env):
        assigns = {'array': {'items_': [1, 2, 3, 4, 5]}}

        markup = '{% for i in array.items_ %}{% continue %}{% endfor %}'
        expected = ""
        assert_template_result(expected, markup, **assigns)

        markup = '{% for i in array.items_ %}{{ i }}{% continue %}{% endfor %}'
        expected = "12345"
        assert_template_result(expected, markup, **assigns)

        markup = '{% for i in array.items_ %}{% continue %}{{ i }}{% endfor %}'
        expected = ""
        assert_template_result(expected, markup, **assigns)

        markup = '{% for i in array.items_ %}{% if i > 3 %}{% continue %}{% endif %}{{ i }}{% endfor %}'
        expected = "123"
        assert_template_result(expected, markup, **assigns)

        markup = '{% for i in array.items_ %}{% if i == 3 %}{% continue %}{% else %}{{ i }}{% endif %}{% endfor %}'
        expected = "1245"
        assert_template_result(expected, markup, **assigns)

        # tests to ensure it only continues the local for loop and not all of them.
        assigns = {'array': [[1, 2], [3, 4], [5, 6]]}
        markup = ('{% for item in array %}'
                  '{% for i in item %}'
                  '{% if i == 1 %}'
                  '{% continue %}'
                  '{% endif %}'
                  '{{ i }}'
                  '{% endfor %}'
                  '{% endfor %}')
        expected = '23456'
        assert_template_result(expected, markup, **assigns)

        # test continue does nothing when unreached
        assigns = {'array': {'items_': [1, 2, 3, 4, 5]}}
        markup = '{% for i in array.items_ %}{% if i == 9999 %}{% continue %}{% endif %}{{ i }}{% endfor %}'
        expected = '12345'
        assert_template_result(expected, markup, **assigns)

    def test_for_tag_string(self, env):
        assert_template_result('test string',
        '{%for val in string%}{{val}}{%endfor%}',
        string="test string")

        #assert_template_result('test string',
        #  '{%for val in string limit:1%}{{val}}{%endfor%}',
        #  string="test string")

        # not sure we can support this string iteration model
        #assert_template_result('val-string-1-1-0-1-0-true-true-test string', (
        #    '{%for val in string%}'
        #    '{{forloop.name}}-'
        #    '{{forloop.index}}-'
        #    '{{forloop.length}}-'
        #    '{{forloop.index0}}-'
        #    '{{forloop.rindex}}-'
        #    '{{forloop.rindex0}}-'
        #    '{{forloop.first}}-'
        #    '{{forloop.last}}-'
        #    '{{val}}{%endfor%}'),
        #    string="test string")

    #def test_for_parentloop_references_parent_loop(self, env):
    #    assert_template_result('1.1 1.2 1.3 2.1 2.2 2.3 ', (
    #        '{% for inner in outer %}{% for k in inner %}'
    #        '{{ forloop.parentloop.index }}.{{ forloop.index }} '
    #        '{% endfor %}{% endfor %}'),
    #        outer=[[1, 1, 1], [1, 1, 1]]
    #    )

    #def test_for_parentloop_nil_when_not_present(self, env):
    #    assert_template_result('.1 .2 ', (
    #        '{% for inner in outer %}'
    #        '{{ forloop.parentloop.index }}.{{ forloop.index }} '
    #        '{% endfor %}'),
    #        outer=[[1, 1, 1], [1, 1, 1]]
    #    )

    def test_inner_for_over_empty_input(self, env):
        assert_template_result('oo', '{% for a in (1..2) %}o{% for b in empty %}{% endfor %}{% endfor %}')

    def test_blank_string_not_iterable(self, env):
        assert_template_result('', "{% for char in characters %}I WILL NOT BE OUTPUT{% endfor %}", characters='')

    def test_bad_variable_naming_in_for_loop(self, env):
        with pytest.raises(TemplateSyntaxError):
            assert_template_result('', '{% for a/b in x %}{% endfor %}')

    def test_spacing_with_variable_naming_in_for_loop(self, env):
        expected = '12345'
        template = '{% for       item   in   items %}{{item}}{% endfor %}'
        assigns = {'items': [1, 2, 3, 4, 5]}
        assert_template_result(expected, template, **assigns)

#  class LoaderDrop:
#      each_called = None
#      load_slice_called = None
#
#      def __init__(self, data):
#    self.data = data
#
#    def each(self):
#        self.each_called = True
#
#    def load_slice(self, start, stop)
#      @load_slice_called = true
#      data[start:stop]
#    end
#  end
#
#  def test_iterate_with_each_when_no_limit_applied
#    loader = LoaderDrop.new([1, 2, 3, 4, 5])
#    assigns = { 'items' => loader }
#    expected = '12345'
#    template = '{% for item in items %}{{item}}{% endfor %}'
#    assert_template_result(expected, template, assigns)
#    assert loader.each_called
#    assert !loader.load_slice_called
#  end
#
#  def test_iterate_with_load_slice_when_limit_applied
#    loader = LoaderDrop.new([1, 2, 3, 4, 5])
#    assigns = { 'items' => loader }
#    expected = '1'
#    template = '{% for item in items limit:1 %}{{item}}{% endfor %}'
#    assert_template_result(expected, template, assigns)
#    assert !loader.each_called
#    assert loader.load_slice_called
#  end
#
#  def test_iterate_with_load_slice_when_limit_and_offset_applied
#    loader = LoaderDrop.new([1, 2, 3, 4, 5])
#    assigns = { 'items' => loader }
#    expected = '34'
#    template = '{% for item in items offset:2 limit:2 %}{{item}}{% endfor %}'
#    assert_template_result(expected, template, assigns)
#    assert !loader.each_called
#    assert loader.load_slice_called
#  end
#
#  def test_iterate_with_load_slice_returns_same_results_as_without
#    loader = LoaderDrop.new([1, 2, 3, 4, 5])
#    loader_assigns = { 'items' => loader }
#    array_assigns = { 'items' => [1, 2, 3, 4, 5] }
#    expected = '34'
#    template = '{% for item in items offset:2 limit:2 %}{{item}}{% endfor %}'
#    assert_template_result(expected, template, loader_assigns)
#    assert_template_result(expected, template, array_assigns)
#  end
#
#  def test_for_cleans_up_registers
#    context = Context.new(ErrorDrop.new)
#
#    assert_raises(StandardError) do
#      Liquid::Template.parse('{% for i in (1..2) %}{{ standard_error }}{% endfor %}').render!(context)
#    end
#
#    assert context.registers[:for_stack].empty?
#  end
#end
