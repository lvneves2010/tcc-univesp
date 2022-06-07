
import sqlite3
from base64 import encodebytes
from requests import get
from datetime import datetime, timedelta, date
from typing import List, Optional, Tuple, Union, Any, Dict
from numpy import zeros


################################ Funções  ################################


def gerar_base_dados_votacoes() -> None:
    try:
        #Conectar banco de dados
        conexao_db = sqlite3.connect('/home/henrique/Downloads/banco_dados.db')
        cursor = conexao_db.cursor()

        quantidade_anos = 3 #34
        ano_atual = datetime.utcnow().date().year
        anos = [str(ano_atual-delta) for delta in list(reversed(range(quantidade_anos)))]
        anos = ['2019']
        meses = [
           #('01','03'), 
           #('04','07') ,
           ('08', '10'), 
            ('11','12')
            ]

        for ano in anos:
            for (mes_inicio, mes_fim) in meses:
                print(f'Buscando votações ano {ano} dentro dos meses {mes_inicio} e {mes_fim}')
                #Montar a primeira URL
                prox_url = f'https://dadosabertos.camara.leg.br/api/v2/votacoes?dataInicio={ano}-{mes_inicio}-01&dataFim={ano}-{mes_fim}-31&ordem=DESC&ordenarPor=dataHoraRegistro'

                while prox_url is not None:
                    #Buscar resultado parcial
                    resposta = get(url=prox_url)       
                    if resposta.status_code != 200: 
                        print(resposta.status_code)
                        return None

                    #Recuperar resultados parciais
                    resposta = resposta.json()
                    lista_info_parcial = resposta.get('dados')
                    for info_parcial in lista_info_parcial:
                        id_votacao = info_parcial.get('id') 
                        #print(f'Recuperando votacao id {id_votacao}')
                        data_votacao = datetime.strftime(datetime.strptime(info_parcial.get('data'), "%Y-%m-%d"), "%d/%m/%Y")
                        descricao_votacao = info_parcial.get('descricao').replace('\'','')
                        aprovada_votacao = True if info_parcial.get('aprovacao') == 1 else False
                        id_proposicao = int(id_votacao.split('-')[0])

                        #inserir banco dados
                        cursor.execute(f"INSERT OR IGNORE INTO votacoes (id, data, descricao, aprovada, id_proposicao) \
                                        VALUES ('{id_votacao}','{data_votacao}','{descricao_votacao}', {aprovada_votacao}, {id_proposicao})")
                        conexao_db.commit()

                    #Apontar para o próximo resultado parcial
                    prox_url = None
                    for link in resposta.get('links'):
                        if link.get('rel') == 'next':
                            prox_url = link.get('href')


    finally:
        conexao_db.commit()
        conexao_db.close()


def gerar_base_dados_despesas() -> None:
    #Calcular anos a serem consultados
    quantidade_anos = 34
    quantidade_total_despesas = 408
    ano_atual = datetime.utcnow().date().year
    anos = [str(ano_atual-delta) for delta in list(reversed(range(quantidade_anos)))]

    #Recuperar lista de ids dos deputados no banco de dados
    try:
        conexao_db = sqlite3.connect('/home/henrique/Downloads/banco_dados.db')
        cursor = conexao_db.cursor()

        #Recuperar lista de IDs
        cursor = cursor.execute("SELECT id FROM identificacao")
        ids = cursor.fetchall()

        for id in ids:
            id = id[0]
            #Verificar se já existe no banco despesas para o deputado
            cursor = cursor.execute(f'SELECT count(valor) FROM despesas WHERE id_deputado={id}')
            quantidade_despesas = cursor.fetchone()[0]

            #Gravar no banco se as despesas estão incompletas ou inexistentes para o deputado
            if quantidade_despesas < quantidade_total_despesas:
                print(f'Buscando despesas para o deputado {id} ...')
                for ano in anos:  

                    #Montar a primeira URL  
                    despesas_ano = list(zeros(12))
                    prox_url = f'https://dadosabertos.camara.leg.br/api/v2/deputados/{id}/despesas?ordem=ASC&ordenarPor=mes&ano={ano}&itens=100'

                    #Consultar dados na API da câmara dos deputados para um ano específico
                    while prox_url is not None:

                        #Buscar resultado parcial
                        resposta = get(url=prox_url)       
                        if resposta.status_code != 200: 
                            print(resposta.status_code)
                            return None

                        #Somar as despesas parciais
                        resposta = resposta.json()
                        lista_despesas_parcial = resposta.get('dados')
                        for despesa_parcial in lista_despesas_parcial:
                            if despesa_parcial['valorLiquido'] is None: despesa_parcial['valorLiquido'] = 0.0
                            despesas_ano[despesa_parcial['mes']-1] += despesa_parcial['valorLiquido']
                        
                        #Apontar para o próximo resultado parcial
                        prox_url = None
                        for link in resposta.get('links'):
                            if link.get('rel') == 'next':
                                prox_url = link.get('href')

                    #Montar a lista final com a data e a despesa
                    resultado = []
                    for idx, despesa in enumerate(despesas_ano):
                        data = date(year=int(ano), month=idx+1, day=1).strftime('%d/%m/%Y')
                        cursor.execute(f"INSERT OR IGNORE INTO despesas (id_deputado, data, valor) \
                                        VALUES ({id},'{data}',{despesa})")

                conexao_db.commit()

            else:
                print(f'Ignorando deputado id {id} ...')

    finally:
        conexao_db.commit()
        conexao_db.close()


