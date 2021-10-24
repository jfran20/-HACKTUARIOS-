require(dplyr)
require(class)
require(tidyr)
require(stats)



######  Generacion de clusters

Clt_info <- 
  read.csv("./db/base 01_V3.csv",sep = "|") %>% 
  select(CODIGO_CLIENTE,EDAD,GENERO,
         ESTADO_CIVIL,INGRESO_MENSUAL,PERIODO) %>% 
    filter(GENERO != 5) %>% 
  group_by(CODIGO_CLIENTE) %>% 
  arrange(PERIODO) %>% 
  summarise(
    EDAD = last(EDAD),
    GENERO = last(GENERO),
    ESTADO_CIVIL = last(ESTADO_CIVIL),
    INGRESO_MENSUAL = median(INGRESO_MENSUAL,na.rm = T)) %>% 
  ungroup() %>% 
  mutate(
         GENERO = ifelse(GENERO != '',paste0('G_',GENERO),'G_Na'),
         G_valor = 1,
         ESTADO_CIVIL = ifelse(ESTADO_CIVIL != '',paste0('EC_',ESTADO_CIVIL),'EC_Na'),
         E_valor = 1) %>%
  spread(key = GENERO,value = G_valor) %>% 
  spread(key = ESTADO_CIVIL,value = E_valor) %>% 
  mutate(across(G_F:EC_Y,~ifelse(is.na(.x),0,1)))

edades <- Clt_info %>% pull(EDAD) %>% mean(na.rm = T)
ingresos <- Clt_info %>% pull(EDAD) %>% median(na.rm = T)
Vinculacion <- read.csv("./db/Otros/Vinculacion.csv")
Clientes <- read.csv("./db/Otros/Cliente.csv") %>% filter(Clt == 'Si') %>% pull(CODIGO_CLIENTE)
Riesgo <- read.csv("./db/Otros/PCARik.csv") %>% distinct()

Clt_info <- Clt_info %>% mutate(
  EDAD = ifelse(is.na(EDAD),edades,EDAD),
  INGRESO_MENSUAL = ifelse(is.na(INGRESO_MENSUAL),ingresos,INGRESO_MENSUAL)) %>% 
  inner_join(Vinculacion) %>% 
  inner_join(Riesgo) 
# %>% 
  # filter(!CODIGO_CLIENTE %in% Clientes)

write.csv(Clt_info,'to_clustall.csv',row.names = F)

