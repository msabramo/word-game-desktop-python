class Bunch:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def import_cPickle_or_pickle():
    try:
        import cPickle as pickle
    except ImportError:
        import pickle

    return pickle


def import_cStringIO_or_StringIO():
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

    return StringIO


def replace_widget(old, new):
    parent = old.parent
    idx = parent.get_children().index(old)
    parent.remove(old)
    parent.add(new)

    # If the parent has a notion of ordering (e.g.: gtk.Box),
    # preserve the order
    if hasattr(parent, 'reorder_child'):
        parent.reorder_child(new, idx)

    new.show_all()

        
def freeze_size(widget):
    # Request that widget keep its size the same
    widget.set_size_request(*widget.size_request())


def container(cls, *widgets, **kwargs):
    container = cls()
    for key, val in kwargs.items():
        method = getattr(container, 'set_%s' % key)
        method(val)

    for widget in widgets: container.add(widget)
        
    return container


_letter_point_values = (
    (1, 'EAIONRTLSU'),
    (2, 'DG'),
    (3, 'BCMP'),
    (4, 'FHVWY'),
    (5, 'K'),
    (8, 'JX'),
    (10, 'QZ'))

def num_points_for_letter(letter):
    for point_value, letters in _letter_point_values:
        if letter in letters: return point_value