def gerar_base_dados_deputados() -> None:

    try:
        conexao_db = sqlite3.connect('/home/henrique/Downloads/banco_dados.db')
        cursor = conexao_db.cursor()

        #Montar a primeira URL
        legislatura_atual = 56
        prox_url = f'https://dadosabertos.camara.leg.br/api/v2/deputados?dataInicio=1988-01-01&ordem=ASC&ordenarPor=nome'

        while prox_url is not None:
            #Buscar resultado parcial
            resposta = get(url=prox_url)       
            if resposta.status_code != 200: 
                print(resposta.status_code)
                return None

            #Recuperar as últimas informações de cada deputado
            resposta = resposta.json()
            lista_info_parcial = resposta.get('dados')
            for info_parcial in lista_info_parcial:
                #Verificar se o deputado já está cadastrado no banco
                id_provisorio = info_parcial.get('id')
                cursor = cursor.execute(f'SELECT * FROM identificacao WHERE id={id_provisorio}')
                informacoes_deputado = cursor.fetchone()
                if informacoes_deputado is None:

                    #Buscar últimas informações do deputado
                    resposta_info_deputado = get(url=info_parcial['uri'])
                    if resposta_info_deputado.status_code != 200: 
                        print(resposta.status_code)
                        return None
                    resposta_info_deputado = resposta_info_deputado.json()
                    print(f'Buscando informações para o deputado id {resposta_info_deputado.get("dados").get("id")} ...')

                    id_deputado = resposta_info_deputado.get('dados').get('id')
                    nome_deputado = resposta_info_deputado.get('dados').get('ultimoStatus').get('nome').replace('\'','')
                    partido_deputado = resposta_info_deputado.get('dados').get('ultimoStatus').get('siglaPartido').replace('\'','')
                    legislatura_atual = True if resposta_info_deputado.get('dados').get('ultimoStatus').get('idLegislatura') == legislatura_atual else False
                    url_foto = resposta_info_deputado.get('dados').get('ultimoStatus').get('urlFoto')

                    cursor.execute(f"INSERT OR IGNORE INTO identificacao (id, nome, partido, legislatura_atual, url_foto) \
                        VALUES ({id_deputado},'{nome_deputado}','{partido_deputado}', \
                                {legislatura_atual}, '{url_foto}')")

                    conexao_db.commit()

                else:
                    print(f'Deputado id {id_provisorio} já cadastrado')

            #Apontar para o próximo resultado parcial
            prox_url = None
            for link in resposta.get('links'):
                if link.get('rel') == 'next':
                    prox_url = link.get('href')

    finally:
        conexao_db.commit()
        conexao_db.close()


