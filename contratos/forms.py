from django import forms
from .models import EkContrato,EkContratoDetalhe


class FormularioContratos(forms.ModelForm):
    class Meta:
        model = EkContrato
        fields = ['cod_pessoa','numero_contrato','dt_inicio_contrato','dt_fim_contrato','vl_contrato','combustivel','qtd_combustivel','cabos','chave_transf_manual','chave_transf_auto','transporte','instalacao','manutencao','distancia_transporte','franquia','carga_horaria']
        
        widgets = {
            'cod_pessoa' : forms.TextInput(
                attrs={
                    'placeholder':'Codigo do cliente',
                    'id':'cod-pessoa',
                    'class':"form-control w-25",
                    'name':'cod_pessoa'
                }
            ),
            'numero_contrato' : forms.TextInput(
                attrs={
                    'placeholder':'Numero do Contrato',
                    'id':'numero_contrato',
                    'class':"form-control w-25",
                    'name':'numero_contrato'
                    
                    }
                ),
            'dt_inicio_contrato': forms.TextInput(
                attrs={
                    'type':'date',
                    'id':'data_inicio',
                    'class':'form-control',
                    'name':'dt_inicio_contrato','placeholder':'Data Inicial ',
                    'onchange' :'atualizar()',
                    'style':'width: 227px'
                }
            ),
            'dt_fim_contrato': forms.TextInput(
                attrs={
                    'type':'date',
                    'id':'data_fim',
                    'class':'form-control ms-3 mt-1',
                    'name':'dt_fim_contrato','placeholder':'Data Final',
                    'style':'width: 228px',
                    'onchange':'atualiza_preco()'
                }
            ),
            'vl_contrato': forms.TextInput(attrs={
                'placeholder':'Valor do contrato',
                'class':"form-control ms-3",
                'name':'valor_contrato',
                'disabled' : 'true',
                'id':'valor_contrato',
                'type':'text',
                'style':'width:150px'
            })
        }
        
class FormularioItensContrato(forms.ModelForm):
    class Meta:
        model = EkContratoDetalhe
        fields = ['seq_contrato_detalhe' ,'seq_contrato' ,'cod_produto' ,'desc_item_contrato' ,'vl_item_contrato' ]
        
        

        