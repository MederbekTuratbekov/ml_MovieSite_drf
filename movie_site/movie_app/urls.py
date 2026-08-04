from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import (UserProfileAPIView, CountryAPIView, CountryDetailAPIView,
                    DirectorAPIView, DirectorDetailAPIView,
                    ActorAPIView, ActorDetailAPIView,
                    GenreAPIView, GenreDetailAPIView,
                    MovieAPIView, MovieDetailAPIView,
                    MovieLanguagesAPIView, MovieMomentsAPIView,
                    FavoriteMoviesAPIView, SaveToFavoriteAPIView, HistoryAPIView,
                    RegisterView, CustomLoginView, LogoutView, RatingAPIView)


urlpatterns = [
    path('', MovieAPIView.as_view(), name='movies'),
    path('<int:pk>/', MovieDetailAPIView.as_view(), name='movie_details'),
    path('genre/', GenreAPIView.as_view(), name='genres'),
    path('genre/<int:pk>/', GenreDetailAPIView.as_view(), name='genre_details'),
    path('country/', CountryAPIView.as_view(), name='countries'),
    path('country/<int:pk>/', CountryDetailAPIView.as_view(), name='country_details'),
    path('director/', DirectorAPIView.as_view(), name='directors'),
    path('director/<int:pk>/', DirectorDetailAPIView.as_view(), name='director_details'),
    path('actor/', ActorAPIView.as_view(), name='actors'),
    path('actor/<int:pk>/', ActorDetailAPIView.as_view(), name='actor_details'),
    path('movie_languages/', MovieLanguagesAPIView.as_view(), name='movie_languages'),
    path('movie_moments/', MovieMomentsAPIView.as_view(), name='movie_moments'),
    path('history/', HistoryAPIView.as_view(), name='histories'),
    path('favorite_movie/', FavoriteMoviesAPIView.as_view(), name='favorite_movies'),
    path('save_to_favorite/', SaveToFavoriteAPIView.as_view(), name='save_to_favorite'),
    path('user/', UserProfileAPIView.as_view(), name='user'),
    path('rating/', RatingAPIView.as_view(), name='ratings'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
