from django.shortcuts import render

class LogInFormView(View):
	form_class = LogInForm
	template_name = "login_form.html"
	def get(self,request):
		form = self.form_class(None)
		
		return render(request,self.template_name,{'form':form})
	def post(self,request):
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
					return redirect('home:index')
		return render(request,self.template_name,{'form':form})