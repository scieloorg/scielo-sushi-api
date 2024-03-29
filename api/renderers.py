import csv

from io import StringIO


class TSVRenderer(object):
    def __init__(self, info):
        pass

    def __call__(self, value, system):
        request = system.get('request')

        if request is not None:
            response = request.response

            ct = response.content_type
            if ct == response.default_content_type:
                response.content_type = 'text/tsv'

            fout = StringIO()

            writer = csv.writer(fout, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for r in value.get('rows'):
                writer.writerow(r)

            return fout.getvalue()
