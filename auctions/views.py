from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


def listing(request, id):
    data = Listing.objects.get(pk=id)
    inwatchlist = request.user in data.watchlist.all()
    allcomments = Comment.objects.filter(listing=data)
    isOwner = request.user.username == data.owner.username
    return render(request, 'auctions/listing.html', {
        'listing': data,
        'inwatchlist': inwatchlist,
        'allcomments': allcomments,
        'isOwner': isOwner
    })


def index(request):
    activelistings = Listing.objects.filter(isactive=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        'listings': activelistings,
        'categories': categories
    })


def removewatchlist(request, id):
    data = Listing.objects.get(pk=id)
    currentuser = request.user
    data.watchlist.remove(currentuser)
    return HttpResponseRedirect(reverse(listing, args=(id, )))


def addwatchlist(request, id):
    data = Listing.objects.get(pk=id)
    currentuser = request.user
    data.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse(listing, args=(id,)))


def watchlist(request):
    currentuser = request.user
    listings = currentuser.listingwatchlist.all()
    return render(request, 'auctions/watchlist.html', {
        'listings': listings
    })


def close(request, id):
    data = Listing.objects.get(pk=id)
    data.isactive = False
    data.save()
    inwatchlist = request.user in data.watchlist.all()
    allcomments = Comment.objects.filter(listing=data)
    return render(request, 'auctions/listing.html', {
        'listing': data,
        'inwatchlist': inwatchlist,
        'allcomments': allcomments,
        'message2': 'Bid Placed Successfully'
    })


def addbid(request, id):
    newbid = int(request.POST['newbid'])
    data = Listing.objects.get(pk=id)
    inwatchlist = request.user in data.watchlist.all()
    allcomments = Comment.objects.filter(listing=data)
    if newbid > data.bid_price.bid:
        updatebid = Bid(user=request.user, bid=newbid)
        updatebid.save()
        data.bid_price = updatebid
        data.save()
        return render(request, 'auctions/listing.html', {
            'listing': data,
            'inwatchlist': inwatchlist,
            'allcomments': allcomments,
            'message': 'Bid Placed Successfully'
        })
    else:
        return render(request, 'auctions/listing.html', {
            'listing': data,
            'inwatchlist': inwatchlist,
            'allcomments': allcomments,
            'message1': 'Bid failed'
        })


def addcomment(request, id):
    currentuser = request.user
    data = Listing.objects.get(pk=id)
    message = request.POST['comment']
    xcomment = Comment(author=currentuser, listing=data, message=message)
    xcomment.save()
    return HttpResponseRedirect(reverse(listing, args=(id,)))


def category_display(request):
    if request.method == 'POST':
        categoryx = request.POST['category']
        categoryname = Category.objects.get(name=categoryx)
        activelistings = Listing.objects.filter(
            isactive=True, category=categoryname)
        categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            'listings': activelistings,
            'categories': categories
        })


def createlisting(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, 'auctions/create.html', {
            'categories': categories
        })
    else:
        title = request.POST['title']
        description = request.POST['description']
        imageurl = request.POST['imageurl']
        price = request.POST['price']
        category = request.POST['category']
        currentuser = request.user
        bid = Bid(bid=float(price), user=currentuser)
        bid.save()
        category_object = Category.objects.get(name=category)

        newlisting = Listing(title=title, description=description, image_url=imageurl,
                             bid_price=bid, category=category_object, owner=currentuser)

        newlisting.save()

        return HttpResponseRedirect(reverse(index))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
