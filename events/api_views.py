from django.http import JsonResponse

from .models import Conference, Location, State
from common.json import ModelEncoder
from django.views.decorators.http import require_http_methods
import json


class LocationListEncoder(ModelEncoder):
    model = Location
    properties = ["name"]


class LocationDetailEncoder(ModelEncoder):
    model = Location
    properties = [
        "name",
        "city",
        "room_count",
        "created",
        "updated",
    ]

    def get_extra_data(self, o):
        return {"state": o.state.abbreviation}


class ConferenceDetailEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
        "description",
        "max_presentations",
        "max_attendees",
        "starts",
        "ends",
        "created",
        "updated",
        "location",
    ]
    encoders = {
        "location": LocationListEncoder(),
    }


class ConferenceListEncoder(ModelEncoder):
    model = Conference
    properties = [
        "name",
    ]


@require_http_methods(["GET", "POST"])
def api_list_conferences(request):
    """Description
    Lists the conference names and the link to the conference.

    Returns a dictionary with a single key "conferences" which
    is a list of conference names and URLS. Each entry in the list
    is a dictionary that contains the name of the conference and
    the link to the conference's information.

    {
        "conferences": [
            {
                "name": conference's name,
                "href": URL to the conference,
            },
            ...
        ]
    }
    """
    if request.method == "GET":
        conferences = Conference.objects.all()
        return JsonResponse(
            {"conferences": conferences}, encoder=ConferenceListEncoder
        )
    else:
        content = json.loads(request.body)
        try:
            location = Location.objects.get(id=content["location"])
            content["location"] = location
        except Location.DoesNotExist:
            return JsonResponse({"message": "Invalid location id"}, status=400)
        conference = Conference.objects.create(**content)
        return JsonResponse(
            conference, encoder=ConferenceDetailEncoder, safe=False
        )


@require_http_methods(["GET", "PUT", "DELETE"])
def api_show_conference(request, id):
    """Description
    Returns the details for the Conference model specified
    by the id parameter.

    This should return a dictionary with the name, starts,
    ends, description, created, updated, max_presentations,
    max_attendees, and a dictionary for the location containing
    its name and href.

    {
        "name": the conference's name,
        "starts": the date/time when the conference starts,
        "ends": the date/time when the conference ends,
        "description": the description of the conference,
        "created": the date/time when the record was created,
        "updated": the date/time when the record was updated,
        "max_presentations": the maximum number of presentations,
        "max_attendees": the maximum number of attendees,
        "location": {
            "name": the name of the location,
            "href": the URL for the location,
        }
    }
    """
    if request.method == "GET":
        conference = Conference.objects.get(id=id)
        return JsonResponse(
            conference, encoder=ConferenceDetailEncoder, safe=False
        )
    elif request.method == "PUT":
        content = json.loads(request.body)
        try:
            if "location" in content:
                real_location = Location.objects.get(name=content["location"])
                content["location"] = real_location
        except Location.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid location name"},
                status=400,
            )
        Conference.objects.filter(id=id).update(**content)
        conference = Conference.objects.get(id=id)
        return JsonResponse(
            conference, encoder=ConferenceDetailEncoder, safe=False
        )
    else:
        conference = Conference.objects.get(id=id)
        conference.delete()
        return JsonResponse({"delete": "successful"})


@require_http_methods(["GET", "POST"])
def api_list_locations(request):
    """Description
    Lists the location names and the link to the location.

    Returns a dictionary with a single key "locations" which
    is a list of location names and URLS. Each entry in the list
    is a dictionary that contains the name of the location and
    the link to the location's information.

    {
        "locations": [
            {
                "name": location's name,
                "href": URL to the location,
            },
            ...
        ]
    }
    """
    """GET Explanation - Get Locations
    if request.method is a GET request:
        create variable and set it equal to all the objects
        return jsonresponse dictionary, where key is a string and variable is the value. Use encoder
    """
    """POST Explanation - Create Location
        We know that content is in the request.body
        Attach content of post to a variable. Must use the json.loads method to convert json to python
        Set return variable to the content variable by unpacking the content variable
        Return like any other
    """
    if request.method == "GET":
        locations = Location.objects.all()
        return JsonResponse(
            {"locations": locations}, encoder=LocationListEncoder
        )
    else:
        content = json.loads(request.body)
        # Get the state object and insert it into content since it's from a foreign key
        try:
            state = State.objects.get(abbreviation=content["state"])
            content["state"] = state
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )
        location = Location.objects.create(**content)
        return JsonResponse(
            location, encoder=LocationDetailEncoder, safe=False
        )


@require_http_methods(["DELETE", "GET", "PUT"])
def api_show_location(request, id):
    """Description
    Returns the details for the Location model specified
    by the id parameter.

    This should return a dictionary with the name, city,
    room count, created, updated, and state abbreviation.

    {
        "name": location's name,
        "city": location's city,
        "room_count": the number of rooms available,
        "created": the date/time when the record was created,
        "updated": the date/time when the record was updated,
        "state": the two-letter abbreviation for the state,
    }
    """
    """GET Explanation
    Get specific instance of a location by matching id's
    Set equal to a variable, return variable via JsonReponse with an encoder
    """
    """PUT Explanation
    Retrieve request body from Insomnia, convert to Python and set to variable
    State will need access to foreign key to get actual abbreviation
    Create 2nd variable accessing state and look for abbreviation key that is equal to variable[state] which is what you write in the body
    Set the variable[state] to that 2nd variable
    Create except condition for if someone provides nonexistent abbreviation

    Now update that instance of Location by pairing ID's. Set instance to variable and return it, like Show Location Detail function
    """
    """DELETE Explanation
    After setting the Queryset equal to a variable, delete the variable
    Return JsonResponse with any dictionary string that should be output when delete is successful
    """
    if request.method == "GET":
        location = Location.objects.get(id=id)
        return JsonResponse(
            location, encoder=LocationDetailEncoder, safe=False
        )
    elif request.method == "DELETE":
        location = Location.objects.get(id=id)
        location.delete()
        return JsonResponse({"delete": "successful"})
    else:
        content = json.loads(request.body)
        try:
            if "state" in content:
                abbrev = State.objects.get(abbreviation=content["state"])
                content["state"] = abbrev
        except State.DoesNotExist:
            return JsonResponse(
                {"message": "Invalid state abbreviation"},
                status=400,
            )
        Location.objects.filter(id=id).update(**content)
        location = Location.objects.get(id=id)
        return JsonResponse(
            location, encoder=LocationDetailEncoder, safe=False
        )
