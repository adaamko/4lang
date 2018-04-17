import json
import logging
import os
import re
import sys
import pygraphviz as pgv

from text_to_4lang import TextTo4lang
from flask import Flask
from flask import jsonify
from corenlp_wrapper import CoreNLPWrapper
from dep_to_4lang import DepTo4lang
from lexicon import Lexicon
from magyarlanc_wrapper import Magyarlanc
from utils import ensure_dir, get_cfg, print_text_graph
from flask import json
from flask import request
from pymachine.machine import Machine
from pymachine.utils import MachineGraph


assert Lexicon  # silence pyflakes (Lexicon must be imported for cPickle)

__LOGLEVEL__ = 'INFO'
__MACHINE_LOGLEVEL__ = 'INFO'

app = Flask(__name__)

class MyServer:
    def __init__(self):
        cfg = get_cfg(None)
        self.textto4lang = TextTo4lang(cfg)
        self.textto4lang.graphs_dir = '/home/adaamko/AACS18/4lang/data'
        self.textto4lang.abstract = False
        self.textto4lang.expand = False

my_server = MyServer()


@app.route('/default', methods = ['POST'])
def default():
    r = request.json
    filehyp = '/home/adaamko/projects/4lang/data/' + 'hypothesis' + '.sens'
    fileprem = '/home/adaamko/projects/4lang/data/' + 'premise' + '.sens'
    hyp = r['hyp']
    prem = r['prem']
    return_sentences = {}
    hyp_pro = my_server.textto4lang.preprocess_text(hyp)
    prem_pro = my_server.textto4lang.preprocess_text(prem)
    with open(filehyp, 'w') as f:
        f.write(hyp_pro.encode("utf8"))
    with open(fileprem, 'w') as f:
        f.write(prem_pro.encode("utf8"))
    my_server.textto4lang.input_sens = filehyp
    machines_hyp = my_server.textto4lang.process_file(filehyp, 'hyp')
    graph_hyp = MachineGraph.create_from_machines(
                machines_hyp[0].values())
    return_sentences['hyp'] = graph_hyp.to_dict()

    my_server.textto4lang.input_sens = fileprem
    machines_prem = my_server.textto4lang.process_file(fileprem, 'prem')
    graph_prem = MachineGraph.create_from_machines(
                machines_prem[0].values())    
    return_sentences['prem'] = graph_prem.to_dict()

    return jsonify(return_sentences)

@app.route('/expand', methods = ['POST'])
def expand():
    my_server.textto4lang.abstract = False
    my_server.textto4lang.expand = True
    my_server.textto4lang.dep_to_4lang.lexicon.lexicon = {}
    r = request.json
    filehyp = '/home/adaamko/projects/4lang/data/' + 'exp_hypothesis' + '.sens'
    fileprem = '/home/adaamko/projects/4lang/data/' + 'exp_premise' + '.sens'
    hyp = r['hyp']
    prem = r['prem']
    return_sentences = {}
    hyp_pro = my_server.textto4lang.preprocess_text(hyp)
    prem_pro = my_server.textto4lang.preprocess_text(prem)
    with open(filehyp, 'w') as f:
        f.write(hyp_pro.encode("utf8"))
    with open(fileprem, 'w') as f:
        f.write(prem_pro.encode("utf8"))
    my_server.textto4lang.input_sens = filehyp
    machines_hyp = my_server.textto4lang.process_file(filehyp, 'exp_hyp')
    graph_hyp = MachineGraph.create_from_machines(
                machines_hyp[0].values())
    return_sentences['hyp'] = graph_hyp.to_dict()

    my_server.textto4lang.input_sens = fileprem
    machines_prem = my_server.textto4lang.process_file(fileprem, 'exp_prem')
    graph_prem = MachineGraph.create_from_machines(
                machines_prem[0].values())    
    return_sentences['prem'] = graph_prem.to_dict()

    return jsonify(return_sentences)

@app.route('/abstract', methods = ['POST'])
def abstract():
    my_server.textto4lang.abstract = True
    my_server.textto4lang.expand = True
    my_server.textto4lang.dep_to_4lang.lexicon.lexicon = {}
    r = request.json
    filehyp = '/home/adaamko/projects/4lang/data/' + 'abs_hypothesis' + '.sens'
    fileprem = '/home/adaamko/projects/4lang/data/' + 'abs_premise' + '.sens'
    hyp = r['hyp']
    prem = r['prem']
    return_sentences = {}
    hyp_pro = my_server.textto4lang.preprocess_text(hyp)
    prem_pro = my_server.textto4lang.preprocess_text(prem)
    with open(filehyp, 'w') as f:
        f.write(hyp_pro.encode("utf8"))
    with open(fileprem, 'w') as f:
        f.write(prem_pro.encode("utf8"))
    my_server.textto4lang.input_sens = filehyp
    machines_hyp = my_server.textto4lang.process_file(filehyp, 'abs_hyp')
    graph_hyp = MachineGraph.create_from_machines(
                machines_hyp[0].values())
    return_sentences['hyp'] = graph_hyp.to_dict()

    my_server.textto4lang.input_sens = fileprem
    machines_prem = my_server.textto4lang.process_file(fileprem, 'abs_prem')
    graph_prem = MachineGraph.create_from_machines(
                machines_prem[0].values())    
    return_sentences['prem'] = graph_prem.to_dict()

    return jsonify(return_sentences)


@app.route('/wikidata', methods = ['POST'])
def wikidata():
    my_server.textto4lang.abstract = False
    my_server.textto4lang.expand = True
#    my_server.textto4lang.dep_to_4lang.lexicon.lexicon = {}
    r = request.json
    word = '/home/adaamko/AACS18/4lang/data/' + 'wikidata' + '.sens'
    hyp = r['word']
    return_sentences = {}
    hyp_pro = my_server.textto4lang.preprocess_text(hyp)
    with open(word, 'w+') as f:
        f.write(hyp_pro.encode("utf8"))
    my_server.textto4lang.input_sens = word
    machines_hyp = my_server.textto4lang.process_file(word, 'wikidata')
    graph_hyp = MachineGraph.create_from_machines(
                machines_hyp[0].values())
    return_sentences['word'] = graph_hyp.to_dict()
    return_sentences['lem'] = my_server.textto4lang.get_lem_machine(word)
    return jsonify(return_sentences)



@app.route("/")
def hello():
    return "Hello World!"


if __name__ == '__main__':
    app.run(debug=True)
