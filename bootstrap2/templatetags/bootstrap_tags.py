from django.template import Context
from django.template.loader import get_template
from django import template
from django.conf import settings
from bootstrap2.forms import TEMPLATE_PREFIX, _bound_field_context, Field, _merge_field
from django.forms.forms import BoundField
from django.template.context import Context
from django.template import Library, Node, TemplateSyntaxError
from django.template.defaulttags import kwarg_re


register = Library()

class BootstrapFieldNode(Node):
    def __init__(self,args,kwargs):
        self.args = args
        self.kwargs = kwargs
        
    def render(self,ctx):
        attrs = {}
        
        if hasattr(settings,'BOOTSTRAP_HELP_BLOCK') and settings.BOOTSTRAP_HELP_BLOCK:
            help_inline = False
        else:
            help_inline = True

        if 'span' in self.kwargs:
            attrs['class'] = Field.SPAN % self.kwargs['span'].resolve(ctx)
            
        if 'label' in self.kwargs:
            label = self.kwargs['label'].resolve(ctx)
        else:
            label = None
        
        if len(self.args) > 1:
            template = get_template(TEMPLATE_PREFIX % "inline_field.html")
            contexts = tuple()
            for field in [f.resolve(ctx) for f in self.args]:
                if isinstance(field,BoundField):
                    contexts = contexts + (_bound_field_context(field,widget_attrs=attrs.copy()),)
                else:
                    contexts = contexts + (field,)
                                    
            help = _merge_field(contexts,'help_text')
            errors = _merge_field(contexts,'errors')
            
            return template.render(Context({'fields' : contexts, 'label' : label, 'help' : help, 'errors' : errors, 'help_inline': help_inline}))
    
        else:
            if 'prepend' in self.kwargs or 'append' in self.kwargs:
                if 'prepend' in self.kwargs:
                    template = get_template(TEMPLATE_PREFIX % "addon_field_prepend.html")
                else:
                    template = get_template(TEMPLATE_PREFIX % "addon_field_append.html")
                
                addon = self.kwargs.get('prepend',self.kwargs.get('append'))
                addon = addon.resolve(ctx)

                context = {'help_inline': help_inline}
                
                context['field'] = _bound_field_context(self.args[0].resolve(ctx),widget_attrs=attrs.copy())
                if isinstance(addon,BoundField):
                    context['addon'] = _bound_field_context(addon)
                else:
                    context['addon'] = addon
                
                context['help'] = _merge_field([context['field'],context['addon']],'help_text')
                context['errors'] = _merge_field([context['field'],context['addon']],'errors')
    
                return template.render(Context(context))
            else:
                template = get_template(TEMPLATE_PREFIX % "field.html")
                context = _bound_field_context(self.args[0].resolve(ctx),widget_attrs=attrs.copy())
                context['help_inline'] = help_inline
                return template.render(Context(context))

@register.tag
def bootstrap_field(parser,token):
    
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument - a field" % bits[0])
    args = []
    kwargs = {}
    bits = bits[1:]
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))
    
    if not len(args):
        return ''

    return BootstrapFieldNode(args,kwargs)

@register.filter
def as_bootstrap(form):
    template = get_template(TEMPLATE_PREFIX % "form.html")
    c = Context({"form": form})
    return template.render(c)

SCRIPT_TAG = '<script src="%sjs/bootstrap.min.js"></script>'

class BootstrapJSNode(template.Node):

    def __init__(self, args):
        self.args = set(args)

    def render_all_scripts(self):
        results = [
            SCRIPT_TAG % settings.STATIC_URL,
        ]
        return '\n'.join(results)

    def render(self, context):
        return self.render_all_scripts()

@register.simple_tag
def bootstrap_css():
    return '<link rel="stylesheet" href="%scss/bootstrap.min.css">' % settings.STATIC_URL

@register.simple_tag
def bootstrap_responsive_css():
    return '<link rel="stylesheet" href="%scss/bootstrap_responsive.min.css">' % settings.STATIC_URL

@register.tag(name='bootstrap_js')
def do_bootstrap_js(parser, token):
    print '\n'.join(token.split_contents())
    return BootstrapJSNode(token.split_contents()[1:])

class IconNode(template.Node):
    """
node class for icon tag
"""
    
    def __init__(self, name, attrs):
        self.name = template.Variable(name)
        self.attrs = {}
        for attr in attrs:
            key, value = attr.split("=")
            self.attrs[key] = template.Variable(value)
    
    def render(self, context):
        """
render the i tag with specified attributes
"""
        name = self.name.resolve(context)
        return """<i class="%s"></i>""" % name


@register.tag
def icon(parser, token):
    """
Template tag to render icons
Usage::
{% icon "icon_name" %}
"""
    bits = token.split_contents()
    return IconNode(bits[1], bits[2:])
