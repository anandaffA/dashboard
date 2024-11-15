from django.shortcuts import render
from urllib.parse import urlparse, parse_qs
from django.http import JsonResponse
from django.core.paginator import Paginator
import requests

# Create your views here.
def index(request):
    url = 'index.html'
    return render(request, url)

def dashboard(request):
    url = 'dashboard.html'
    return render(request, url)

def get_images(request):
    url = 'https://picsum.photos/v2/list'
    params = {
        'page': request.GET.get('page', 1),
        'limit': request.GET.get('limit', 9),
    }
    response = requests.get(url, params=params)

    # Check the Link header
    link_header = response.headers.get('Link')
    images = response.json()

    # Optionally, parse the Link header if needed
    pagination_links = parse_link_header(link_header) if link_header else {}
    def extract_page_from_url(full_url):
        parsed_url = urlparse(full_url)
        query_params = parse_qs(parsed_url.query)
        page = query_params.get('page', ['1'])[0]  # Default to '1' if not found
        limit = query_params.get('limit', [params["limit"]])[0]  # Use current limit if not found
        return f'/photos?page={page}&limit={limit}'
        
    next_page_url = extract_page_from_url(pagination_links.get("next")) if pagination_links.get('next') else None

    return JsonResponse({
        'images': images,
        'pagination': next_page_url,
    })

    
def parse_link_header(header):
    links = {}
    parts = header.split(', ')
    for part in parts:
        section = part.split('; ')
        url = section[0].replace('<', '').replace('>', '')
        rel = section[1].replace('rel="', '').replace('"', '')
        links[rel] = url
    return links