require(shiny)
require(dplyr)
require(plotly)

shinyServer(function(input, output) {
    clusters <- read.csv('db/Otros/Cluster_Final.csv') %>% select(CODIGO_CLIENTE,Cluster)

    base_5 <- read.csv('db/base 05_edit.csv') %>% 
        select(CODIGO_CLIENTE,PRODUCTO,PERIODO)
    
    top_prod <- function(cluster){
        prods <- 
            prod_group_temp %>% filter(Cluster == cluster) %>% 
            arrange(PERIODO,PRODUCTO)
        
        plot <- 
            plot_ly(prods,type = 'bar', x = ~PRODUCTO, y = ~N,frame =~PERIODO,color = I("#30D9C8")) %>%
            layout(title = '',
                   xaxis = list(title = '',showgrid = F),
                   yaxis = list(title = 'Frecuencia',showgrid = F),
                   showlegend = FALSE,
                   font = list(color = "white"),
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)'
            ) %>% 
            config(displayModeBar = F)
        
    }
    
    rent_c <- function(cluster){
        rent %>% filter(Cluster == cluster) %>% arrange(PERIODO) %>% 
            plot_ly(type = 'scatter',mode = 'lines',x = ~as.factor(PERIODO), y = ~RATIO_RENTABILIDAD,color = I("#30D9C8")) %>%
            layout(title = '',
                   xaxis = list(title = '',showgrid = F),
                   yaxis = list(title = 'Rentabilidad',showgrid = F),
                   showlegend = FALSE,
                   font = list(color = "white"),
                   plot_bgcolor='rgba(0,0,0,0)',
                   paper_bgcolor='rgba(0,0,0,0)') %>% 
            config(displayModeBar = F)
    }
    
    
    rent <-
        read.csv('db/base 04_edit.csv') %>% 
        inner_join(clusters) %>% 
        select(CODIGO_CLIENTE,Cluster,PERIODO,NUMERADOR_RATIO_RENTABILIDAD,DENOMINADOR_RATIO_RENTABILIDAD) %>% 
        group_by(Cluster,PERIODO) %>% 
        summarise(
            RATIO_RENTABILIDAD = sum(NUMERADOR_RATIO_RENTABILIDAD,na.rm = T)/sum(DENOMINADOR_RATIO_RENTABILIDAD,na.rm = T))
    
    prod_group_temp <- 
        base_5 %>% inner_join(clusters) %>% 
        group_by(Cluster,PERIODO,PRODUCTO) %>% 
        summarise(N = n()) %>% ungroup()
    
    
    output$productos <- renderPlotly(top_prod(input$cluster))
    output$rent <- renderPlotly(rent_c(input$cluster))
    
    get_tbl <- function(cluster){
        productos <- switch (cluster,
            "C1" = c("TARJETAS","CONSUMO"),
            "C2" = c("TJ_EMPRESAS","TARJETAS"),
            "C3" = c("TJ_EMPRESAS","HIPOTECARIO","TARJETAS"),
            "C4" = c("CONSUMO","TARJETAS"),
            "C5" = c("TJ_EMPRESAS","PRESTAMOS_COMERCIALES"),
            "C6" = c("TJ_EMPRESAS","TARJETAS")
        )
        riesgo <- switch (cluster,
             "C1" = c("BAJO","BAJO"),
             "C2" = c("ALTO","BAJO"),
             "C3" = c("ALTO","BAJO","BAJO"),
             "C4" = c("BAJO","BAJO"),
             "C5" = c("ALTO","ALTO"),
             "C6" = c("ALTO","BAJO")
        )
        
        return(as.data.frame(cbind(Productos = productos,Riesgo = riesgo)))
    }
    output$recommend <- renderTable(get_tbl(input$cluster))
    
})
