from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import EkContrato,EkPessoa,EkProduto,EkContratoDetalhe
from django.core.paginator import Paginator
from .forms import FormularioContratos
from django.db.models import Q
from datetime import datetime
from django.db import connection
from funcoes.gera_contrato import *
from django.conf import settings
import os


# Create your views here.

def index(request):

    usuario = request.session.get('cod_usuario')
    
    if usuario:
        empresa = request.session['num_empresa']
        models = EkContrato.objects.all().filter(num_empresa=empresa).filter(status='A').order_by('-seq_contrato')
        pessoa = EkPessoa.objects.all()

        # Responsavel pela barra de pesquisa. Atualmente busca pelo codigo do cliente.
        buscar = request.GET.get("q")
        status =  request.GET.get('status')
        if buscar:
            filtro = request.GET.get('filtro')
            

            if filtro == 'pessoa':
                nome_pessoa =  EkPessoa.objects.filter(nome__icontains = buscar)
                models = EkContrato.objects.filter(cod_pessoa__in = nome_pessoa).filter(num_empresa = empresa).order_by('-seq_contrato')
            if filtro == 'contrato':
                try:
                    models = EkContrato.objects.filter(Q(seq_contrato = buscar)).filter(num_empresa = empresa).order_by('-seq_contrato')
                except:
                    return redirect('/home/?status=5')
        # models = EkContrato.objects.filter(Q(cod_pessoa = buscar))

        # Paginação de 10 em 10 contratos na aba home
        paginator = Paginator(models, 10) 

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        
        return render(request,'contratos/index.html',{'page_obj':page_obj,'pessoa':pessoa,'status':status})
    else:
        return redirect('/login/?status=2')

