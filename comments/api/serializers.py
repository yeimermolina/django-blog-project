from rest_framework.serializers import (
	ModelSerializer, 
	HyperlinkedIdentityField, 
	SerializerMethodField,)

from comments.models import Comment


class CommentSerializer(ModelSerializer):
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
			'content_type',
			'object_id',
			'parent',
			'content',
			'id',
			'reply_count',
		]

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0


class CommentChildSerializer(ModelSerializer):
	class Meta:
		model = Comment
		fields = [
			'timestamp',
			'content',
			'id',
		]


class CommentDetailSerializer(ModelSerializer):
	replies = SerializerMethodField()
	reply_count = SerializerMethodField()
	class Meta:
		model = Comment
		fields = [
			'content_type',
			'object_id',
			'content',
			'id',
			'replies',
			'timestamp',
			'reply_count',
		]

	def get_replies(self, obj):
		if obj.is_parent:
			return CommentChildSerializer(obj.children(), many=True).data
		return None

	def get_reply_count(self, obj):
		if obj.is_parent:
			return obj.children().count()
		return 0