def gerar_base_dados_proposicoes() -> None:
    try:
        #Conectar banco de dados
        conexao_db = sqlite3.connect('/home/henrique/Downloads/banco_dados.db')
        cursor = conexao_db.cursor()

        #Recuperar lista de IDs
        cursor = cursor.execute("SELECT id_proposicao FROM votacoes")
        ids = cursor.fetchall()

        for id in ids:
            id = id[0]
            #Verificar se já existe no banco
            cursor = cursor.execute(f'SELECT id FROM proposicoes WHERE id={id}')
            if cursor.fetchone() is None:
                print(f'Buscando proposicao {id} ...')
                #Buscar resultado
                resposta = get(url=f'https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id}')       
                if resposta.status_code != 200 and resposta.status_code != 404: 
                    print(resposta.status_code)
                    return None
                elif resposta.status_code == 404:
                    print(resposta.json())
                    continue

                
                resposta = resposta.json()
                resposta = resposta.get('dados')
                numero_proposicao=resposta.get('numero')
                ano_proposicao=str(resposta.get('ano'))
                siglaTipo=resposta.get('siglaTipo').replace('\'','')
                ementa_proposicao=resposta.get('ementa').replace('\'','')
                cursor.execute(f"INSERT OR IGNORE INTO proposicoes (id, numero, ano, ementa, siglaTipo) \
                                VALUES ({id},{numero_proposicao},'{ano_proposicao}','{ementa_proposicao}', '{siglaTipo}')")
                conexao_db.commit()

            else:
                print(f'Ignorando proposicao id {id} ...')


    finally:
        conexao_db.commit()
        conexao_db.close()


def buscar_votos(ids) -> None:
    try:
        #Conectar banco de dados
        conexao_db = sqlite3.connect('/home/henrique/Downloads/banco_dados.db', timeout=15)
        cursor = conexao_db.cursor()
        soma_nao_encontrados = 0

        for idx, id in enumerate(ids):
            id = id[0]
            #Verificar se já existe no banco
            cursor = cursor.execute(f'SELECT id_votacao FROM votos WHERE id_votacao="{id}"')
            if cursor.fetchone() is None:
                
                print(f'[{idx}] Buscando votos da votacao {id} ...')

                #Montar a primeira URL
                prox_url = f'https://dadosabertos.camara.leg.br/api/v2/votacoes/{id}/votos'

                while prox_url is not None:
                    #Buscar resultado parcial
                    resposta = get(url=prox_url)       
                    if resposta.status_code != 200: 
                        print(resposta.status_code)
                        return None

                    #Recuperar as últimas informações de cada deputado
                    resposta = resposta.json()
                    lista_info_parcial = resposta.get('dados')
                    if len(lista_info_parcial) != 0:
                        for voto in lista_info_parcial:
                            tipo_voto = True if voto.get('tipoVoto') == 'Sim' else False
                            data_voto = datetime.strftime(datetime.strptime(voto.get('dataRegistroVoto'), "%Y-%m-%dT%H:%M:%S"), "%Y-%m-%d %H:%M:%S:%f")
                            id_deputado = voto.get('deputado_').get('id')

                            cursor.execute(f"INSERT OR IGNORE INTO votos (id_deputado, id_votacao, voto, data) \
                                VALUES ({id_deputado},'{id}', {tipo_voto}, '{data_voto}')")
                            conexao_db.commit()
                    else:
                        soma_nao_encontrados += 1
                        cursor.execute(f"INSERT OR IGNORE INTO votos (id_deputado, id_votacao, voto, data) \
                                VALUES (0,'{id}', 0, '0')")
                        conexao_db.commit()
                
                    #Apontar para o próximo resultado parcial
                    prox_url = None
                    for link in resposta.get('links'):
                        if link.get('rel') == 'next':
                            prox_url = link.get('href')
            else:
                print(f'id de votação {id} já existe no banco de dados')

    finally:
        print(f'Soma votações sem votos encontrados: {soma_nao_encontrados}')
        conexao_db.commit()
        conexao_db.close()


def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]


def gerar_lista_ids_votos() -> List[str]:

    try:
        conexao_db2 = sqlite3.connect('/home/henrique/Downloads/banco_dados.db')
        cursor2 = conexao_db2.cursor()
        #Recuperar lista de IDs
        #cursor2 = cursor2.execute("SELECT id FROM votacoes")
        #ids = cursor2.fetchall()

        sql = """ SELECT id 
                FROM votacoes
                WHERE DATE(substr(data,7,4)
                ||'-'
                ||substr(data,4,2)
                ||'-'
                ||substr(data,1,2)) 
                BETWEEN DATE('2015-01-01') AND DATE('2015-12-31') ORDER BY data ASC;"""
        cursor2 = cursor2.execute(sql)
        ids = cursor2.fetchall()
        