def cadastro_contrato(request):
    usuario = request.session.get('cod_usuario')
    
    if usuario:
        if request.method == 'GET':    
            form = FormularioContratos()
            models_pessoa = EkPessoa.objects.filter(status='L').order_by('nome')
            models_produto = EkProduto.objects.filter(tipo_item = 9).exclude(cod_produto = 321).order_by('desc_produto')
            return render(request,'contratos/cadastro_contrato.html',{'forms':form,'ek_pessoa':models_pessoa,'ek_produto':models_produto})
        
        elif request.method == 'POST':   
            cursor = connection.cursor()
            
            # Dados capa do contrato
            cod_pessoa = request.POST.get('select')
            numero_contrato = request.POST.get('numero_contrato')
            num_empresa = request.session['num_empresa']
            dt_inicio_contrato = request.POST.get('dt_inicio_contrato')
            dt_fim_contrato = request.POST.get('dt_fim_contrato')
            vl_contrato = request.POST.getlist('vl_total')
            franquia = request.POST.get('select-franquia')
            carga_horaria = request.POST.get('horas-select')
            
            # Diferença de dias ( data final - data inicial )
            d2 = datetime.datetime.strptime(dt_fim_contrato, '%Y-%m-%d')
            d1 = datetime.datetime.strptime(dt_inicio_contrato, '%Y-%m-%d')
            diferenca_datas = abs((d2 - d1).days)
            
            # Variaveis do contrato
            combustivel = request.POST.get('combustivel')
            cabos = request.POST.get('cabos')
            chave_transf_manual = request.POST.get('chave_transf_manual')
            chave_transf_auto = request.POST.get('chave_transf_auto')
            transporte = request.POST.get('transporte')
            instalacao = request.POST.get('instalacao')
            manutencao = request.POST.get('manutencao')
            
            
            
            if combustivel == 'S':
                qtd_combustivel = request.POST.get('qtd_combustivel')
            else:
                qtd_combustivel = 0
            
            if transporte == 'S':
                distancia_transporte = request.POST.get('qtd_transporte')
            else:
                distancia_transporte = 0
            
            vl_contrato = sum(list(map(lambda x : round(float(x),2) , vl_contrato))) # Soma dos itens gerado a partir da função javascript atualiza_preco()
            
            cursor.execute('select case when max(seq_contrato) is null then 0 else max(seq_contrato)end  from ek_contrato')
            max_seq_contrato = int(str(cursor.fetchall()[0][0])) + 1
            
            # Capa do contrato 
            dados_contrato = EkContrato(
                seq_contrato = max_seq_contrato,
                cod_pessoa=cod_pessoa,
                numero_contrato=numero_contrato,
                num_empresa=num_empresa,
                dt_inicio_contrato = dt_inicio_contrato,
                dt_fim_contrato = dt_fim_contrato,
                vl_contrato=vl_contrato, # quantidade de produtos * preco unitario * diferenca de datas final e inicial,
                combustivel = combustivel,
                qtd_combustivel = qtd_combustivel,
                cabos = cabos,
                chave_transf_manual = chave_transf_manual,
                chave_transf_auto = chave_transf_auto,
                transporte = transporte,
                instalacao = instalacao,
                manutencao = manutencao,
                distancia_transporte = distancia_transporte,
                franquia = int(franquia),
                carga_horaria = int(carga_horaria)
                )
            dados_contrato.save() # Insert no banco de dados

            # Dados itens do contrato
            
            # Lista de valores dos campos name
            produto = request.POST.getlist("select-produto")
            valor = request.POST.getlist("campo_valor")    
            quantidade = request.POST.getlist("quantidade")
            
            
            
            for cod_produto,vl_item,quantia  in zip(produto,valor,quantidade): # quantidade,quantia
                    descricao_produto = EkProduto.objects.filter(cod_produto=cod_produto).values()
                    desc_produto = list(descricao_produto)[0]['desc_produto']
                    
                    cursor.execute('select case when max(seq_contrato_detalhe) is null then 0 else  max(seq_contrato_detalhe) end from ek_contrato_detalhe')
                    max_seq_item_detalhe = int(str(cursor.fetchall()[0][0])) + 1 
                    
                    itens = EkContratoDetalhe(seq_contrato_detalhe = max_seq_item_detalhe,
                                            cod_produto=cod_produto,
                                            vl_item_contrato=vl_item,
                                            desc_item_contrato = desc_produto,
                                            seq_contrato=dados_contrato.seq_contrato,
                                            quantidade=quantia)
                    itens.save()
            
            cursor.execute(
                '''select max(seq_contrato) from ek_contrato'''
            )
            seq_contrato = cursor.fetchall()[0][0]
            
            # Gerando contrato
            num_empresa = request.session['num_empresa']
            cursor = connection.cursor()
            
            cursor.execute(f'''
                                select seq_pedido_cli 
                                from ek_pedido_cli 
                                where numero_contrato = {seq_contrato}
                            ''')
            
            seq_pedido = cursor.fetchall()
            if len(seq_pedido) == 0:
                print('passou aqui')
                cursor.execute(
                f'''
                    select * from ek_contrato 
                    where seq_contrato = {seq_contrato}
                '''
                )
                
                contrato = cursor.fetchall()[0]

                cursor.execute(f'''select * from 
                                   ek_contrato_detalhe 
                                   where seq_contrato = {seq_contrato}
                               ''')

                resultado = cursor.fetchall()
                valor_itens = []

                for x in resultado:
                    valor_itens.append(x[4] * x[5])
                    
                # Gerando o pedido
                cursor.execute(
                    f'''
                        insert into ek_pedido_Cli(
                            dt_pedido,
                            flag_status,
                            vl_total_pedido,
                            cod_pessoa,
                            tipo_pedido,
                            dt_cadastro,
                            num_empresa,
                            obs_pedido,
                            numero_contrato
                        )values(
                            '{datetime.datetime.now()}',
                            'F',
                            {contrato[4]},
                            {contrato[2]},
                            'P',
                            '{datetime.datetime.now()}',
                            {request.session['num_empresa']},
                            'Pedido gerado através do contrato',
                            {seq_contrato}
                        )
                    '''
                )
                
                # Gerando os itens do pedido
                cursor.execute(f'''select * from 
                                ek_contrato_detalhe 
                                where seq_contrato = {seq_contrato}''')
                resultado = cursor.fetchall()
            

                cursor.execute(f'''
                                    select dt_inicio_contrato , dt_fim_contrato 
                                    from ek_contrato 
                                    where seq_contrato = {seq_contrato}
                                ''')
                data = cursor.fetchall()[0]
                dias_contrato = abs((data[1] - data[0]).days)
                
                start = 1
                cursor.execute(f'select max(seq_item_pedido) from ek_item_pedido_cli')
                max_seq_item_pedido = cursor.fetchall()[0][0]
                
                cursor.execute(f'''select seq_pedido_cli 
                               from ek_pedido_cli 
                               where numero_contrato = {seq_contrato}''')
                seq_pedido_cli = cursor.fetchall()[0][0]


                for res in resultado:
                    max_seq_item_pedido += 1
                    cursor.execute(f'''select desc_produto 
                                       from ek_produto 
                                       where cod_produto = {res[2]}''')
                    desc = cursor.fetchall()[0]
                    
                    cursor.execute(f'''insert into ek_item_pedido_cli(
                                    seq_pedido_cli,
                                    cod_item,
                                    qtd_pedido,
                                    qtd_atendido,
                                    vl_unitario,
                                    vl_total_item,
                                    dt_cadastro,
                                    seq_item_pedido,
                                    status_item,
                                    sequencia_item,
                                    desc_item
                                )values(
                                    {seq_pedido_cli},
                                    {res[2]},
                                    1,
                                    1,
                                   {res[4] * res[5]},
                                    {res[4] * res[5]},
                                    '{datetime.datetime.now()}',
                                    {max_seq_item_pedido},
                                    'F',
                                    {start},
                                    'Locacao produto {res[2]} - {desc[0]} - {dias_contrato} dias - Valor Total: {dias_contrato * res[4]}'
                                )
                                ''')
                    start += 1                
            return redirect('/home/?status=3') # Stauts=3 é o parametro para exibição da mensagem
    else:
        return redirect('/login/?status=2')
        
