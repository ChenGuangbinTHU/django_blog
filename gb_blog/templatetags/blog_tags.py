from django import template
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

register = template.Library()

def block_code(text, lang, inlinestyles=False, linenos=False):
    if not lang:
        text = text.strip()
        return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(
            noclasses=inlinestyles, linenos=linenos
        )
        code = highlight(text, lexer, formatter)
        if linenos:
            return '<div class="highlight">%s</div>\n' % code
        return code
    except:
        return '<pre class="%s"><code>%s</code></pre>\n' % (
            lang, mistune.escape(text)
        )


class HighlightMixin(mistune.Renderer):
    def block_code(self, text, lang='en'):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)

class TocRenderer(HighlightMixin, mistune.Renderer):
    pass

# @register.filter(is_safe=True)
# def markdown_detail(value):
#     renderer = HighlightMixin()
#     mdp = mistune.Markdown(renderer=renderer)
#     return mdp(value)

@register.filter(is_safe=True)
# @stringfilter
def custom_markdown(value):
    return mark_safe(markdown2.markdown(force_text(value),
          extras=["fenced-code-blocks", "cuddled-lists", "metadata", "tables", "spoiler"]))