#        ids_1 = ids[:len(ids)//2]
#        ids_1_a = ids_1[:len(ids_1)//2]
#        ids_1_b = ids_1[len(ids_1)//2:]

#        ids_2 = ids[len(ids)//2:]
#        ids_2_a = ids_2[:len(ids_2)//2]
#        ids_2_b = ids_2[len(ids_2)//2:]

        res = split_list(ids, wanted_parts=1)


    finally:
        conexao_db2.close()

        return res
        #return ids_1_a, ids_1_b, ids_2_a, ids_2_b
        #return ids_1, ids_2


def gerar_base_dados_proposicoes_ajuste() -> None:
    try:
        #Conectar banco de dados
        conexao_db = sqlite3.connect('/home/henrique/Downloads/banco_dados.db')
        cursor = conexao_db.cursor()

        #Recuperar lista de IDs
        cursor = cursor.execute("SELECT id FROM proposicoes WHERE siglaTipo IS NULL")
        ids = cursor.fetchall()

        for idx, id in enumerate(ids):
            id = id[0]

            print(f'[{idx}] Ajustando proposicao {id} ...' )
            #Buscar resultado
            resposta = get(url=f'https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id}')       
            if resposta.status_code != 200 and resposta.status_code != 404: 
                print(resposta.status_code)
                return None
            elif resposta.status_code == 404:
                print(resposta.json())
                continue

            resposta = resposta.json()
            resposta = resposta.get('dados')
            siglaTipo=resposta.get('siglaTipo').replace('\'','')
            cursor.execute(f"UPDATE proposicoes SET siglaTipo='{siglaTipo}' WHERE id='{id}' and siglaTipo IS NULL")
            conexao_db.commit()
            

    finally:
        conexao_db.commit()
        conexao_db.close()


def gerar_base_dados_proposicoes_add_tema() -> None:
    try:
        #Conectar banco de dados
        conexao_db = sqlite3.connect('/home/henrique/Downloads/banco_dados.db')
        cursor = conexao_db.cursor()

        #Recuperar lista de IDs
        cursor = cursor.execute("SELECT id FROM proposicoes WHERE tema IS NULL")
        ids = cursor.fetchall()

        for idx, id in enumerate(ids):
            id = id[0]

            
            #Buscar resultado
            resposta = get(url=f'https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id}/temas')       
            if resposta.status_code != 200 and resposta.status_code != 404: 
                print(resposta.status_code)
                return None
            elif resposta.status_code == 404:
                print(resposta.json())
                continue

            resposta = resposta.json()
            resposta = resposta.get('dados')
            if len(resposta) != 0: 
                resposta = resposta[0]
                tema=resposta.get('tema').replace('\'','')
                print(f'[{idx}] Buscando tema para proposicao {id} ...')
            else:
                tema = 'Tema indefinido'
                print(f'[{idx}] Buscando tema para proposicao {id} ... [NAO ENCONTRADO]' )

            
            cursor.execute(f"UPDATE proposicoes SET tema='{tema}' WHERE id='{id}' and tema IS NULL")
            conexao_db.commit()
    except:
        print(resposta.get('dados'))
            

    finally:
        conexao_db.commit()
        conexao_db.close()


