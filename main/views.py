from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from scripts.solvro_city import SolvroCity
from .forms import FavouriteForm
from .models import Favourite
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import views
from rest_framework.response import Response
from .serializers import StopsSerializer, ShortestRouteSerializer
import json
import re


class Home(View):
    def get(self, request):
        return render(request, "main/home.html")


class Stops(View):
    def get(self, request):
        solvro = SolvroCity("scripts")
        return render(
            request, "main/stops.html", {"stops": solvro.get_all_stops()}
        )


class StopsAPI(views.APIView):
    def get(self, request):
        solvro = SolvroCity("scripts")

        data = solvro.get_all_stops()
        result = StopsSerializer(data, many=True).data
        return Response(result)


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


class ShortestRouteAPI(views.APIView):
    def get(self, request):
        try:
            solvro = SolvroCity("scripts")

            # validate GET parameters
            source = request.GET.get("source")
            target = request.GET.get("target")

            # check if stops exists
            solvro.get_stop_id(source)
            solvro.get_stop_id(target)

            data = solvro.get_shortest_route(source, target)
            result = ShortestRouteSerializer(data).data
            return Response(result)
        except ValueError:
            return Response(
                ShortestRouteSerializer({"distance": 0, "route": []}).data
            )


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


class Map(View):
    def get(self, request):
        solvro = SolvroCity("scripts")
        return render(
            request,
            "main/map.html",
            {"stops": solvro.get_all_stops(), "links": solvro.get_all_links()},
        )
