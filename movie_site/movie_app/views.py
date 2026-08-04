from  rest_framework.response import Response
from .permissions import CheckRole
from .filters import MovieFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics, views, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserProfile, Country, Director, Actor, Genre, Movie, MovieLanguages, MovieMoments, Rating, SaveToFavorite, FavoriteMovies, History
from .serializers import (UserProfileSerializers, CountrySerializers, CountryDetailSerializers, DirectorSerializers, ActorSerializers, GenreSerializers, GenreDetailSerializers,
                          MovieSerializers, MovieDetailSerializers, MovieLanguagesSerializers, MovieMomentsSerializers,
                          RatingSerializers, SaveToFavoriteSerializers, FavoriteMoviesSerializers, HistorySerializers,
                          LoginSerializer, UserSerializer, RatingCreateSerializers)



class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

# --------------------------------------------------------------------------------------
class UserProfileAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers
    permission_classes = [permissions.IsAdminUser]

class CountryAPIView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializers

class CountryDetailAPIView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryDetailSerializers

class DirectorAPIView(generics.ListAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializers

class DirectorDetailAPIView(generics.RetrieveAPIView):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializers

class ActorAPIView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializers

class ActorDetailAPIView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializers

class GenreAPIView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers

class GenreDetailAPIView(generics.RetrieveAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreDetailSerializers

class MovieAPIView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializers

    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = MovieFilter
    ordering_fields = ['year']
    search_fields = ['movie_name']

class MovieDetailAPIView(generics.RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializers
    permission_classes = [permissions.IsAuthenticated, CheckRole]

class MovieLanguagesAPIView(generics.ListAPIView):
    queryset = MovieLanguages.objects.all()
    serializer_class = MovieLanguagesSerializers

class MovieMomentsAPIView(generics.ListAPIView):
    queryset = MovieMoments.objects.all()
    serializer_class = MovieMomentsSerializers

class RatingAPIView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RatingCreateSerializers
        return RatingSerializers

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class SaveToFavoriteAPIView(generics.ListAPIView):
    queryset = SaveToFavorite.objects.all()
    serializer_class = SaveToFavoriteSerializers

class FavoriteMoviesAPIView(generics.ListCreateAPIView):
    queryset = FavoriteMovies.objects.all()
    serializer_class = FavoriteMoviesSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteMovies.objects.filter(save_to_favorite__user=self.request.user)

    def perform_create(self, serializer):
        save_to_favorite, _ = SaveToFavorite.objects.get_or_create(user=self.request.user)
        serializer.save(save_to_favorite=save_to_favorite)

class HistoryAPIView(generics.ListCreateAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
