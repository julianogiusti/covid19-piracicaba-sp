from flask import render_template, make_response
from flask_restful import Resource

from api import api
from ..services import stats_service


class StatsOverview(Resource):

    def get(self):
        data = stats_service.list_stats()
        return make_response(render_template("index.html", data=data))


api.add_resource(StatsOverview, '/')
