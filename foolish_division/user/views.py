from rest_framework import viewsets


class VendorViewset(viewsets.ModelViewSet):
    serializer_class = VendorSerializer

    def get_queryset(self):
        user = self.request.user
        if not user:
            return Vendor.objects.none()

        return Vendor.objects.all()