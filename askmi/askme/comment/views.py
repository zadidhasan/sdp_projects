from django.shortcuts import render

def CommentView:
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
