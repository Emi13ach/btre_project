from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Listing
from .choices import bedroom_choices, price_choices, state_choices



def index(request):
    listings = Listing.objects.all().order_by("-list_date").filter(is_published=True)
    paginator = Paginator(listings, 3)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    print(page_number)
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj
    }
    
    return render(request, "listings/listings.html", context)
     
     
def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        "listing": listing
    }
    return render(request, "listings/listing.html", context)
    
    
def search(request):
    queryset_list = Listing.objects.order_by("-list_date")
    
    # Keywords
    if "keywords" in request.GET:
        keywords = request.GET["keywords"]
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    
    # City
    if "city" in request.GET:
        city = request.GET["city"]
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
            
    # State
    if "state" in request.GET:
        state = request.GET["state"]
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)
    
    # Bedrooms
    if "bedrooms" in request.GET:
        bedrooms = request.GET["bedrooms"]
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__gte=bedrooms)

    # Price
    if "price" in request.GET:
        price = request.GET["price"]
        if price:
            queryset_list = queryset_list.filter(price__lte=price)
    
    context = {
        "listings": queryset_list,
        "bedroom_choices": bedroom_choices,
        "price_choices": price_choices,
        "state_choices": state_choices,
        "values": request.GET
    }
    return render(request, "listings/search.html", context)
