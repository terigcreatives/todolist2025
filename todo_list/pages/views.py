from django.shortcuts import render

# Create your views here.

# Display welcome page of todolist app
def welcome_view(request):
    return render(request, "pages/welcome.html")

def contact_view(request):
    return render(request, "pages/contact.html")
