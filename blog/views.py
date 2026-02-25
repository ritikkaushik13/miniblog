from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    OTPVerifySerializer,
    BlogPostSerializer,
    CommentSerializer,
    LikeSerializer
)
from .models import BlogPost, OTP
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema


class RegisterView(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Delete old OTPs
            OTP.objects.filter(user=user).delete()

            code = OTP.generate_otp()
            expires_at = timezone.now() + timedelta(minutes=5)

            OTP.objects.create(
                user=user,
                code=code,
                expires_at=expires_at
            )

            print("OTP:", code)
            send_mail(
                subject="Your OTP Code",
                message=f"Your OTP is {code}. It expires in 5 minutes.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return Response(
                {"message": "OTP sent successfully."},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    @swagger_auto_schema(request_body=OTPVerifySerializer)
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Delete OTP after successful verification
            OTP.objects.filter(user=user).delete()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=BlogPostSerializer)
    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)


class ListPostsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = BlogPost.objects.all().order_by('-created_at')
        serializer = BlogPostSerializer(posts, many=True)
        return Response(serializer.data)


class GetMyPostView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            post = BlogPost.objects.get(id=pk, author=request.user)
        except BlogPost.DoesNotExist:
            return Response(
                {"error": "Post not found or not yours."},
                status=404
            )

        serializer = BlogPostSerializer(post)
        return Response(serializer.data)


class EditPostView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            post = BlogPost.objects.get(id=pk, author=request.user)
        except BlogPost.DoesNotExist:
            return Response(
                {"error": "Not allowed."},
                status=404
            )

        serializer = BlogPostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class DeletePostView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            post = BlogPost.objects.get(id=pk, author=request.user)
        except BlogPost.DoesNotExist:
            return Response(
                {"error": "Not allowed."},
                status=404
            )

        post.delete()
        return Response({"message": "Deleted successfully."})


from django.shortcuts import get_object_or_404

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LikeSerializer)
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, id=pk)

        like, created = post.likes.get_or_create(user=request.user)

        if not created:
            return Response(
                {"message": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"message": "Post liked successfully."},
            status=status.HTTP_201_CREATED
        )


class CommentPostView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, pk):
        post = get_object_or_404(BlogPost, id=pk)

        data = request.data.copy()
        data['post'] = post.id

        serializer = CommentSerializer(data=data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