def delete(request,seq_contrato):
    usuario = request.session.get('cod_usuario')
    
    if usuario:
        cursor = connection.cursor()
        # Delete altera o status do contrato para E ( Excluido ) para caso precise voltar no banco de dados
        cursor.execute(
            f'''
                select
                (case when seq_nota is null then 0
                else 1
                end) as "seq_nota",
                (case when seq_nota_servico is null then 0
                else 1
                end) as "seq_nota_servico" 
                from ek_contrato where seq_contrato = {seq_contrato}
            '''
        )
        atributos = cursor.fetchall()[0]

        if request.POST:
            if atributos[0] == 0 and atributos[1] == 0:
                cursor.execute(
                    f'''
                        update ek_contrato 
                        set status = 'E' 
                        where seq_contrato = {seq_contrato}
                    '''
                )
                
                cursor.execute(
                    f"""
                        update ek_pedido_cli 
                        set flag_status = 'C' , 
                        obs_pedido = 'Pedido cancelado através do EkoOS Contrato {seq_contrato}' 
                        where numero_contrato = {seq_contrato}
                    """
                )
                
                cursor.execute(
                    f"""
                        update ek_item_pedido_cli set 
                        status_item = 'C' 
                        where seq_pedido_cli in 
                        (select seq_pedido_cli from ek_pedido_cli where numero_contrato = {seq_contrato})
                    """
                )
                
                connection.commit()
                return redirect('/home/?status=2')
            else:
                return redirect('/home/?status=13')
        return render(request,'contratos/delete.html',{'seq_contrato':seq_contrato})
    else:
        return redirect('/login/?status=2')


