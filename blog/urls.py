from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    VerifyOTPView,
    CreatePostView,
    ListPostsView,
    GetMyPostView,
    EditPostView,
    DeletePostView,
    LikePostView,
    CommentPostView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify-otp/', VerifyOTPView.as_view()),

    path('posts/create/', CreatePostView.as_view()),
    path('posts/', ListPostsView.as_view()),
    path('posts/<int:pk>/', GetMyPostView.as_view()),
    path('posts/<int:pk>/edit/', EditPostView.as_view()),
    path('posts/<int:pk>/delete/', DeletePostView.as_view()),

    path('posts/<int:pk>/like/', LikePostView.as_view()),
    path('posts/<int:pk>/comment/', CommentPostView.as_view()),
]
