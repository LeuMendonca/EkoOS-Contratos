from django.db import models

# Create your models here.

class EkContrato(models.Model):
    seq_contrato = models.AutoField(primary_key=True)
    num_empresa = models.IntegerField(blank=True, null=True)
    #cod_pessoa = models.ForeignKey('EkPessoa', models.DO_NOTHING,db_column='cod_pessoa')
    cod_pessoa = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)
    numero_contrato = models.IntegerField(blank=True, null=True)
    vl_contrato = models.FloatField(blank=True, null=True)
    dt_inicio_contrato = models.DateTimeField(blank=True, null=True)
    dt_fim_contrato = models.DateTimeField(blank=True, null=True)
    dt_cadastro = models.DateTimeField(auto_now_add=True)
    dt_contrato = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, blank=True, null=True,default='A')
    combustivel = models.CharField(max_length=1,blank=True,null=True)
    qtd_combustivel = models.FloatField(blank=True, null=True)
    cabos = models.CharField(max_length=1, blank=True, null=True)
    chave_transf_manual = models.CharField(max_length=1, blank=True, null=True)
    chave_transf_auto = models.CharField(max_length=1, blank=True, null=True)
    transporte = models.CharField(max_length=1, blank=True, null=True)
    instalacao = models.CharField(max_length=1, blank=True, null=True)
    manutencao = models.CharField(max_length=1, blank=True, null=True)
    distancia_transporte = models.FloatField(blank=True, null=True)
    franquia = models.IntegerField(blank=True, null=True)
    carga_horaria = models.IntegerField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'ek_contrato'
        


class EkPessoa(models.Model):
    nome = models.CharField(max_length=100, blank=True, null=True)
    cod_pessoa = models.IntegerField(primary_key=True)    
    cnpj = models.CharField(max_length=14, blank=True, null=True)
    cpf = models.CharField(max_length=11, blank=True, null=True)
    status = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return  self.nome
    class Meta:
        managed = False
        db_table = 'ek_pessoa'



class EkProduto(models.Model):
    cod_produto = models.DecimalField(primary_key=True, max_digits=10, decimal_places=0)
    desc_produto = models.CharField(max_length=100, blank=True, null=True)
    tipo_item = models.DecimalField(max_digits=2, decimal_places=0, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ek_produto'


class EkContratoDetalhe(models.Model):
    seq_contrato_detalhe = models.AutoField(primary_key=True)
    seq_contrato = models.IntegerField(db_column='seq_contrato', blank=True, null=True)
    cod_produto = models.IntegerField(blank=True, null=True)
    desc_item_contrato = models.CharField(max_length=200,blank=True, null=True)
    vl_item_contrato = models.FloatField(blank=True, null=True)
    quantidade = models.IntegerField(blank=True, null=True)
    unid_medida = models.CharField(blank=False,null=False,max_length = 20,db_column='unid_medida')



    class Meta:
        managed = False
        db_table = 'ek_contrato_detalhe'