def gerar_base_dados_proposicoesDeputados() -> None:
    try:
        #Conectar banco de dados
        conexao_db = sqlite3.connect('/home/henrique/Downloads/banco_dados.db')
        cursor = conexao_db.cursor()

        #Recuperar lista de IDs
        cursor = cursor.execute("SELECT id FROM proposicoes")
        ids = cursor.fetchall()

        for idx, id in enumerate(ids):
            id = id[0]

            #Verificar se já existe no banco
            cursor = cursor.execute(f'SELECT id_proposicao FROM proposicoesDeputado WHERE id_proposicao={id}')
            if cursor.fetchone() is None:

                #Buscar resultado
                resposta = get(url=f'https://dadosabertos.camara.leg.br/api/v2/proposicoes/{id}/autores')       
                if resposta.status_code != 200 and resposta.status_code != 404: 
                    print(resposta.status_code)
                    return None
                elif resposta.status_code == 404:
                    print(resposta.json())
                    continue

                resposta = resposta.json()
                resposta = resposta.get('dados')
                for autor in resposta:
                    nome=autor.get('nome').replace('\'','')
                    tipo=autor.get('tipo').replace('\'','')
                    if tipo == 'Deputado':
                        cursor = cursor.execute(f"SELECT id FROM identificacao WHERE nome='{nome}'")
                        id_deputado = cursor.fetchone()
                        if id_deputado is None: id_deputado = 0
                        else: id_deputado = id_deputado[0]
                    else:
                        id_deputado = 0
                    print(f'[{idx}] Buscando autor para proposicao {id} ... ({nome},{tipo})' )
                    sql = f"INSERT OR IGNORE INTO proposicoesDeputado (id_deputado, id_proposicao) VALUES ({id_deputado},{id})"
                    cursor.execute(sql)
                    conexao_db.commit()
            
            else:
                print(f'Ignorando proposicao {id} ...')
                    
    #except:
        #print(sql)

    finally:
        conexao_db.commit()
        conexao_db.close()


def gerar_base_dados_deputados_add_foto() -> None:

    try:
        #Conectar banco de dados
        conexao_db = sqlite3.connect('/home/henrique/Downloads/banco_dados.db')
        cursor = conexao_db.cursor()

        #Recuperar url das fotos
        cursor = cursor.execute("SELECT id, url_foto FROM identificacao WHERE foto is NULL")
        fotos = cursor.fetchall()
        
        for idx, foto in enumerate(fotos):
            #Buscar resultado
            resposta = get(url=foto[1])
            if resposta.status_code != 200 and resposta.status_code != 404: 
                    print(resposta.status_code)
                    return None
            elif resposta.status_code == 404:
                    continue

            foto_bytes = resposta.content
            cursor.execute(f"UPDATE identificacao SET foto=? WHERE id=? and foto IS NULL", [sqlite3.Binary(foto_bytes), foto[0]])
            conexao_db.commit()
            print(f'[{idx}] Ajustando foto deputado {foto[0]} ...' )


    finally:
        conexao_db.commit()
        conexao_db.close()


def gerar_base_dados_deputados_add_foto_base64() -> None:
    try:
        #Conectar banco de dados
        conexao_db = sqlite3.connect('/home/henrique/Downloads/banco_dados.db')
        cursor = conexao_db.cursor()

        #Recuperar url das fotos
        cursor = cursor.execute("SELECT id, foto FROM identificacao")
        fotos = cursor.fetchall()
        
        for idx, foto in enumerate(fotos):
            #Converter fotos
            if foto[1]:
                base64Foto = encodebytes(foto[1]).decode('ascii')
            cursor.execute(f"UPDATE identificacao SET fotoBase64='{base64Foto}' WHERE id={foto[0]} and fotoBase64 IS NULL")
            conexao_db.commit()
            print(f'[{idx}] Ajustando foto deputado {foto[0]} ...' )

    finally:
        conexao_db.commit()
        conexao_db.close() 



if __name__ == '__main__':

    print('Atualizando base de dados de deputados ...')
    gerar_base_dados_deputados()

    print('Atualizando base de dados fotos de cada deputado...')
    gerar_base_dados_deputados_add_foto()
    gerar_base_dados_deputados_add_foto_base64()

    print('Atualizando base de dados de despesas ...')
    gerar_base_dados_despesas()

    print('Atualizando base de dados de votacoes ...')
    gerar_base_dados_votacoes()

    print('Atualizando base de dados votos de cada deputado ...')
    buscar_votos(gerar_lista_ids_votos())

    print('Atualizando base de dados de proposicoes ...')
    gerar_base_dados_proposicoes()

    print('Atualizando temas das proposicoes ...')
    gerar_base_dados_proposicoes_add_tema()

    print('Atualizando base de dados proposicoes de cada deputado ...')
    gerar_base_dados_proposicoesDeputados()

    


