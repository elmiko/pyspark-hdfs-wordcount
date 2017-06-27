import argparse
import operator

import flask
from flask import views
import pyspark.sql as pyspark


class IndexView(views.MethodView):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.spark = (
            pyspark.SparkSession.builder.appName('WordCount').getOrCreate())

    def get(self):
        counts = None
        count = int(flask.request.args.get('count', 20))
        if flask.request.args.has_key('path'):
            path = flask.request.args.get('path')
            text_file = self.spark.sparkContext.textFile(
                'hdfs://{host}:{port}/{path}'.format(
                host=self.host, port=self.port, path=path))
            words = (text_file
                .flatMap(lambda line: line.split(" "))
                .map(lambda word: (word, 1))
                .reduceByKey(operator.add)
                .sortBy(lambda w: w[1]))
            values = words.collect()[::-1]
            counts = ["{} = {}".format(v[0], v[1]) for v in values[1:count]]
        return flask.render_template('index.html', counts=counts)


def main():
    parser = argparse.ArgumentParser(
        description='count words in an hdfs file')
    parser.add_argument('--host', help='the hdfs host', required=True)
    parser.add_argument('--port', help='the hdfs port', required=True,
                        type=int)
    args = parser.parse_args()
    app = flask.Flask(__name__)
    app.add_url_rule('/',
        view_func=IndexView.as_view('index', args.host, args.port))
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    main()
