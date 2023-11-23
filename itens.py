import psycopg2 as pg 

conexao = pg.connect(
    dbname = 'ekoos_leo',
    port = '5432',
    host = '192.168.0.7',
    user = 'postgres',
    password = 'economia11@#'
)
cursor = conexao.cursor()

select_all = []
cursor.execute('''select cod_pessoa from ek_pessoa''')
all_people = cursor.fetchall()

for p in all_people:
    select_all.append(p[0])

lista_off = []

cursor.execute('''
select cod_pessoa
                    
                from ek_pessoa inner join ek_cidade on ek_cidade.num_cidade = ek_pessoa.cidade
                inner join ek_estado on ek_estado.num_estado = ek_pessoa.estado
                

''')
peoples_expecificas = cursor.fetchall()
select_espe = []

for s in select_all:
    select_all.append(s[0])
    if s[0] in select_all:
        print(s[0])

