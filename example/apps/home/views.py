from raystack.shortcuts import render_template

# Create your views here.

def home_view(request):
    return render_template(request, "home/home.html", context={"framework": "Raystack"})
