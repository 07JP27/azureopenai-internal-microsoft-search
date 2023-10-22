from msgraph import GraphServiceClient
from azure.identity.aio import OnBehalfOfCredential
from quart import current_app


class GraphClientBuilder:
    def get_client(obo_token: str, scopes=["https://graph.microsoft.com/.default"]):
        print("hfewoge"+obo_token)


        credential = OnBehalfOfCredential(
            tenant_id=current_app.config["TENANT_ID"] ,
            client_id=current_app.config["CLIENT_ID"],
            client_secret=current_app.config["APP_SECRET"],
            user_assertion=obo_token)

        graph_client = GraphServiceClient(credential, scopes) 
        return graph_client
