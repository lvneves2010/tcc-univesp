

import sqlite3
from base64 import encodebytes
from logging import basicConfig, FileHandler, info, warning, error, debug
from datetime import datetime
from os import environ
from typing import Dict, List, Optional, Tuple, Union
from flask import Flask, request, make_response, jsonify, Response

############################## Inicialização #############################

# export SECRETKEY="ab7651a2-e66a-11ec-8fea-0242ac120002"
# export LOGLEVEL=10
# export DB_PATH="/home/henrique/Downloads/banco_dados.db"
# export VERSAO="1.0.0"

#Configuração do Flask
versao_app=environ['VERSAO']
app = Flask(__name__)
app.secret_key = environ['SECRETKEY']

#Logger
basicConfig(handlers=[FileHandler(filename='server.log', encoding='utf-8', mode='a+')], level=int(environ['LOGLEVEL']), format='[%(asctime)s][%(levelname)s] %(message)s', datefmt='%d/%m/%Y %H:%M:%S')


################################ Funções  ################################


def banco_dados():
    #'/home/henrique/Downloads/banco_dados.db'
    return sqlite3.connect(environ['DB_PATH'])


def consultar_banco_dados(consulta:str, unico=False) -> Optional[List[Dict[str,str]]]:
    try:

        cursor = banco_dados().cursor()
        cursor.execute(consulta)
        r = [dict((cursor.description[i][0], valor) \
                for i, valor in enumerate(row)) for row in cursor.fetchall()]
        return (r[0] if r else None) if unico else r

    except Exception as e:
        print(e)
        return None

    finally:
        cursor.connection.close()


def alterar_banco_dados(comando) -> bool:
    try:
        conexao = banco_dados()
        cursor = conexao.cursor()
        cursor.execute(comando)
        conexao.commit()
        return True

    except Exception as e:
        return False

    finally:
        conexao.commit()
        conexao.close()


################################### Rotas #################################


@app.route('/versao', methods=['GET'])
def versao() -> Response:   
    return make_response(jsonify({'retorno:': f'versao {versao_app}'}), 200)


@app.route('/deputado', methods=['GET'])
def deputado() -> Response:
    id = request.args.get('id')
    foto = request.args.get('foto')
    limite = request.args.get('limite')

    if limite is None: limite = 10
    
    if id is None:
        
        deputado = consultar_banco_dados("SELECT identificacao.id, identificacao.nome, identificacao.partido, "
                                        f"{'identificacao.fotoBase64, ' if foto == '1' else 'identificacao.url_foto, '}"
                                        "identificacao.partido_uf, identificacao.email, despesas.valor as despesa_mes FROM identificacao "
                                        "INNER JOIN despesas ON despesas.id_deputado = identificacao.id "
                                        "WHERE identificacao.legislatura_atual=1 AND "
                                        "DATE(substr(despesas.data,7,4) "
                                        "||'-' "
                                        "||substr(despesas.data,4,2) "
                                        "||'-' "
                                        "||substr(despesas.data,1,2)) "
                                        "BETWEEN DATE(strftime('%Y-%m', datetime('now')) || '-' || '01') AND "
                                        "DATE(strftime('%Y-%m', datetime('now')) || '-' || '31')"
                                        f"LIMIT {limite}")
        info(f'Consultado informações de todos os deputados')
        
    else:
        try:
            id=int(id)
        except:
            return make_response(jsonify({'erro': 'Id não reconhecido'}), 400)
        
        deputado = consultar_banco_dados("SELECT identificacao.id, identificacao.nome, identificacao.partido, "
                                        f"{'identificacao.fotoBase64, ' if foto == '1' else 'identificacao.url_foto, '}"
                                        "identificacao.partido_uf, identificacao.email, despesas.valor as despesa_mes FROM identificacao "
                                        "INNER JOIN despesas ON despesas.id_deputado = identificacao.id "
                                        "WHERE identificacao.legislatura_atual=1 AND "
                                        f"identificacao.id = '{id}' AND "
                                        "DATE(substr(despesas.data,7,4) "
                                        "||'-' "
                                        "||substr(despesas.data,4,2) "
                                        "||'-' "
                                        "||substr(despesas.data,1,2)) "
                                        "BETWEEN DATE(strftime('%Y-%m', datetime('now')) || '-' || '01') AND "
                                        "DATE(strftime('%Y-%m', datetime('now')) || '-' || '31')"
                                        f"LIMIT {limite}")
        info(f'Consultado informações do deputado (id {id})')
    
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

    info(f'Consultado despesas do deputado (id {id})')
    return make_response(jsonify(dados_resposta), 200)