def update(request,seq_contrato):
    usuario = request.session.get('cod_usuario')
    
    if usuario:
        if request.method == 'GET':
            models_pessoa = EkPessoa.objects.filter(status='L').order_by('nome')
            models_produto = EkProduto.objects.filter(tipo_item = 9).exclude(cod_produto = 321).order_by('desc_produto')

            models_contrato = EkContrato.objects.get(seq_contrato=seq_contrato)
            form_contrato = FormularioContratos(request.POST or None,instance=models_contrato)
            request.session['franquia'] = models_contrato.franquia
            request.session['horas'] = models_contrato.carga_horaria
            cursor = connection.cursor()
            cursor.execute(f'''
            select * from ek_contrato_detalhe where seq_contrato = {seq_contrato}
            ''')
            resultado = cursor.fetchall()

            diferenca_datas = str(models_contrato.dt_fim_contrato - models_contrato.dt_inicio_contrato).split()[0]
            
            formulario = []
            # No for abaixo eu crio uma especie de JSON formulario = [{ }] e envio para o template , no template eu faço o for nas tags html 
            # preenchendo o value 
            #        ↓↓↓↓↓↓
            
            for x in resultado:
                formulario.append({
                'seq_contrato_detalhe' : x[0],
                'seq_contrato' : x[1],
                'cod_produto' : x[2],
                'descricao' : x[3],
                'vl_item_contrato' : x[4],
                'quantidade':x[5],
                'vl_total_item' : int(x[4]) * int(x[5])
                })
            request.session['datai'] = str(models_contrato.dt_inicio_contrato)[:10]
            request.session['dataf'] = str(models_contrato.dt_fim_contrato)[:10]

            dados = {'form': formulario,'pessoas':models_pessoa,'produto':models_produto,'form_contrato':form_contrato,'models_contrato':models_contrato}
            return render(request,'contratos/update.html',dados)
        
        if request.method == 'POST':
            cursor = connection.cursor()

            # ↓ Coleta manual de dados dos campos name nas tags HTML ↓
            cod_pessoa = request.POST.get('select')
            numero_contrato = request.POST.get('numero_contrato')
            vl_contrato = request.POST.getlist('vl_total')
            vl_contrato = sum(list(map(lambda x : round(float(x),2) , vl_contrato))) # Duas casas decimais no valor do contrato
            num_empresa = request.session['num_empresa']
            combustivel = request.POST.get('combustivel')
            cabos = request.POST.get('cabos')
            chave_transf_manual = request.POST.get('chave_transf_manual')
            chave_transf_auto = request.POST.get('chave_transf_auto')
            transporte = request.POST.get('transporte')
            instalacao = request.POST.get('instalacao')
            manutencao = request.POST.get('manutencao')
            franquia = request.POST.get('select-franquia')
            carga_horaria = request.POST.get('horas-select')
            
            
            if combustivel == 'S':
                qtd_combustivel = request.POST.get('qtd_combustivel')
            else:
                qtd_combustivel = 0
            
            if transporte == 'S':
                distancia_transporte = request.POST.get('qtd_transporte')
            else:
                distancia_transporte = 0
            
            # ↓ Calculo para encontrar a diferença de datas ↓
            data_inicial = request.POST.get('dt_inicio_contrato')
            data_final = request.POST.get('dt_fim_contrato')
            d2 = datetime.datetime.strptime(data_inicial, '%Y-%m-%d')
            d1 = datetime.datetime.strptime(data_final, '%Y-%m-%d')

            resultado = abs((d2 - d1).days)
            
            # ↓ Foi usado este modo de coletar a data pois quando uso o .save para atualizar a capa eu perco a data de cadastro ↓
            cursor.execute(f'''select dt_cadastro 
                           from ek_contrato 
                           where seq_contrato = {seq_contrato}''')
            dt_cadastro = cursor.fetchall()[0][0]
            dt_cadastro_convertida = str(dt_cadastro)
            
            # ↓ Capa do contrato a ser atualizado ↓
            contrato = EkContrato(
                        seq_contrato=seq_contrato,
                        cod_pessoa = cod_pessoa,
                        numero_contrato = numero_contrato,
                        num_empresa=num_empresa,
                        vl_contrato = vl_contrato,
                        dt_inicio_contrato = data_inicial,
                        dt_fim_contrato = data_final,
                        status='A',
                        combustivel = combustivel,
                        qtd_combustivel = qtd_combustivel,
                        cabos = cabos,
                        chave_transf_manual = chave_transf_manual,
                        chave_transf_auto = chave_transf_auto,
                        transporte = transporte,
                        instalacao = instalacao,
                        manutencao = manutencao,
                        distancia_transporte = distancia_transporte,
                        franquia = int(franquia),
                        carga_horaria = int(carga_horaria)
            )
            
            contrato.save() # Insert da capa do contrato no banco de dados

                # ↓ Inserindo a data de cadastro de volta no banco de dados ↓
            cursor.execute(f'''
                                update ek_contrato 
                                set dt_cadastro = '{dt_cadastro_convertida}' 
                                where seq_contrato = {seq_contrato}
                        ''')
            
            
            cursor.execute(f'''update ek_pedido_cli set 
                                vl_total_pedido = {vl_contrato},
                                cod_pessoa = {cod_pessoa} 
                                where numero_contrato = {seq_contrato}
                            ''')            
            # ↓ Contrato Detalhe ( Produtos )↓
            
            produto = request.POST.getlist('select_produtos')
            valores = request.POST.getlist('campo_valor')
            quantidade = request.POST.getlist('quantidade')
            cursor.execute(
                            f'''
                                select min(seq_contrato_detalhe) 
                                from ek_contrato_detalhe 
                                where seq_contrato = {seq_contrato}
                            '''
                            )
            sequencial_item = cursor.fetchall()[0][0]
            cursor.execute(
                f'''
                    select min(seq_item_pedido) 
                    from ek_item_pedido_cli 
                    where seq_pedido_cli in 
                    (select seq_pedido_cli from ek_pedido_cli where numero_contrato = {seq_contrato})
                '''
            )
            sequencial_item_pedido = cursor.fetchall()[0][0]
            # ↓ Primeiro sequencial do contrato , após isso eu vou somando +1 enquanto tiver dados a serem atualizados ↓ 
            
            
            for produto , valor,quantia in zip(produto,valores,quantidade):
        
                descricao = EkProduto.objects.get(cod_produto = produto ).desc_produto
                
                cursor.execute(
                    f'''
                        update ek_contrato_detalhe 
                        set cod_produto = {produto} , 
                        vl_item_contrato = {valor} , 
                        desc_item_contrato = '{descricao}' , 
                        quantidade = {quantia} 
                        where seq_contrato_detalhe = {sequencial_item}
                    '''
                )
                
                cursor.execute(
                    f'''
                        update ek_item_pedido_cli set
                                    cod_item = {produto},
                                    qtd_pedido = {quantia},
                                    qtd_atendido = {quantia},
                                    vl_unitario = {valor},
                                    vl_total_item = {float(quantia) * float(valor)},
                                    desc_item = '{descricao}'
                                    where seq_item_pedido = {sequencial_item_pedido}
                                    and seq_pedido_cli in 
                                    (select seq_pedido_cli from ek_pedido_cli where numero_contrato = {seq_contrato})
                    '''
                )
                
                sequencial_item_pedido += 1
                sequencial_item = sequencial_item + 1 # Soma do item comentada acima 
                connection.commit() # Execução dos comandos update
            
            return redirect('/home/?status=4')
    else:
        return redirect('/login/?status=2')    


