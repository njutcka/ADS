from rest_framework import serializers

from ads.models import Comment, Ad


class CommentSerializer(serializers.ModelSerializer):
    """сериализатор для модели Comment"""
    author_first_name = serializers.CharField(source="author.first_name", read_only=True)
    author_last_name = serializers.CharField(source="author.last_name", read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    author_image = serializers.CharField(source="author.image", read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    # сериализатор для модели Ad
    image = serializers.ImageField(allow_null=True, default=None)

    class Meta:
        model = Ad
        fields = '__all__'


class AdDetailSerializer(serializers.ModelSerializer):
    # сериализатор для детального просмотра модели Ad
    image = serializers.ImageField(allow_null=True, default=None)
    title = serializers.CharField(max_length=250),
    price = serializers.IntegerField(),
    description = serializers.CharField(),
    author_first_name = serializers.CharField(source="author.first_name", read_only=True)
    author_last_name = serializers.CharField(source="author.last_name", read_only=True)
    author_email = serializers.CharField(source="author.email", read_only=True)

    class Meta:
        model = Ad
        fields = '__all__'
