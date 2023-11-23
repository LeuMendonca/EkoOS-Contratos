let id_dinamico = 1
function adicionar_item() {

  let placeholder_valor_unitario = ''
  let placeholder_quantidade = ''
  
  let franquia = document.getElementById('select-franquia').value
  switch (franquia){
    case '1':
      placeholder_quantidade = 'Dias'
      placeholder_valor_unitario = 'Valor diário'
      break
    case '7':
      placeholder_quantidade = 'Semanas'
      placeholder_valor_unitario = 'Valor semanal'
      break
    case '15':
      placeholder_quantidade = 'Quizenas'
      placeholder_valor_unitario = 'Valor quinzenal'
      break
    case '30':
      placeholder_quantidade = 'Meses'
      placeholder_valor_unitario = 'Valor mensal'
      break
    default:
      pass
  }
  
  id_dinamico += 1

  let tabela_produtos = window.document.querySelector('select#select-produto')

  let formulario = document.querySelector('form.form-contrato')

  let div_row = document.createElement('div')
  div_row.setAttribute('class','row')
  div_row.setAttribute('id',`div-${id_dinamico}`)
  div_row.setAttribute('name',`div_area_produtos`)
 

  
  let div_select = document.createElement('div')
  div_select.setAttribute('class','col-sm-auto')
  let select = document.createElement('select')
  select.setAttribute('name','select-produto')
  select.setAttribute(`id`,`select-produto-${id_dinamico}`)
  select.setAttribute('class','form-select')
  select.style.minWidth = '450px'
  select.style.height = '35px'

 

  for (c = 0 ; c < tabela_produtos.length ; c++ ){
    let option = document.createElement('option')
    option.text = tabela_produtos.options[c].text
    option.value = tabela_produtos.options[c].value
    select.appendChild(option)
    
  }
  
  div_select.append(select)

  //Produto
  let div_valor_produto = document.createElement('div')
  div_valor_produto.setAttribute('class','col-auto')
  let input_valor = document.createElement('input')
  input_valor.setAttribute('type','text')
  input_valor.setAttribute('placeholder',placeholder_valor_unitario)
  input_valor.setAttribute('id',`Valor-do-Produto-${id_dinamico}`)
  input_valor.setAttribute('class','form-control')
  input_valor.setAttribute('name','campo_valor')
  input_valor.setAttribute('onkeyup','atualiza_preco()')
  input_valor.setAttribute("required",true)
  input_valor.style.height = '35px'
  input_valor.style.marginTop = '1px'
  
  let div_botao = document.createElement('div')
  div_botao.setAttribute('class','col-auto')

  let botao = document.createElement('input')
  botao.setAttribute('type','button')
  botao.setAttribute('value','Remover')
  botao.setAttribute('onclick',`remover_item('${id_dinamico}')`)
  botao.setAttribute('class','btn btn-danger btn-sm')
  botao.style.marginTop = '3px'
  botao.style.height = '30px'

  let div_quantidade = document.createElement('div')
  div_quantidade.setAttribute('class','col-auto')

  let campo_quantidade = document.createElement('input')
  campo_quantidade.setAttribute('type','number')
  campo_quantidade.setAttribute('class','form-control')
  campo_quantidade.style.height = '35px'
  campo_quantidade.style.marginTop = '5px'
  campo_quantidade.style.width = '100px'
  campo_quantidade.setAttribute('placeholder',placeholder_quantidade)
  campo_quantidade.setAttribute('name','quantidade')
  campo_quantidade.setAttribute("required",true)

  let campo_total_valor = document.createElement('div')
  campo_total_valor.setAttribute('class','col-auto')

  let input_valor_total = document.createElement('input')
  input_valor_total.setAttribute('type','number')
  input_valor_total.setAttribute('placeholder','Total')
  input_valor_total.setAttribute('name','vl_total')
  input_valor_total.setAttribute('class','form-control')
  input_valor_total.setAttribute('tabindex','-1')
  input_valor_total.setAttribute("required",true)
  //input_valor_total.setAttribute('disabled','true')
  input_valor_total.style.height = '35px'
  input_valor_total.style.marginTop = '5px'
  input_valor_total.style.width = '100px'

  campo_total_valor.appendChild(input_valor_total)
  

  div_quantidade.appendChild(campo_quantidade)
  div_botao.appendChild(botao)

  div_valor_produto.appendChild(input_valor)
  // Fim do Produto

  formulario.appendChild(div_row)
  
  div_row.appendChild(div_select)
  div_row.appendChild(div_quantidade)
  //div_row.appendChild(div_select_tipo_qtd)
  div_row.appendChild(div_valor_produto)
  div_row.appendChild(campo_total_valor)
  div_row.appendChild(div_botao)

  formulario.append(div_row)
  
}



