from msgraph import GraphServiceClient
from azure.identity.aio import OnBehalfOfCredential
from quart import current_app
import asyncio


class GraphClientBuilder: 
    def get_client(self, obo_token: str, scopes=['https://graph.microsoft.com/.default']):
        credential = OnBehalfOfCredential(
            tenant_id=current_app.config["TENANT_ID"] ,
            client_id=current_app.config["CLIENT_ID"],
            client_secret=current_app.config["APP_SECRET"],
            user_assertion=obo_token)
        graph_client = GraphServiceClient(credential, scopes)
        return graph_client