def gerador_contrato(request,seq_contrato):
    
    caminho ="C:/ekoos_contrato/midia/Contrato-"+ str(seq_contrato) + '.pdf'
    caminho = os.path.join(settings.MEDIA_ROOT,caminho)

    gera_contrato(caminho,seq_contrato)
    
    
    if os.path.exists(caminho):
        with open(caminho,'rb') as fh:
            response = HttpResponse(fh.read(),content_type="application/pdf")
            response['Content-Disposition'] = 'inline;filename=' + os.path.basename(caminho)
        os.remove(caminho)
        return response
    else:
        return redirect('/home/?status=6')
    
    
    #return redirect(f'/midia/Contrato-{seq_contrato}.pdf')

def gera_nota_servico(request,seq_contrato):
    usuario = request.session.get('cod_usuario')
    
    if usuario:
        if request.method == 'POST':
        
            cursor = connection.cursor()
            
            cursor.execute(f'''select count(*) 
                           from ek_pedido_cli 
                           where numero_contrato = {seq_contrato}''')
            confere_pedido = cursor.fetchall()[0][0]
        
            if confere_pedido == 0:
                return redirect('/home/?status=8')
            else:
                
                cursor = connection.cursor()
                
                cursor.execute(
                    f"""select 
                    (case when seq_nota_servico is null then 0
                    else seq_nota_servico
                    end) as "seq_nota_servico"
                    from ek_contrato where seq_contrato = {seq_contrato}"""
                )
                
                seq_nota_servico = cursor.fetchall()[0][0]

                if seq_nota_servico == 0:
                    cursor.execute(f'''select seq_pedido_cli 
                                   from ek_pedido_cli 
                                   where numero_contrato = {seq_contrato}''')
                    pedido = cursor.fetchall()[0][0]
                    
                    
                    cursor = connection.cursor()
                    cursor.execute(f'''select * from gera_nota_fiscal({pedido})''')
                    seq_nota_servico = cursor.fetchall()[0][0]
                    
                    cursor.execute(
                        f'''
                            update ek_contrato 
                            set seq_nota_servico = {seq_nota_servico} 
                            where seq_contrato = {seq_contrato}
                        '''
                    )
                    
                    cursor.execute(f'''update ek_contrato set status = 'F' where seq_contrato = {seq_contrato}''')

                    return redirect('/home/?status=10')
                else:
                    return redirect(f'/home/?status=11')
                
            
        return render(request,"contratos/gera_nota_serv.html",{'seq_contrato':seq_contrato})
    return redirect('/login/?status=2')



