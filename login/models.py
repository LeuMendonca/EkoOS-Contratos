from django.db import models

# Create your models here.
class Empresa(models.Model):
    
    num_empresa = models.AutoField(primary_key=True,db_column='num_empresa')
    nome_empresa = models.CharField(max_length=50,db_column='nome_empresa')

    def __str__(self):
        return f'{self.num_empresa} - ' + f'{self.nome_empresa}'
    
    
    class Meta:
        managed = False
        db_table = 'ek_empresa'
    
    
class Login(models.Model):
    id_usuario = models.AutoField(primary_key=True,db_column='cod_usuario')
    login = models.CharField(max_length=50,blank=False,null=False,db_column='nome_usuario')
    password = models.CharField(max_length=50,blank=False,null=False,db_column='senha') 
    
    def __str__(self):
        if self.login == '1':
            self.login = 'EkoOS'
            return self.login
        else:
            return self.login
        
    class Meta:
        managed = False
        db_table = 'ek_usuario'


class EkUsuarioEmpresa(models.Model):
    cod_usuario = models.IntegerField(db_column='cod_usuario')
    cod_empresa = models.IntegerField(db_column='cod_empresa', primary_key=True)
    
    def __str__(self):
        return f'Usuario: {self.cod_usuario} - Empresa: {self.cod_empresa}'
    class Meta:
        managed = False
        db_table = 'ek_usuario_empresa'
        unique_together = (('cod_empresa', 'cod_usuario'),)