# calling
# ui["app-window"]
# ui["app-window"]["some-widget"]

# examples
# {widget':None}
# ['w1', 'w2']
# 'single-widget'
# {'compound-widget': ['child1', 'child2']
#  'second': None}



class UI:
    def __init__(self, name, element, children=None):
        self.name = name
        self.element = element
        self.children = children

    @staticmethod
    def from_structure(builder, ui_structure):
        if ui_structure is None:
            return None
        def g(obj_str):
            return builder.get_object(obj_str)
        if isinstance(ui_structure, str):
            return UI(ui_structure, g(ui_structure))
        elif isinstance(ui_structure, dict):
            res = []
            for element, children in ui_structure.iteritems():
                if not children:
                    res.append(UI(element, g(element)))
                else:
                    res.append(UI(element, g(element),
                              UI.from_structure(builder, children)))
            if len(res) == 1:
                return res[0]
            else:
                return res
        elif isinstance(ui_structure, list):
            return [UI.from_structure(builder, c) for c in ui_structure]
        else:
            raise ValueError("No such UI element.")

    def __getitem__(self, key):
        return self.children[key]

    def __eq__(self, other):
        return ((self.element == other.element) and
                (self.children == other.children))

    def __repr__(self):
        return "UI({}, {}, {})".format(
            self.name, self.element, self.children)
