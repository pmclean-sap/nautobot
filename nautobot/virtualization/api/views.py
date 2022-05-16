from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.routers import APIRootView

from nautobot.dcim.models import Device
from nautobot.extras.api.views import (
    ConfigContextQuerySetMixin,
    CustomFieldModelViewSet,
    ModelViewSet,
    StatusViewSetMixin,
)
from nautobot.utilities.utils import count_related, SerializerVersions, versioned_serializer_selector
from nautobot.virtualization import filters
from nautobot.virtualization.models import (
    Cluster,
    ClusterGroup,
    ClusterType,
    VirtualMachine,
    VMInterface,
)
from . import serializers


class VirtualizationRootView(APIRootView):
    """
    Virtualization API root view
    """

    def get_view_name(self):
        return "Virtualization"


#
# Clusters
#


class ClusterTypeViewSet(CustomFieldModelViewSet):
    queryset = ClusterType.objects.annotate(cluster_count=count_related(Cluster, "type"))
    serializer_class = serializers.ClusterTypeSerializer
    filterset_class = filters.ClusterTypeFilterSet


class ClusterGroupViewSet(CustomFieldModelViewSet):
    queryset = ClusterGroup.objects.annotate(cluster_count=count_related(Cluster, "group"))
    serializer_class = serializers.ClusterGroupSerializer
    filterset_class = filters.ClusterGroupFilterSet


class ClusterViewSet(CustomFieldModelViewSet):
    queryset = Cluster.objects.prefetch_related("type", "group", "tenant", "site", "tags").annotate(
        device_count=count_related(Device, "cluster"),
        virtualmachine_count=count_related(VirtualMachine, "cluster"),
    )
    serializer_class = serializers.ClusterSerializer
    filterset_class = filters.ClusterFilterSet


#
# Virtual machines
#


class VirtualMachineViewSet(ConfigContextQuerySetMixin, StatusViewSetMixin, CustomFieldModelViewSet):
    queryset = VirtualMachine.objects.prefetch_related(
        "cluster__site",
        "platform",
        "primary_ip4",
        "primary_ip6",
        "status",
        "role",
        "tenant",
        "tags",
    )
    filterset_class = filters.VirtualMachineFilterSet

    def get_serializer_class(self):
        """
        Select the specific serializer based on the request context.

        If the `brief` query param equates to True, return the NestedVirtualMachineSerializer

        If the `exclude` query param includes `config_context` as a value, return the VirtualMachineSerializer

        Else, return the VirtualMachineWithConfigContextSerializer
        """

        request = self.get_serializer_context()["request"]
        if request is not None and request.query_params.get("brief", False):
            return serializers.NestedVirtualMachineSerializer

        elif request is not None and "config_context" in request.query_params.get("exclude", []):
            return serializers.VirtualMachineSerializer

        return serializers.VirtualMachineWithConfigContextSerializer


@extend_schema_view(
    bulk_update=extend_schema(
        responses={"200": serializers.VMInterfaceSerializerVersion12(many=True)}, versions=["1.2", "1.3"]
    ),
    bulk_partial_update=extend_schema(
        responses={"200": serializers.VMInterfaceSerializerVersion12(many=True)}, versions=["1.2", "1.3"]
    ),
    create=extend_schema(responses={"201": serializers.VMInterfaceSerializerVersion12}, versions=["1.2", "1.3"]),
    list=extend_schema(
        responses={"200": serializers.VMInterfaceSerializerVersion12(many=True)}, versions=["1.2", "1.3"]
    ),
    partial_update=extend_schema(
        responses={"200": serializers.VMInterfaceSerializerVersion12}, versions=["1.2", "1.3"]
    ),
    retrieve=extend_schema(responses={"200": serializers.VMInterfaceSerializerVersion12}, versions=["1.2", "1.3"]),
    update=extend_schema(responses={"200": serializers.VMInterfaceSerializerVersion12}, versions=["1.2", "1.3"]),
)
class VMInterfaceViewSet(StatusViewSetMixin, ModelViewSet):
    queryset = VMInterface.objects.prefetch_related("virtual_machine", "status", "tags", "tagged_vlans")
    serializer_class = serializers.VMInterfaceSerializer
    filterset_class = filters.VMInterfaceFilterSet
    brief_prefetch_fields = ["virtual_machine"]

    def get_serializer_class(self):
        serializer_choices = (
            SerializerVersions(versions=["1.2", "1.3"], serializer=serializers.VMInterfaceSerializerVersion12),
        )
        return versioned_serializer_selector(
            obj=self,
            serializer_choices=serializer_choices,
            current_serializer=super().get_serializer_class(),
        )
