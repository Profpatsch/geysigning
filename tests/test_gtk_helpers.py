from gtk_helpers import UI

import pytest

@pytest.fixture
def widget():
    def widget_fn(name):
        return name

@pytest.fixture
def mock_builder(widget):
    class MockBuilder:
        def get_object(self, name):
            return widget(name)
    return MockBuilder()

@pytest.fixture
def mock_widget():
    def mock_widget_fn(name, children=None):
        return UI(name, "mock-object", children)
    return mock_widget_fn

# class TestUIFromStruct:
#     def test_string(self, mock_builder, mock_widget):
#         s = 'some-widget'
#         ui = mock_widget(s)
#         assert UI.from_structure(mock_builder, s) == ui

#     def test_list(self, mock_builder, mock_widget):
#         l = ['widget1', 'widget2']
#         ui = [mock_widget(w) for w in l]
#         assert UI.from_structure(mock_builder, l) == ui

#     def test_dict_(self, mock_builder, mock_widget):
#         dfilled = {'container': 'child'}
#         dempty = {'element': None}
#         uifilled = mock_widget('container', mock_widget('child'))
#         uiempty = mock_widget('element')
#         assert UI.from_structure(mock_builder, dfilled) == uifilled
#         assert UI.from_structure(mock_builder, dempty) == uiempty

#     def test_none(self, mock_builder, mock_widget):
#         assert UI.from_structure(mock_builder, None) == None

#     def test_wrong_structure(self, mock_builder):
#         with pytest.raises(ValueError):
#             UI.from_structure(mock_builder, 123)

class TestUIAccessing:
    structure = {
        'some-container': 'inner-widget',
        'some-widget': None,
        'list-container': [
            'widget',
            {'inner-container': 'innermost-widget'}
        ]
    }

    def test_container(self, mock_builder, widget):
        ui = UI.from_structure(mock_builder, self.structure)
        assert len(ui) == len(self.structure)
        assert type(ui) is UI
        assert ui['some-container'] == widget('some-container')
        assert ui['some-container']['inner-widget'] == widget('inner-widget')
        assert ui['list-container'][1]['inner-container'] \
            == widget('inner-container')
