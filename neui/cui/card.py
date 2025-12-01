from ..ui.box import Box

class Card(Box):
    def __init__(self, **kwargs):
        style = kwargs.get('style', {})
        
        # Card defaults
        if 'bg' not in style: style['bg'] = "#2D2D2D"
        if 'radius' not in style: style['radius'] = 12
        if 'padding' not in style: style['padding'] = 20
        if 'shadow' not in style: style['shadow'] = 10
        if 'layout' not in style: style['layout'] = 'col'
        if 'gap' not in style: style['gap'] = 10
        
        kwargs['style'] = style
        super().__init__(**kwargs)
