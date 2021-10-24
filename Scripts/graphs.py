import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import datetime as dt

os.chdir("C:/Users/mi03127/Documents/HACK/bases")

b4 = pd.read_csv('b4.csv', sep='|')
b5 = pd.read_csv('b5.csv', sep='|')

rentabilidad = pd.merge(b4, b5, how="left", on=['PERIODO', 'CODIGO_CLIENTE', 'SALDO_PUNTUAL','MARGEN_FINANCIERO', 'COMISIONES','MARGEN_BRUTO',
                                                'EXPOSICION_DEFAULT','PERDIDA_ESPERADA','NUMERADOR_RATIO_RENTABILIDAD','DENOMINADOR_RATIO_RENTABILIDAD','RATIO_RENTABILIDAD'])
rentabilidad['PERIODO'] = rentabilidad.PERIODO.astype(str)
rentabilidad['PERIODO'] = [list(i) for i in rentabilidad.PERIODO]
fecha = pd.DataFrame([i for i in rentabilidad.PERIODO], columns=['F1','F2','F3','F4','M1','M2'])
rentabilidad['YEAR'] = fecha.F1 + fecha.F2 + fecha.F3 + fecha.F4
rentabilidad['MES'] = fecha.M1 + fecha.M2
rentabilidad = pd.concat([rentabilidad.YEAR, rentabilidad.MES, rentabilidad.CODIGO_CLIENTE, rentabilidad.SALDO_PUNTUAL], axis=1)

edad_sexo = pd.read_csv('b1.csv', sep='|')
edad_sexo['PERIODO'] = edad_sexo.PERIODO.astype(str)
edad_sexo['PERIODO'] = [list(i) for i in edad_sexo.PERIODO]
fecha = pd.DataFrame([i for i in edad_sexo.PERIODO], columns=['F1','F2','F3','F4','M1','M2'])
edad_sexo['YEAR'] = fecha.F1 + fecha.F2 + fecha.F3 + fecha.F4
edad_sexo['MES'] = fecha.M1 + fecha.M2
edad_sexo = pd.concat([edad_sexo.YEAR, edad_sexo.MES, edad_sexo.CODIGO_CLIENTE, edad_sexo.EDAD, edad_sexo.GENERO], axis=1)

merge = pd.merge(rentabilidad, edad_sexo, how="left", on=['YEAR', 'MES', 'CODIGO_CLIENTE'])
merge = merge.drop_duplicates()

merge.EDAD.fillna("-1", inplace=True)
merge['EDAD'] = merge.EDAD.astype(int)
merge['EDAD'] = merge.apply(lambda x: 10 if x.EDAD > 0 and x.EDAD <= 10 else x.EDAD, axis=1)
merge['EDAD'] = merge.apply(lambda x: 20 if x.EDAD > 10 and x.EDAD <= 20 else x.EDAD, axis=1)
merge['EDAD'] = merge.apply(lambda x: 30 if x.EDAD > 20 and x.EDAD <= 30 else x.EDAD, axis=1)
merge['EDAD'] = merge.apply(lambda x: 40 if x.EDAD > 30 and x.EDAD <= 40 else x.EDAD, axis=1)
merge['EDAD'] = merge.apply(lambda x: 50 if x.EDAD > 40 and x.EDAD <= 50 else x.EDAD, axis=1)
merge['EDAD'] = merge.apply(lambda x: 60 if x.EDAD > 50 and x.EDAD <= 60 else x.EDAD, axis=1)
merge['EDAD'] = merge.apply(lambda x: 70 if x.EDAD > 60 and x.EDAD <= 70 else x.EDAD, axis=1)
merge['EDAD'] = merge.apply(lambda x: 80 if x.EDAD > 70 and x.EDAD <= 80 else x.EDAD, axis=1)
merge['EDAD'] = merge.apply(lambda x: 90 if x.EDAD > 80 and x.EDAD <= 90 else x.EDAD, axis=1)
merge['EDAD'] = merge.apply(lambda x: 100 if x.EDAD > 90 else x.EDAD, axis=1)
merge['EDAD'] = merge.apply(lambda x: 'NA' if x.EDAD == -1 else x.EDAD, axis=1)

merge = merge[['YEAR', 'MES', 'CODIGO_CLIENTE', 'SALDO_PUNTUAL', 'EDAD', 'GENERO']]
merge.columns = ['YEAR', 'MES', 'CODIGO_CLIENTE', 'SALDO_PUNTUAL', 'EDAD', 'GENERO']

saldo = merge.SALDO_PUNTUAL
edad = merge.EDAD
year = merge.YEAR
genero = merge.GENERO

bar_edad = px.bar(merge, x=edad, y=saldo, color=year, barmode='group')
bar_edad.write_html('bar_edad.html', auto_open=True)

bar_gen = px.bar(merge, x=genero, y=saldo, color=year, barmode='group')
bar_gen.write_html('bar_gen.html', auto_open=True)

