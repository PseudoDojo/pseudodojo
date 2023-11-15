from flask_restful import Resource, Api

class MyApiResource(Resource):
    def get(self):
        # Implementation of GET method
        pass

    def post(self):
        # Implementation of POST method
        pass

def create_api(api):
    api.add_resource(MyApiResource, '/api/resource')