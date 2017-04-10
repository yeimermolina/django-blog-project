from rest_framework.serializers import (
	ModelSerializer, 
	HyperlinkedIdentityField, 
	SerializerMethodField,)

from posts.models import Post 


class PostCreateUpdateSerializer(ModelSerializer):
	class Meta:
		model = Post
		fields = [
			'title',
			'content',
			'publish',
		]

class PostDetailSerializer(ModelSerializer):
	user = SerializerMethodField()
	image = SerializerMethodField()
	markdown = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'title',
			'slug',
			'content',
			'publish',
			'user',
			'image',
			'markdown',
		]

	def get_user(self, obj):
		return str(obj.user.username)

	def get_markdown(self, obj):
		return obj.get_markdown()

	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image


class PostListSerializer(ModelSerializer):
	url = HyperlinkedIdentityField(
			view_name = 'posts-api:detail',
			lookup_field = 'slug'
		)

	delete_url = HyperlinkedIdentityField(
			view_name = 'posts-api:delete',
			lookup_field = 'slug'
		)

	user = SerializerMethodField()

	class Meta:
		model = Post
		fields = [
			'id',
			'title',
			'slug',
			'content',
			'publish',
			'user',
			'url',
			'delete_url',
		]

	def get_user(self, obj):
		return str(obj.user.username)


"""
froms posts.models import POst
from posts.api.serializers import PostDEtailsserializer
data = {
	"title":"yeah",
	"content": "new content",
	"publish" : "2016-2-12",
	"slug": "yeah"
}

obj = Post.objects.get(id=2)
new_item = PostDetailsSerializer(obj, data=data)
new_item.save()
"""