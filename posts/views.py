from urllib import quote_plus

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.db.models import Q

from .models import Post
from .forms import PostForm
from comments.models import Comment
from comments.forms import CommentForm
# Create your views here.

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Successfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
	if request.method=="POST":
		print request.POST
	context = {
		'form' : form
	}
	return render(request, "post_form.html", context)


def post_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	comments = instance.comments
	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id
	}
	comment_form = CommentForm(request.POST or None, initial=initial_data)

	if comment_form.is_valid() and request.user.is_authenticated():
		print(comment_form.cleaned_data)
		c_type = comment_form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = comment_form.cleaned_data.get("object_id")
		content_data = comment_form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()

		new_comment, created = Comment.objects.get_or_create(
				user = request.user,
				content_type = content_type,
				object_id = obj_id,
				content = content_data,
				parent = parent_obj
			)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())


	context = {
		"title": "Detail",
		"post": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form": comment_form,
	}
	return render(request, "post_detail.html", context)


def post_list(request):
	qs_list = Post.objects.active_posts()
	if request.user.is_staff or request.user.is_superuser:
		qs_list = Post.objects.all()
	
	q = request.GET.get('q')
	if q:
		qs_list = qs_list.filter(
			Q(title__icontains=q)|
			Q(content__icontains=q) |
			Q(user__username__icontains=q)
			).distinct()

	paginator = Paginator(qs_list, 2) # Show 25 contacts per page

	
	page = request.GET.get('page')
	try:
		qs = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		qs = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		qs = paginator.page(paginator.num_pages)
	context = {
		"queryset": qs,
		"title": "List Page"
	}

	return render(request, "post_list.html", context)


def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Successfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"title": "Detail",
		"post": instance,
		"form": form
	}
	return render(request, "post_form.html", context)


def post_delete(request, id= None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Successfully deleted")
	return redirect("posts:list")