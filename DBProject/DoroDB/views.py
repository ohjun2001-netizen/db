from django.shortcuts import render

def index_view(request):
    # 'index.html' 템플릿을 렌더링
    return render(request, 'index.html')

