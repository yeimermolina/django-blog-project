
from django.db.models import Q

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

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

from comments.models import Comment
from posts.api.permissions import IsOwnerOrReadOnly
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .serializers import CommentSerializer, CommentDetailSerializer, CommentChildSerializer


class CommentDetailAPIView(RetrieveAPIView):
	queryset = Comment.objects.all()
	serializer_class = CommentDetailSerializer
	# http://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
	lookup_field = 'id'


class CommentListAPIView(ListAPIView):
	# queryset = Post.objects.all()
	serializer_class = CommentSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['content', 'user__username']
	pagination_class = PostPageNumberPagination

	def get_queryset(self, *args, **kwargs):
		# queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
		queryset_list = Comment.objects.all()
		q = self.request.GET.get('q')
		if q:
			queryset_list = queryset_list.filter(
				Q(content__icontains=q) |
				Q(user__username__icontains=q)
				).distinct()
		return queryset_list