from django.http import Http404
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Gallery, Mentor, Notice, projects
from .serializers import GallerySerializer, MentorSerializer, NoticeSerializer, ProjectSerializer, MessagesSerializer, FeadbackSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.


class UserCreateAPIView(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LatestNoticelistView(APIView):
    def get(self, request, format=None):
        notices = list(Notice.objects.all()[0:7])
        if not notices:
            return Response({'message': 'No data found'})
        serializer = NoticeSerializer(notices, many=True)
        return Response(serializer.data)


class NoticedetailView(APIView):
    def get_object(self, notice_slug):
        try:
            return Notice.objects.get(slug=notice_slug)
        except Notice.DoesNotExist:
            raise Http404

    def get(self, notice_slug, format=None):
        Notices = self.get_object(notice_slug)
        serializer = NoticeSerializer(Notices)
        return Response(serializer.data)


class LatestGallerylistView(APIView):
    def get(self, request, format=None):
        Gallerys = Gallery.objects.all()[:6]
        if not Gallerys:
            return Response({'message': 'No data found'})
        serializer = GallerySerializer(Gallerys, many=True)
        return Response(serializer.data)


class FullGalleryView(APIView):
    def get_object(self, notice_slug):
        try:
            return Notice.objects.get(slug=notice_slug)
        except Notice.DoesNotExist:
            raise Http404

    def get(self, notice_slug, format=None):
        Notices = self.get_object(notice_slug)
        serializer = NoticeSerializer(Notices)
        return Response(serializer.data)


class ProjectView(APIView):
    def get(self, request, format=None):
        project = projects.objects.all()
        if not project:
            # Corrected variable name
            return Response({'message': 'No data found'})
        serializer = ProjectSerializer(project, many=True)
        return Response(serializer.data)


class MessagesView(APIView):
    def post(self, request, format=None):
        massages = MessagesSerializer(data=request.data)
        if massages.is_valid():
            massages.save()
            return Response(massages.data, status=status.HTTP_201_CREATED)
        return Response(massages.errors, status=status.HTTP_400_BAD_REQUEST)


class FeadbackView(APIView):
    def post(self, request, format=None):
        massages = FeadbackSerializer(data=request.data)
        if massages.is_valid():
            massages.save()
            return Response(massages.data, status=status.HTTP_201_CREATED)
        return Response(massages.errors, status=status.HTTP_400_BAD_REQUEST)


class MentorView(APIView):
    def get(self, request, format=None):
        mentor = list(Mentor.objects.all())
        if not mentor:
            return Response({'message': 'No data found'})
        serializer = MentorSerializer(mentor, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        mentor = Mentor.objects.all()
        if not mentor:
            return Response({'message': 'No data found'})
        serializer = MentorSerializer(mentor, many=True)
        return Response(serializer.data)
