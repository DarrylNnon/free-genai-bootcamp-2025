from comps import ServiceOrchestrator, ServiceRoleType, MicroService
from comps.cores.proto.api_protocol import ChatCompletionRequest, ChatCompletionResponse  # ✅ Fixed import syntax

from fastapi import Request

class Chat:
    def __init__(self):
        print('init')
        self.megaservice = ServiceOrchestrator()
        self.endpoint = '/Darryl-is-great'
        self.host = '0.0.0.0'
        self.port = 8888

    def add_remote_services(self):
        print('add_remote_services')
        # Future: Register remote microservices here using self.megaservice

    def handle_request(self, request: Request):
        print('handle_request')
        # Future: Parse and process ChatCompletionRequest from request here
        return ChatCompletionResponse()  # This line assumes a no-arg constructor is valid

    def start(self):
        print('start')
        self.service = MicroService(
            self.__class__.__name__,
            service_role=ServiceRoleType.MEGASERVICE,
            host=self.host,
            port=self.port,
            endpoint=self.endpoint,
            input_datatype=ChatCompletionRequest,
            output_datatype=ChatCompletionResponse,
        )

        self.service.add_route(self.endpoint, self.handle_request, methods=["POST"])
        self.service.start()


if __name__ == '__main__':
    print('main')
    chat = Chat()
    chat.add_remote_services()
    chat.start()
