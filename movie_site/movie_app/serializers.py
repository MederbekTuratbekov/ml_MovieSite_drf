from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import UserProfile, Country, Director, Actor, Genre, Movie, MovieLanguages, MovieMoments, Rating, SaveToFavorite, FavoriteMovies, History
import os
import joblib
from django.conf import settings


model_path = os.path.join(settings.BASE_DIR, 'model_nb.pkl')
model = joblib.load(model_path)

vector_path = os.path.join(settings.BASE_DIR, 'vector.pkl')
vector = joblib.load(vector_path)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'age', 'phone_number', 'status')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileMovieDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']


class CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class CountryDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class DirectorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name', 'bio', 'age', 'director_image']


class DirectorMovieDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']


class ActorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name', 'bio', 'age', 'actor_image']


class ActorMovieDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name']


class GenreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class GenreDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class MovieSerializers(serializers.ModelSerializer):
    year = serializers.DateField(format='%Y')
    genre = GenreSerializers(many=True)
    country = CountrySerializers()

    class Meta:
        model = Movie
        fields = ['id', 'movie_name', 'movie_image', 'year', 'genre', 'country', 'status_movie']


class MovieMomentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = MovieMoments
        fields = ['movie_moments']


class MovieLanguagesSerializers(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['movie_dubbing', 'video']


class RatingSerializers(serializers.ModelSerializer):
    user = UserProfileMovieDetailSerializers()
    parent = UserProfileMovieDetailSerializers(source='parent.user', read_only=True, allow_null=True)
    created_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    check_comments = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ['user', 'parent', 'text', 'stars', 'created_date', 'check_comments']

    def get_check_comments(self, obj):
        return model.predict(vector.transform([obj.text]))


class RatingCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['movie', 'stars', 'text', 'parent']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
        

class MovieDetailSerializers(serializers.ModelSerializer):
    director = DirectorMovieDetailSerializers(many=True)
    actor = ActorMovieDetailSerializers(many=True)
    year = serializers.DateField(format='%d-%m-%Y')
    genre = GenreSerializers(many=True)
    country = CountrySerializers()
    movie_moments_connect_movie = MovieMomentsSerializers(many=True)
    movie_videos_connect_movie = MovieLanguagesSerializers(many=True)
    avg_rating = serializers.SerializerMethodField()
    count_user = serializers.SerializerMethodField()
    rating_connect_movie = RatingSerializers(many=True)

    class Meta:
        model = Movie
        fields = ['movie_name', 'movie_image', 'director', 'actor', 'year', 'genre', 'country',
                  'quality', 'movie_time', 'movie_trailer', 'movie_moments_connect_movie',
                  'description', 'movie_videos_connect_movie', 'status_movie', 'avg_rating',
                  'count_user', 'rating_connect_movie']

    def get_avg_rating(self, obj):
        return obj.avg_rating()

    def get_count_user(self, obj):
        return obj.count_user()


class SaveToFavoriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = SaveToFavorite
        fields = '__all__'


class FavoriteMoviesSerializers(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovies
        fields = ['movie', 'save_to_favorite']


class HistorySerializers(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['user', 'movie', 'viewed_at']