def gera_nota_remessa(request,seq_contrato):
    usuario = request.session.get('cod_usuario')
    
    if usuario:
        if request.method == 'GET':
            return render(request,"contratos/gera_nota_remessa.html",{'seq_contrato':seq_contrato})
        else:
            cursor = connection.cursor()
            cursor.execute(
                f'''
                    select (case when seq_nota is null then 0
                    else seq_nota
                    end) as "seq_nota"
                    from ek_contrato 
                    where seq_contrato = {seq_contrato}
                '''
            )
            seq_nota_remessa = cursor.fetchall()[0][0]
            if seq_nota_remessa == 0:

                cursor.execute(
                        f'''
                        select cod_pessoa,vl_total_pedido 
                        from ek_pedido_cli 
                        where numero_contrato = {seq_contrato}
                        '''
                        )
                pedido = cursor.fetchall()[0]
                
                cursor.execute(
                        f'''update ek_configuracao 
                        set num_doc_controle = num_doc_controle + 1  
                        where num_empresa = {request.session["num_empresa"]} 
                        returning num_doc_controle'''
                        )
                num_doc_controle = cursor.fetchall()[0][0]
                    
                cursor.execute(
                f'''
                select seq_pessoa_inscricao_estadual 
                from ek_pessoa_incricao_estadual 
                where cod_pessoa = {pedido[0]} 
                and insc_fiscal = 'S' 
                limit 1
                '''
                )
                seq_pessoa_inscricao_estadual = cursor.fetchall()[0][0]
                
                cursor.execute(
                    f'''
                        select estado 
                        from ek_pessoa 
                        where cod_pessoa = {pedido[0]}
                    '''
                )
                estado_cliente = cursor.fetchall()[0][0]
                cursor.execute(
                    f'''select estado from
                        ek_empresa 
                        where num_empresa = {request.session["num_empresa"]}'''
                )
                estado_empresa = cursor.fetchall()[0][0]
                cfop = 0
                
                if int(estado_empresa) == int(estado_cliente):
                    cfop = 5949
                else:
                    cfop = 6949
                # AJUSTAR QUANTIDADE E VALOR DO ITEM
                
                cursor.execute(f'''select serie_nfe 
                               from ek_configuracao 
                               where num_empresa = {request.session["num_empresa"]}''')
                serie = cursor.fetchall()[0][0]
                
                cursor.execute(
                    f'''
                    insert into ek_nota(
                        num_empresa,
                        ind_oper,   
                        ind_emit,
                        cod_part,
                        cod_mod,
                        ser,
                        num_doc,
                        dt_doc,
                        dt_e_s,
                        vl_doc,
                        vl_merc,
                        cod_mov,
                        dt_cadastro,
                        cfop,
                        cod_sit,
                        desc_complementar,
                        seq_pessoa_inscricao_estadual
                    )values(
                        {request.session['num_empresa']},
                        '1',
                        '0',
                        {pedido[0]},
                        '55',
                        '{serie}',
                        {num_doc_controle},
                        '{datetime.datetime.now()}',
                        '{datetime.datetime.now()}',
                        {pedido[1]},
                        {pedido[1]},
                        '2',
                        '{datetime.datetime.now()}',
                        '{cfop}',
                        '00',
                        'Nota fiscal de remessa locacao referente ao contrato {seq_contrato}.',
                        {seq_pessoa_inscricao_estadual}
                        ) returning seq_nota
                        '''
                )

                seq_nota = cursor.fetchall()[0][0]

                cursor.execute(
                    f'''
                        select * 
                        from ek_item_pedido_cli 
                        where seq_pedido_cli in 
                        (select seq_pedido_cli from ek_pedido_cli where numero_contrato = {seq_contrato})
                    '''
                )

                ek_item_pedido_cli = cursor.fetchall()
                
                
                seq_item = 0
                for x in ek_item_pedido_cli:
                    cursor.execute(
                    f'''
                    select unid_venda , desc_produto 
                    from ek_produto 
                    where cod_produto = {x[1]}
                    '''
                    )
                    produto = cursor.fetchall()[0]
                
                    
                    seq_item = seq_item + 1
                    cursor.execute(f'''
                        insert into ek_item_nota (
                        seq_nota,
                        seq_item, 
                        cod_item,
                        quantidade,
                        unidade,
                        vl_item,
                        cst_icms,
                        cfop,
                        dt_cadastro,
                        vl_total_item,
                        desc_item_nota
                        )values(
                            {seq_nota},
                            {seq_item},
                            127,
                            {x[2]},
                            '{produto[0]}',
                            {x[10]},
                            '090',
                            '{cfop}',
                            '{datetime.datetime.now()}',
                            {x[11]},
                            '{produto[1]}'
                        )
                    ''')

                        
                    
                    cursor.execute(f'''
                                    update ek_item_pedido_cli 
                                    set seq_nota = {seq_nota} 
                                    where seq_pedido_cli in 
                                    (select seq_pedido_cli from ek_pedido_cli where numero_contrato = {seq_contrato})
                                ''')
                    
                
                cursor.execute(f'''update ek_contrato 
                               set seq_nota = {seq_nota} 
                               where seq_contrato = {seq_contrato}''')
                
                connection.commit()
                return redirect('/home/?status=9')
            else:
                return redirect('/home/status=12')
    else:
        return redirect('/login/?status=2')