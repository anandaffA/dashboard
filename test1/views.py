from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
import requests

# Create your views here.
def index(request):
    url = 'index.html'
    return render(request, url)


def dashboard(request):
    url = "https://picsum.photos/v2/list"
    # url = "https://picsum.photos/v2/list?page=2&limit=1"
    response = requests.get(url)

    if response.status_code == 200:
        users = response.json()
        # Get page number from request (default is page 1)
        page_number = request.GET.get('page', 1)
        paginator = Paginator(users, 10)  # Show 10 users per page
        page = paginator.get_page(page_number)

        # Return paginated data as JSON
        return JsonResponse({
            'users': list(page),
            'total_pages': paginator.num_pages,
            'current_page': page.number
        })
    
    else :
        return JsonResponse({"error": "Failed to fetch data"}, status=500)
