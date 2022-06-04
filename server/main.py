
from requests import get
from datetime import datetime, timedelta, date
from os import environ
from functools import wraps
from typing import Dict, List, Optional, Tuple, Union
from flask import Flask, redirect, url_for, request, abort, make_response, jsonify, Response, render_template, g, abort
from numpy import array, zeros, nanmean, nanstd, NaN
import sqlite3

############################## Inicialização #############################

#Configuração do Flask
versao_app='1.0.0'
app = Flask(__name__)
app.secret_key = 'app_api'
#app.secret_key = os.environ['SECRETKEY']


################################ Funções  ################################

def zero_to_nan(y):
    x = array(y)
    x[x == 0] = NaN
    return x

def banco_dados():
    return sqlite3.connect('/home/henrique/Downloads/banco_dados.db')

def consultar_banco_dados(consulta:str, unico=False) -> Optional[List[Dict[str,str]]]:
    try:

        cursor = banco_dados().cursor()
        cursor.execute(consulta)
        r = [dict((cursor.description[i][0], valor) \
                for i, valor in enumerate(row)) for row in cursor.fetchall()]
        return (r[0] if r else None) if unico else r

    except Exception as e:
        return None

    finally:
        cursor.connection.close()


################################### Rotas #################################


@app.route('/versao', methods=['GET'])
def versao() -> Response:   
    return make_response(jsonify({'retorno:': f'versao {versao_app}'}), 200)


@app.route('/deputado', methods=['GET'])
def deputado() -> Response:
    id = request.args.get('id')
    
    if id is None:
        deputado = consultar_banco_dados('SELECT id, nome, partido, url_foto FROM identificacao WHERE legislatura_atual=1')
    else:
        try:
            id=int(id)
        except:
            return make_response(jsonify({'erro': 'Id não reconhecido'}), 400)
        deputado = consultar_banco_dados(f'SELECT id, nome, partido, url_foto FROM identificacao WHERE legislatura_atual=1 and id={id}')
    
    if deputado is None: return make_response(jsonify({'erro': 'Não foi possível recuperar as informações'}), 500)
    
    dados_resposta = {'dados': deputado}
    return make_response(jsonify(dados_resposta), 200)


@app.route('/deputado/<id>/despesas/', methods=['GET'])
def despesas_deputado(id:str) -> Response:  

    dataInicio = request.args.get('dataInicio') 
    if dataInicio is None: dataInicio = '2022-01-01'
    dataFim = datetime.now().strftime('%Y-%m-%d')
    
    #Recuperar despesas
    despesas = consultar_banco_dados("SELECT data,valor FROM despesas "
            "WHERE DATE(substr(data,7,4) "
            "||'-'"
            "||substr(data,4,2) "
            "||'-' "
            "||substr(data,1,2)) "
            f"BETWEEN DATE('{dataInicio}') AND DATE('{dataFim}') and id_deputado='{id}' ORDER BY data ASC;")

    #Recuperar estatísticas
    media_despesas = consultar_banco_dados("SELECT avg(valor) as media FROM despesas "
            "WHERE DATE(substr(data,7,4) "
            "||'-' "
            "||substr(data,4,2) "
            "||'-' "
            "||substr(data,1,2)) "
            f"BETWEEN DATE('{dataInicio}') AND DATE('{dataFim}') and id_deputado='{id}' ORDER BY data ASC;")
    
    total_despesas = consultar_banco_dados("SELECT sum(valor) as media FROM despesas "
            "WHERE DATE(substr(data,7,4) " 
            "||'-' "
            "||substr(data,4,2) "
            "||'-' "
            "||substr(data,1,2)) "
            f"BETWEEN DATE('{dataInicio}') AND DATE('{dataFim}') and id_deputado='{id}' ORDER BY data ASC;")
    

    if not despesas or not media_despesas or not total_despesas: 
        return make_response(jsonify({'erro': 'Não foi possível recuperar as informações'}), 500)


    dados_resposta = {
        'dados': {
            'despesas': despesas,
            'media_despesas': media_despesas,
            'total_despesas': total_despesas
        }
    }

    return make_response(jsonify(dados_resposta), 200)


@app.route('/deputado/<id>/proposicoes/', methods=['GET'])
def proposicoes_deputado(id:str) -> Response:  

    #Recuperar proposicoes
    proposicoes = consultar_banco_dados("SELECT proposicoes.siglaTipo, proposicoes.numero, proposicoes.ano, proposicoes.tema, proposicoes.ementa FROM proposicoes "
                                        "INNER JOIN proposicoesDeputado ON proposicoesDeputado.id_proposicao = proposicoes.id "
                                        "INNER JOIN identificacao ON identificacao.id = proposicoesDeputado.id_deputado "
                                        f"WHERE proposicoesDeputado.id_deputado='{id}'")
    if not proposicoes: make_response(jsonify({'erro': 'Não foi possível recuperar as informações'}), 500)

    dados_resposta = {
        'dados': proposicoes
    }

    return make_response(jsonify(dados_resposta), 200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)