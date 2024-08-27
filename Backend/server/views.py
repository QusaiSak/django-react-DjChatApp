from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.db.models import Count
from .serializer import ServerSerializer
from .models import *
from .schema import server_list_docs

class ServerListViewSet(viewsets.ViewSet):
    """
    A viewset for retrieving a list of servers.

    This viewset supports various filtering and annotation options:
    - **Category**: Filter servers by their category name.
    - **Quantity**: Limit the number of servers returned in the response.
    - **User Membership**: Filter servers to include only those where the requesting user is a member.
    - **Server ID**: Retrieve a server by its unique ID.
    - **Number of Members**: Include the count of members in each server in the response.

    The results are serialized and returned in JSON format.
    """
    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """
        Handle GET requests to list servers with optional filters.

        The query parameters can be used to filter and annotate the server list:
        - `category`: Filter servers by category name (string).
        - `qty`: Limit the number of servers returned (integer).
        - `by_user`: Include only servers where the requesting user is a member (boolean).
        - `by_serverid`: Filter by server ID (string). If provided, the user must be authenticated.
        - `with_num_members`: Include the count of members in each server (boolean).

        Args:
            request (HttpRequest): The request object containing query parameters.

        Returns:
            Response: A Response object with serialized server data.

        Raises:
            AuthenticationFailed: If authentication is required but the user is not authenticated.
            ValidationError: 
                - If `by_serverid` is provided but the server with the specified ID does not exist.
                - If `by_serverid` is not a valid integer.
        """
        category = request.query_param.get("category")
        qty = request.query_param.get("qty")
        by_user = request.query_param.get("by_user") == "true"
        by_serverid = request.query_param.get("by_serverid")
        with_num_members = request.query_param.get("with_num_members") == "true"

        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed()

        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_serverid:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()

            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        details=f"Server with id {by_serverid} not found"
                    )
            except ValueError:
                raise ValidationError(details="Invalid server id")

        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