b3 = pd.read_csv('b3.csv', sep='|')
b3['PERIODO'] = b3.PERIODO.astype(str)
b3['PERIODO'] = [list(i) for i in b3.PERIODO]
fecha = pd.DataFrame([i for i in b3.PERIODO], columns=['F1','F2','F3','F4','M1','M2'])
b3['PERIODO'] = fecha.F1 + fecha.F2 + fecha.F3 + fecha.F4

b3_2020 = b3[b3.PERIODO != '2021']
P10 = b3_2020.SALDO_MEDIO_VISTA.sum()
P20 = b3_2020.SALDO_MEDIO_AHORRO.sum()
P30 = b3_2020.SALDO_MEDIO_CTS.sum()
P40 = b3_2020.SALDO_MEDIO_PLAZO.sum()
P50 = b3_2020.SALDO_MEDIO_FONDO_MUTUO.sum()
A10 = b3_2020.SALDO_MEDIO_AUTOS.sum()
A20 = b3_2020.SALDO_MEDIO_CONSUMO.sum()
A30 = b3_2020.SALDO_MEDIO_TARJETAS.sum()
A40 = b3_2020.SALDO_MEDIO_HIPOTECARIO.sum()
A50 = b3_2020.SALDO_MEDIO_CARTERA.sum()
A60 = b3_2020.SALDO_MEDIO_LEASING.sum()
A70 = b3_2020.SALDO_MEDIO_PRESTAMOS_COMERCIALES.sum()
A80 = b3_2020.SALDO_MEDIO_COMEXT.sum()
A90 = b3_2020.SALDO_MEDIO_TJ_EMPRESAS.sum()

b3_2021 = b3[b3.PERIODO != '2020']
P11 = b3_2021.SALDO_MEDIO_VISTA.sum()
P21 = b3_2021.SALDO_MEDIO_AHORRO.sum()
P31 = b3_2021.SALDO_MEDIO_CTS.sum()
P41 = b3_2021.SALDO_MEDIO_PLAZO.sum()
P51 = b3_2021.SALDO_MEDIO_FONDO_MUTUO.sum()
A11 = b3_2021.SALDO_MEDIO_AUTOS.sum()
A21 = b3_2021.SALDO_MEDIO_CONSUMO.sum()
A31 = b3_2021.SALDO_MEDIO_TARJETAS.sum()
A41 = b3_2021.SALDO_MEDIO_HIPOTECARIO.sum()
A51 = b3_2021.SALDO_MEDIO_CARTERA.sum()
A61 = b3_2021.SALDO_MEDIO_LEASING.sum()
A71 = b3_2021.SALDO_MEDIO_PRESTAMOS_COMERCIALES.sum()
A81 = b3_2021.SALDO_MEDIO_COMEXT.sum()
A91 = b3_2021.SALDO_MEDIO_TJ_EMPRESAS.sum()

SALDO_TOTAL_2020 = [P10,P20,P30,P40,P50,A10,A20,A30,A40,A50,A60,A70,A80,A90]
SALDO_TOTAL_2021 = [P11,P21,P31,P41,P51,A11,A21,A31,A41,A51,A61,A71,A81,A91]
PRODUCTO = ['VISTA','AHORRO','CTS','PLAZO','FONDOMUTUO','AUTOS','CONSUMO','TARJETAS','HIPOTECARIO','CARTERA','LEASING','PRESTAMOSCOMERCIALES','COMEXT','TJEMPRESAS',]
TIPO_PRODUCTO = ['PASIVO', 'PASIVO', 'PASIVO', 'PASIVO', 'PASIVO', 'ACTIVO', 'ACTIVO', 'ACTIVO', 'ACTIVO', 'ACTIVO', 'ACTIVO', 'ACTIVO', 'ACTIVO', 'ACTIVO']

activo_pasivo_2020 = pd.DataFrame()
activo_pasivo_2020['PRODUCTO'] = PRODUCTO
activo_pasivo_2020['SALDO_TOTAL'] = SALDO_TOTAL_2020
activo_pasivo_2020['TIPO_PRODUCTO'] = TIPO_PRODUCTO

activo_pasivo_2021 = pd.DataFrame()
activo_pasivo_2021['PRODUCTO'] = PRODUCTO
activo_pasivo_2021['SALDO_TOTAL'] = SALDO_TOTAL_2021
activo_pasivo_2021['TIPO_PRODUCTO'] = TIPO_PRODUCTO

activo_pasivo_2020 = px.sunburst(activo_pasivo_2020, path=[TIPO_PRODUCTO, PRODUCTO], values=SALDO_TOTAL_2020, title='2020')
activo_pasivo_2020.write_html('pie_activo_pasivo_2020.html', auto_open=True)

activo_pasivo_2021 = px.sunburst(activo_pasivo_2021, path=[TIPO_PRODUCTO, PRODUCTO], values=SALDO_TOTAL_2021, title='2021')
activo_pasivo_2021.write_html('pie_activo_pasivo_2021.html', auto_open=True)