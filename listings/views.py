from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Listing


def index(request):
    listings = Listing.objects.all().order_by("-list_date").filter(is_published=True)
    paginator = Paginator(listings, 2)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    print(page_number)
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj
    }
    
    return render(request, "listings/listings.html", context)
     
     
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    context = {
        "listing": listing
    }
    return render(request, "listings/listing.html", context)
    
def search(request):
    return render(request, "listings/search.html")