function atualiza_preco(){
    let valor_contrato = document.querySelector('input#valor_contrato')
    let contador = 0
    let valores = window.document.getElementsByName('campo_valor')
    let data_inicial = window.document.querySelector('input#data_inicio').value
    let data_final = window.document.querySelector('input#data_fim').value
    let quantidade = window.document.getElementsByName('quantidade')
    

    let diferenca_datas = (new Date(data_final) - new Date(data_inicial)) 
    let resultado = Number(diferenca_datas) / (1000 * 60 * 60 * 24)

    for (let c = 0  ; c < valores.length ; c ++){
      
      calculo = quantidade[c].value * valores[c].value
      window.document.getElementsByName('vl_total')[c].value = calculo
      
      let franquia = document.getElementById('select-franquia').value

      switch (franquia){
        case '1':
          valores[c].setAttribute('placeholder',`Valor diário`)
          quantidade[c].setAttribute('placeholder','Dias')
          break
        case '7':
          valores[c].setAttribute('placeholder',`Valor semanal`)
          quantidade[c].setAttribute('placeholder','Semanas')
          break
        case '15':
          valores[c].setAttribute('placeholder',`Valor quinzenal`)
          quantidade[c].setAttribute('placeholder','Quinzenas')
          break
        case '30':
          valores[c].setAttribute('placeholder',`Valor mensal`)
          quantidade[c].setAttribute('placeholder','Meses')
          break
        default:
          pass
      }

      contador += calculo
    }
    let moeda = contador.toLocaleString('pt-br',{style:'currency',currency:'BRL'})
    valor_contrato.value = moeda
  }


function remover_item(id_campo){
  document.getElementById(`div-${id_campo}`).remove()
}


function EnviaDados(param){
  let campo = window.document.querySelector(`input#${param}`)
  console.log(campo)

  if (param == 'combustivel'){
      let div = window.document.querySelector('input#qtd_combustivel')
      let input_combustivel = window.document.getElementById('qtd_combustivel')
      if (campo.checked){
          div.style.display = 'inline-block'
      }else{
          div.style.display = 'none'
          input_combustivel.value = ''

      }
  }

  if (param == 'transporte'){
      let div = window.document.querySelector('input#qtd_transporte')
      let input_transporte = window.document.getElementById('qtd_transporte')
      if (campo.checked){
          div.style.display = 'inline-block'
      }else{
          div.style.display = 'none'
          input_transporte.value = ''
      }
  }
}


function atualizar() {
  let valor = Number(window.document.querySelector('select#select-franquia').value)
  let data = window.document.querySelector('input#data_inicio').value
  data = String(data) + " 12:00"

  let data_inicial = new Date(data)
  
  data_inicial.setDate(data_inicial.getUTCDate() + (valor))
 
  
  let dataf = window.document.querySelector('input#data_fim')

  let mes = (data_inicial.getMonth() + 1) < 10 ? '0' + (data_inicial.getMonth() + 1) : (data_inicial.getMonth() + 1)
  let dia = (data_inicial.getDate()) < 10 ? '0' + (data_inicial.getDate()) : (data_inicial.getDate())

  dataf.value = `${data_inicial.getFullYear()}-${mes}-${dia}`
}



