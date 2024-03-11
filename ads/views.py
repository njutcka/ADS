from rest_framework import pagination, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from ads.filters import AdFilter
from ads.models import Ad, Comment
from ads.permissions import IsAdminOrAuthor
from ads.serializers import CommentSerializer, AdSerializer, AdDetailSerializer


class AdPagination(pagination.PageNumberPagination):
    """Пагинация объявлений по 4 на страницу"""
    page_size = 4
    page_query_param = "page"


class AdViewSet(viewsets.ModelViewSet):
    """Контроллер модели Ad"""
    queryset = Ad.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter
    pagination_class = AdPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AdDetailSerializer
        return AdSerializer

    def perform_create(self, serializer):
        """Автоматическое сохранение автора при создании объекта"""
        new_ad = serializer.save()
        new_ad.author = self.request.user
        new_ad.save()

    def get_permissions(self):
        """Создавать и просматривать может любой авторизованный пользователь
        автор может редактировать и удалять только свои
        админ может редактировать и удалять любые объявления"""
        permission_classes = []
        if self.action == 'list':
            permission_classes = []
        if self.action in ['create', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrAuthor]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    """Контроллер модели Comment"""
    queryset = Comment.objects.all()
    filter_backends = [DjangoFilterBackend]
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Получает отзывы для определенного объявления"""
        ad_id = self.kwargs.get("ad_pk")
        ad = get_object_or_404(Ad, id=ad_id)
        return ad.reviews.all().order_by("created_at")

    def perform_create(self, serializer):
        """Автоматическое сохранение автора отзыва в объявлении"""
        ad_id = self.kwargs['ad_pk']
        ad = Ad.objects.get(pk=ad_id)
        new_comment = serializer.save()
        new_comment.author = self.request.user
        new_comment.ad = ad
        new_comment.save()

    def get_permissions(self):
        """Создавать и просматривать может любой авторизованный пользователь
        автор может редактировать и удалять только свои
        админ может редактировать и удалять любые отзывы"""
        permission_classes = []
        if self.action in ['create', 'list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrAuthor]
        return [permission() for permission in permission_classes]
