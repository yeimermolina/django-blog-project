
from django.db.models import Q

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)


from .pagination import PostLimitOffsetPagination, PostPageNumberPagination


from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView, 
	UpdateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView
	)

from rest_framework.permissions import (
	AllowAny,
	IsAuthenticated,
	IsAdminUser,
	IsAuthenticatedOrReadOnly,
	)

from posts.models import Post
from .serializers import PostCreateUpdateSerializer, PostListSerializer, PostDetailSerializer

from .permissions import IsOwnerOrReadOnly

class PostCreateAPIView(CreateAPIView):
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticated]
	def perform_create(self, serializer):
		serializer.save(user=self.request.user, title="my title")

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	# http://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
	lookup_field = 'slug'


class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	# http://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
	lookup_field = 'slug'

	def perform_update(self, serializer):
		serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
	# http://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
	lookup_field = 'slug'


class PostListAPIView(ListAPIView):
	# queryset = Post.objects.all()
	serializer_class = PostListSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['title', 'content', 'user__username']
	pagination_class = PostPageNumberPagination

	def get_queryset(self, *args, **kwargs):
		# queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
		queryset_list = Post.objects.all()
		q = self.request.GET.get('q')
		if q:
			queryset_list = queryset_list.filter(
				Q(title__icontains=q)|
				Q(content__icontains=q) |
				Q(user__username__icontains=q)
				).distinct()
		return queryset_list