@app.route('/deputado/<id>/proposicoes/', methods=['GET'])
def proposicoes_deputado(id:str) -> Response:  

    #Recuperar proposicoes
    proposicoes = consultar_banco_dados("SELECT proposicoes.siglaTipo, proposicoes.numero, proposicoes.ano, proposicoes.tema, proposicoes.ementa FROM proposicoes "
                                        "INNER JOIN proposicoesDeputado ON proposicoesDeputado.id_proposicao = proposicoes.id "
                                        "INNER JOIN identificacao ON identificacao.id = proposicoesDeputado.id_deputado "
                                        f"WHERE proposicoesDeputado.id_deputado='{id}'")
    if not proposicoes: return make_response(jsonify({'erro': 'Não foi possível recuperar as informações'}), 500)

    dados_resposta = {
        'dados': proposicoes
    }

    info(f'Consultado proposições do deputado (id {id})')
    return make_response(jsonify(dados_resposta), 200)


@app.route('/deputado/<id>/votacoes/', methods=['GET'])
def votacoes_deputado(id:str) -> Response:  

    todas_votacoes = request.args.get('todasVotacoes') 

    if todas_votacoes is None: 
        #Recuperar votacoes do deputado apenas do mês atual
        mes_atual = datetime.now().month 
        votacoes = consultar_banco_dados("SELECT proposicoes.tema, proposicoes.siglaTipo, proposicoes.numero, "
                                        "votacoes.data, votacoes.descricao, votos.voto, identificacao.nome FROM votos "
                                        "INNER JOIN identificacao ON identificacao.id = votos.id_deputado "
                                        "INNER JOIN votacoes ON votacoes.id = votos.id_votacao "
                                        "INNER JOIN proposicoes ON proposicoes.id = votacoes.id_proposicao "
                                        "WHERE DATE(substr(votacoes.data,7,4) "
                                        "||'-' "
                                        "||substr(votacoes.data,4,2) "
                                        "||'-' "
                                        "||substr(votacoes.data,1,2)) "
                                        f"BETWEEN DATE('2022-{mes_atual:02d}-01') AND DATE('2022-{mes_atual:02d}-31') and identificacao.id = '{id}' ORDER BY votacoes.data ASC")
    else:
        #Recuperar todas as votações do deputado
        votacoes = consultar_banco_dados("SELECT proposicoes.tema, proposicoes.siglaTipo, proposicoes.numero, "
                                        "votacoes.data, votacoes.descricao, votos.voto, identificacao.nome FROM votos "
                                        "INNER JOIN identificacao ON identificacao.id = votos.id_deputado "
                                        "INNER JOIN votacoes ON votacoes.id = votos.id_votacao "
                                        "INNER JOIN proposicoes ON proposicoes.id = votacoes.id_proposicao "
                                        f"WHERE identificacao.id = '{id}' ORDER BY votacoes.data ASC")
    
    if not votacoes: return make_response(jsonify({'erro': 'Não foi possível recuperar as informações'}), 500)

    dados_resposta = {
        'dados': votacoes
    }
    info(f'Consultado votações do deputado (id {id})')
    return make_response(jsonify(dados_resposta), 200)


@app.route('/favorito', methods=['POST', 'DELETE'])
def favorito() -> Response:

    #Validar entradas
    email = request.args.get('email')   
    id_deputado = request.args.get('idDeputado') 

    if not email or not id_deputado:
        return make_response(jsonify({'erro': 'E-mail e/ou ID do deputado faltante'}), 400)

    #Verificar se o ID do deputado existe
    informacoes_deputado = consultar_banco_dados(f"SELECT * FROM identificacao WHERE id={id_deputado}", unico=True)
    if not informacoes_deputado: return make_response(jsonify({'erro': 'ID de deputado inexistente'}), 400)

    #Adicionar favorito
    if request.method == 'POST':
        acao='Adicionado'
        sucesso = alterar_banco_dados(f"INSERT OR IGNORE INTO favoritos (email_usuario, id_deputado) VALUES ('{email}', {id_deputado})")
    
    #Remover favorito
    else:
        acao='Removido'
        sucesso = alterar_banco_dados(f"DELETE FROM favoritos WHERE email_usuario='{email}' and id_deputado={id_deputado}")

    #Retornar mensagem ao usuário
    if not sucesso:
        return make_response(jsonify({'erro': 'Não foi possível modificar as informações'}), 500)
    else:
        info(f'{acao} cadastro do deputado (id {id_deputado}) {informacoes_deputado.get("nome")} como favorito para o e-mail {email}')
        return make_response(jsonify({'dados': 'sucesso'}), 200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)