from nautobot.utilities.filters import BaseFilterSet, SearchFilter

from example_plugin.models import AnotherExampleModel, ExampleModel


class ExampleModelFilterSet(BaseFilterSet):
    """API filter for filtering example model objects."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "number": "icontains",
        },
    )

    class Meta(BaseFilterSet.Meta):
        model = ExampleModel
        fields = [
            "id",
            "name",
            "number",
        ]


class AnotherExampleModelFilterSet(BaseFilterSet):
    """API filter for filtering another example model objects."""

    q = SearchFilter(
        filter_predicates={
            "name": "icontains",
            "number": "icontains",
        },
    )

    class Meta(BaseFilterSet.Meta):
        model = AnotherExampleModel
        fields = [
            "id",
            "name",
            "number",
        ]
