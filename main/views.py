from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from scripts.solvro_city import SolvroCity
from .forms import FavouriteForm
from .models import Favourite
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import re


def home(request):
    return render(request, "main/home.html")


def stops(request):
    solvro = SolvroCity("scripts")
    return render(request, "main/stops.html", {"stops": solvro.get_all_stops()})


def stops_api(request):
    solvro = SolvroCity("scripts")
    return HttpResponse(
        json.dumps(solvro.get_all_stops()), content_type="application/json"
    )


class ShortestRoute(View):
    template_name = "main/shortest_route_form.html"
    solvro = SolvroCity("scripts")

    def get(self, request):
        # show the form
        return render(
            request,
            self.template_name,
            {"stops": self.solvro.get_all_stops()},
        )

    def post(self, request):
        try:
            # validate source and target provided data
            source = request.POST.get("source")
            target = request.POST.get("target")

            # check if stops exists
            self.solvro.get_stop_id(source)
            self.solvro.get_stop_id(target)

            # return the shortest route with a distance
            return render(
                request,
                "main/shortest_route.html",
                {
                    "shortest_route": self.solvro.get_shortest_route(
                        source, target
                    ),
                    "source": source,
                    "target": target,
                },
            )
        except ValueError:
            return render(
                request,
                self.template_name,
                {"error": "Wrong data provided."},
            )


def shortest_route_api(request):
    try:
        solvro = SolvroCity("scripts")

        # validate GET parameters
        source = request.GET.get("source")
        target = request.GET.get("target")

        # check if stops exists
        solvro.get_stop_id(source)
        solvro.get_stop_id(target)

        # return json
        return HttpResponse(
            json.dumps(solvro.get_shortest_route(source, target)),
            content_type="application/json",
        )
    except ValueError:
        return HttpResponseBadRequest()


class Favourites(LoginRequiredMixin, View):
    template_name = "main/favourites.html"

    def get(self, request):
        # show the list
        favourites = Favourite.objects.filter(user=request.user)
        return render(request, self.template_name, {"favourites": favourites})

    def post(self, request):
        try:
            # check if favourite doesn't exist already
            if not Favourite.objects.filter(
                user=request.user,
                source=request.POST.get("source"),
                target=request.POST.get("target"),
            ):
                form = FavouriteForm(request.POST)
                new_favourite = form.save(commit=False)
                new_favourite.user = request.user
                new_favourite.save()
            return redirect("favourites")
        except ValueError:
            return redirect("home")


def map(request):
    solvro = SolvroCity("scripts")
    return render(
        request,
        "main/map.html",
        {"stops": solvro.get_all_stops(), "links": solvro.get_all_links()},
    )
