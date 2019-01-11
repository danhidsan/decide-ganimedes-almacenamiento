from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import csv
import json


class Render:

    def render_pdf(path, params):
        plantilla = get_template(path)
        html = plantilla.render(params)

        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)

        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        
        else:
            return HttpResponse("Error renderizando el archivo PDF", status=400)

    def render_csv(path, params):
        response = HttpResponse(content_type='text/csv', charset='UTF-8')
        response['Content-Disposition'] = 'attachment; filename="resultados.csv"'

        votacion = params['voting']
        writer = csv.writer(response)

        writer.writerow([votacion['name'], votacion['question']['desc']])

        if path == 'visualizer/ended_export.html':
            
            writer.writerow(['Opción', 'Número de votos'])
            resultados = params['voting']['postproc']

            for r in resultados:
                writer.writerow([r['option'], r['votes']])
        
        elif path == 'visualizer/ongoing_export.html':

            writer.writerow(['Estadísticas'])
            writer.writerow(['Tamaño del censo', str(params['stats_census_size'])])
            writer.writerow(['Personas que han votado', str(params['stats_voters_turnout'])])
            writer.writerow(['Porcentaje de participación', str(params['stats_participation_ratio']) + '%'])

            if params['stats_voters_age_mean']:
                writer.writerow(['Edad media de las personas que han votado', str(params['stats_voters_age_mean']) + ' años'])

            if params['stats_no_voters_age_mean']:
                writer.writerow(['Edad media de las personas que no han votado', str(params['stats_no_voters_age_mean']) + ' años'])
            
            writer.writerow(['Análisis de la participación según rango etario'])

            for rango, cantidad in params['stats_voters_age_dist'].items():
                writer.writerow([str(rango) + ' años', str(cantidad) + '%'])

            writer.writerow(['Número de mujeres que han votado', str(params['stats_women_participation'])])
            writer.writerow(['Porcentaje de mujeres que han votado respecto a su total', str(params['stats_women_percentage']) + '%'])
            writer.writerow(['Número de personas de género no binario que han votado', str(params['stats_nonbinary_participation'])])
            writer.writerow(['Porcentaje de personas de género no binario que han votado respecto a su total', str(params['stats_nonbinary_percentage']) + '%'])
            writer.writerow(['Número de hombres que han votado', str(params['stats_men_participation'])])
            writer.writerow(['Porcentaje de hombres que han votado respecto a su total', str(params['stats_men_percentage']) + '%'])

        return response

    def render_json(voting_status, params):
        
        response = HttpResponse(content_type='application/json', charset='UTF-8')
        response['Content-Disposition'] = 'attachment; filename="resultados.json"'

        votacion = params['voting']

        if voting_status == 'ended':
            
            export = {}
            results_main = {}

            # Descripción del informe
            results_description = {}
            results_description['Votación'] = votacion['name']
            results_description['Id'] = votacion['id']

            # Resultados
            results_results = {}
            resultados = votacion['postproc']

            for r in resultados:
                results_results[str(r['option'])] = str(r['votes'])
            
            # Composición de la jerarquía
            results_main['Información de la Votación'] = results_description
            results_main['Resultados'] = results_results

            export['Informe de Resultados'] = results_main

            json.dump(export, response)
        
        elif voting_status == 'ongoing':
            
            export = {}
            stats_main = {}

            #Estadísticas básicas de una votación
            stats_basicas = {}
            stats_basicas['Tamaño del censo'] = str(params['census_size'])
            stats_basicas['Personas que han votado'] = str(params['voters_turnout'])
            stats_basicas['Porcentaje de participación'] = str(params['participation_ratio']) + '%'

            #Estadísticas de edad
            stats_edad = {}
            if params['voters_age_mean']:
                stats_edad['Edad media de las personas que han votado'] = str(params['voters_age_mean']) + ' años'

            if params['no_voters_age_mean']:
                stats_edad['Edad media de las personas que no han votado'] =  str(params['no_voters_age_mean']) + ' años'
            
            #Estadísticas por rango etario
            stats_edad_rango = {} 
            
            for rango, cantidad in params['voters_age_dist'].items():
                stats_edad_rango[str(rango) + ' años'] =  str(cantidad) + '%'

            #Estadísticas por género
            stats_genero = {}
            
            stats_genero['Número de mujeres que han votado'] = str(params['women_participation'])
            stats_genero['Porcentaje de mujeres que han votado respecto a su total'] = str(params['women_percentage']) + '%'
            stats_genero['Número de personas de género no binario que han votado'] = str(params['nonbinary_participation'])
            stats_genero['Porcentaje de personas de género no binario que han votado respecto a su total'] = str(params['nonbinary_percentage']) + '%'
            stats_genero['Número de hombres que han votado'] = str(params['men_participation'])
            stats_genero['Porcentaje de hombres que han votado respecto a su total'] = str(params['men_percentage']) + '%'

            #Composición de la jerarquía
            stats_edad['Análisis de la participación según rango etario'] = stats_edad_rango
            stats_main['Estadísticas básicas de una votación'] = stats_basicas
            stats_main['Estadísticas basadas en la edad'] = stats_edad
            stats_main['Estadísticas basadas en el género'] = stats_genero

            export['Estadísticas'] = stats_main

            json.dump(export, response)

        return response