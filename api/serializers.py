from django.contrib.auth import authenticate, get_user_model

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.settings import api_settings

from titles.models import User, Title, Genre, Category, Review, Comment


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields["confirmation_code"] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            "confirmation_code": attrs["confirmation_code"],
        }
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(email=attrs[self.username_field],
                                 password=attrs["confirmation_code"])

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        data = {}
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'bio', 'email', 'role']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["name", "slug"]


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
        required=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def to_representation(self, instance):
        instance.refresh_rating()
        data = super().to_representation(instance)
        data['category'] = CategorySerializer(instance.category).data
        data['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        return data


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "text", "author", "score", "pub_date"]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "text", "author", "pub_date"]