import contextlib
import json
import os

from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute

from resolvers import graphql_app


@contextlib.asynccontextmanager
async def lifespan(app):
    filename = "schools.json"
    if not os.path.exists(filename):
        with open(
            filename, "w"
        ) as file:  # Create the file and write an empty list to it
            json.dump([], file)  # Write an empty list in JSON format
    print("Run on startup!")
    yield
    # os.remove(filename)
    print("Run on shutdown!")


# Custom route handlers
async def graphql_route(request):
    return await graphql_app.handle_request(request)


async def websocket_route(websocket):
    await graphql_app.handle_websocket(websocket)


# Create Starlette App instance with custom routes
app = Starlette(
    lifespan=lifespan,
    routes=[
        Route("/graphql/", graphql_route, methods=["GET", "POST", "OPTIONS"]),
        WebSocketRoute("/graphql/", graphql_app.handle_websocket),
    ],
)
