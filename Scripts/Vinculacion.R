require(dplyr)

#  CODIGO PARA LA CREACION DEL INDICADOR "VINCULACION"

Vinculacion <-
  read.csv("./db/base 03_V3.csv",sep = "|") %>% 
  select(-c(TIPO_DOCUMENTO,NUMERO_DOCUMENTO,
            SALDO_MEDIO_INVERSION_RENTABLE,SALDO_MEDIO_CARTERA_ATRASADA,
            VINCULACION_EMPRESA,VINCULACION_PN)) %>%
  inner_join(read.csv("./db/base 01_V3.csv",sep = "|") %>% 
               select(CODIGO_CLIENTE,PERIODO,AFILIACION_BANCA_ONLINE,AFILIACION_SMS) %>% 
               mutate(across(AFILIACION_BANCA_ONLINE:AFILIACION_SMS,~ifelse(.x == "SI",1,0))),
             by =c("CODIGO_CLIENTE","PERIODO")) %>%
    relocate(PERIODO,.after = AFILIACION_SMS) %>% 
  mutate(across(SALDO_MEDIO_VISTA:SALDO_MEDIO_TJ_EMPRESAS,~ifelse(.x != 0,1,0))) %>%
  mutate(across(FAM_COBRANZAS:FAM_VISANET,~.x/3)) %>% 
  mutate(n_servicios = rowSums(across(SALDO_MEDIO_VISTA:AFILIACION_SMS)),
         Activos = rowSums(across(SALDO_MEDIO_VISTA:SALDO_MEDIO_FONDO_MUTUO)),
         Pasivos = rowSums(across(SALDO_MEDIO_AUTOS:SALDO_MEDIO_TJ_EMPRESAS)),
         Digitales = rowSums(across(T_NETCASH:AFILIACION_SMS),na.rm = T),
         Ratio = ifelse(Pasivos == 0,Activos,Activos/Pasivos)) %>%
  group_by(CODIGO_CLIENTE) %>% 
  arrange(PERIODO) %>% 
  summarise(v_vinculacion = lm(n_servicios~c(1:length(n_servicios)))$coefficients[2],
            Ratio = last(Ratio),
            Digitales = last(Digitales)) %>% 
  ungroup() %>% 
  mutate(
        v_vinculacion = ifelse(is.na(v_vinculacion),1,v_vinculacion),
        VINCULACION = (Ratio + Digitales) * (1 + v_vinculacion)) %>% 
    select(CODIGO_CLIENTE,VINCULACION)
  

write.csv(Vinculacion,"Vinculacion.csv",row.names = F)
