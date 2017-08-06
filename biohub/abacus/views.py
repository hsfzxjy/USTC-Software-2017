import json

from django.shortcuts import render
from rest_framework import viewsets, decorators
from django.http import Http404

from ..abacus import responses


class AbacusView(viewsets.GenericViewSet):

    def list_abacus(self):
        return responses.list_abacus(self.request.user)

    def get_status(self, id):
        return responses.get_status(self.request.user, id)

    def get_download_file(self, id):
        return responses.get_download_file(self.request.user, id)

    def upload_file(self, jsn, files):
        return responses.upload_file(self.request.user, jsn, files)

    def delete_file(self, id):
        return responses.delete_file(self.request.user, id)

    def calculate(self, id):
        return responses.calculate(self.request.user, id)

    def edit_abacus(self, jsn, files):
        return responses.edit_abacus(self.request.user, jsn, files)

    @decorators.list_route(methods=['GET'])
    def download(self, request):
        return responses.download_service(self.request.user, request.GET['id'])

    @decorators.list_route(methods=['GET', 'POST'])
    def upload(self, request):
        print('upload...')
        return self.upload_file(json.load(request.body), request.FILES.getlist('files'))

    @decorators.list_route(methods=['GET', 'POST'])
    def edit(self, request):
        return self.edit_abacus(json.load(request.body), request.FILES.getlist('files'))

    @decorators.list_route(methods=['GET', 'POST'])
    def action(self, request):
        # request.POST.
        print("\n----------------\n", request.body, request.POST, request.GET, '\n-----------------\n')

        print(str(json.dumps(str(request.POST.dict()))))
        jsn = json.loads(json.dumps(str(request.POST.dict())))
        method = jsn['method']
        id = jsn['data']

        if method == "get_download_file":
            return self.get_download_file(id)
        elif method == "get_status":
            return self.get_status(id)
        elif method == "list_abacus":
            return self.list_abacus()
        elif method == "delete_file":
            return self.delete_file(id)
        elif method == "calculate":
            return self.calculate(id)
        else:
            return Http404('No such method was found!')

    @decorators.list_route(methods=['Get', 'Post'])
    def index(self, request):
        return render(request, 'abacus.html')
