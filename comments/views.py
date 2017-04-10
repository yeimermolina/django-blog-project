from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404

from models import Comment
from .forms import CommentForm
# Create your views here.

def comment_thread(request, id):
	# obj =  get_object_or_404(Comment, id=id)
	try:
		obj = Comment.objects.get(id=id)
	except:
		raise Http404

	if not obj.is_parent:
		obj = obj.parent
	# content_object = obj.content_object
	# content_id = obj.content_object.id

	initial_data = {
		"content_type": obj.content_type,
		"object_id": obj.object_id
	}

	comment_form  = CommentForm(request.POST or None, initial= initial_data)

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
				parent_id = parent_obj.id
			)
		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

	context = {
		"comment":obj,
		"comment_form":comment_form,
	}
	return render(request, "comment_thread.html", context)


@login_required
def comment_delete(request, id):
	# obj =  get_object_or_404(Comment, id=id)
	try:
		obj = Comment.objects.get(id=id)
	except:
		raise Http404
	if obj.user != request.user:
		# messages.success(request, "You do not have permission")
		response = HttpResponse("Yoo do no have permission ")
		response.status_code = 403
		return response
	if request.method == "POST":
		parent_obj_url = obj.content_object.get_absolute_url()
		obj.delete()
		messages.success(request, "This has been deleted")
		return HttpResponseRedirect(parent_obj_url)
	context = {
		"object":obj,
	}

	return render(request, "confirm_delete.html", context) 
