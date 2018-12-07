from django.shortcuts import render
from TestBlog.models import BlogsPost
# Create your views here.


def BlogShowInHtml(request):
    blog_list = BlogsPost.objects.all()
    return render(request, 'BlogIndex.html', {'blog_list': blog_list})