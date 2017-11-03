from django.shortcuts import render
from django.http import HttpResponse
from post.models import Post
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.views import generic
from django.views.generic import View
from .forms import UserForm,LoginForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from comment.models import Comment
from comment.forms import CommentForm
from django.http import HttpResponseRedirect
# Create your views here.


def ProfileView(request):
	username = request.user.username
	objects = User.objects.filter(username = username)
	dict = {'user',objects}
	return render(request,'profile.html',dict)

def logout_view(request):
    logout(request)
    return redirect("/login/")

def HomeView(request):
	if not request.user.is_authenticated:
		return redirect("/login/")
	today = timezone.now().date()
	queryset_list = Post.objects.all()
	query = request.GET.get('query')
	if query:
		queryset_list = queryset_list.filter(Q(title__icontains=query)|Q(text__icontains=query)|Q(author__username__icontains=query)).distinct()

	dict ={'posts':queryset_list}
	return render(request,'index.html',dict)



def detailView(request,post_id):
	if not request.user.is_authenticated:
		return redirect("/login/")
	
	objects = Post.objects.filter(id=post_id)
	#objects = get_object_or_404(Post,id=post_id)
	content_type = ContentType.objects.get_for_model(Post)
	for obj in objects:
		obj_id = obj.id
	initial_data = {
		"content_type" : content_type,
		"object_id" : obj_id,
	}
	comment_form = CommentForm(request.POST or None,initial = initial_data)
	if comment_form.is_valid():
		c_type = comment_form.cleaned_data.get('content_type')
		content_type = ContentType.objects.get(model = c_type)
		obj_id = comment_form.cleaned_data.get('object_id')
		content_data = comment_form.cleaned_data.get('content')
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

	comments = Comment.objects.filter(content_type = content_type, object_id=obj_id,parent = None)
	dict ={'post':objects,'comments':comments,'comment_form':comment_form}
	return render(request,'detail.html',dict)	


def profileView(request):
	if not request.user.is_authenticated:
		return redirect("/login/")
	return render(request,'profile.html',{})

class UserFormView(View):
	
	form_class = UserForm
	template_name = "registration_form.html"
	def get(self,request):
		if request.user.is_authenticated:
			return redirect('/')
		form = self.form_class(None)
		
		return render(request,self.template_name,{'form':form})
	def post(self,request):
		if request.user.is_authenticated:
			return redirect('/')
		form = self.form_class(request.POST)
		
		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()
			user = authenticate(username= username, password = password)
			if user is not None:
				if user.is_active:
					login(request,user)
					return render(request,'index.html',{'posts':Post.objects.all()})
					return redirect('home:index')
		return render(request,self.template_name,{'form':form})



class LogInFormView(View):
	
	form_class = LoginForm
	template_name = "login_form.html"
	def get(self,request):
		if not request.user.is_authenticated:
			return redirect("/login/")
		form = self.form_class(None)
		
		return render(request,self.template_name,{'form':form})
	def post(self,request):
		if not request.user.is_authenticated:
			return redirect("/login/")
		form = self.form_class(request.POST)

		if form.is_valid():
			
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			user = User.objects.filter(username = username, password = password)
			if user is not None:
				if user.is_active:
					login(request,user)
					return render(request,'index.html',{'posts':Post.objects.all()})
					return redirect('home:index')
		return render(request,self.template_name,{'form':form})



