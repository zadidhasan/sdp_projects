from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import PostForm
from django.utils import timezone
from .models import Post
# Create your views here.

def PostView(request):
	if not request.user.is_authenticated:
		return redirect("/login/")
	form = PostForm()
	if request.method =="POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.pulished_date = timezone.now()
			post.save()
			
			return redirect("/")
	else:
		form = PostForm()
		return render(request,'post.html',{'form':form})
	return render(request,'post.html',{'form':form})
