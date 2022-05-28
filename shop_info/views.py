from django.db.models import Q, QuerySet
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from .serializers import ShopSerializer
from .models import Shop


class ShopView(ListCreateAPIView):
    serializer_class = ShopSerializer

    def get_queryset(self) -> QuerySet:
        allowed_filters = ['city', 'street']
        current_time = Shop.get_current_time()
        qdict = self.request.query_params

        params = {key: int(value[0]) for key, value in qdict.lists()
                  if key in allowed_filters}

        qs = Shop.objects.filter(**params)
        is_open = int(qdict.get('open', 2))
        if is_open == 1:
            return qs.filter(Q(open_time__lte=current_time) & Q(close_time__gt=current_time)).all()
        elif is_open == 0:
            return qs.exclude(Q(open_time__lte=current_time) & Q(close_time__gt=current_time)).all()
        return qs.all()

    def post(self, request, *args, **kwargs) -> Response:
        data = self.create(request, *args, **kwargs)
        return Response({'id': data.data['id']}, status=200, headers=data.headers)
