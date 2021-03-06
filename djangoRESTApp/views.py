from djangoRESTApp.models import Snippet
from django.contrib.auth.models import User
from djangoRESTApp.serializers import SnippetSerializer, UserSerializer
from djangoRESTApp.permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions, renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

@api_view(('GET',))
def Home(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'snippets': reverse('snippet-list', request=request, format=format)
	})


class SnippetList(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer


class SnippetHighlight(generics.GenericAPIView):
	queryset = Snippet.objects.all()
	renderer_classes = (renderers.StaticHTMLRenderer,)

	def get(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)


class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer