from flask import render_template, make_response, send_file
from flask_restful import Resource

from api import api
from ..services import stats_service


class StatsOverview(Resource):

    def get(self):
        data = stats_service.list_stats()
        return make_response(render_template("index.html", data=data))


class StatsSheet(Resource):

    def get(self):
        return send_file('../covid19_piracicaba_sp.xlsx', as_attachment=True)


api.add_resource(StatsOverview, '/')
api.add_resource(StatsSheet, '/planilha')
