require(shiny)
require(shinydashboard)
require(plotly)
require(shinycssloaders)

shinyUI(
    dashboardPage(title="Modelo SHEEM",
                  
                  dashboardHeader(title = img(src='logo-hack.png',height = 72, width = 72)),
                  
                  # Sidebar
                  dashboardSidebar(
                      sidebarMenu(
                          menuItem("Problematica",tabName = "problematica",icon = icon('question')),
                          menuItem("Metodología",tabName = "metodologia",icon = icon('microscope')),
                          menuItem("Propuesta",tabName = "propuesta",icon = icon('chart-line'))
                          
                      ) 
                  ),
                  dashboardBody(
                      HTML('<link rel="stylesheet" href="style.css">'),
                      # Pagina Principal
                      tabItems(
                          tabItem(tabName = "problematica",
                                  h1("Vinculación Rentable"),
                                  fluidRow(
                                      column(7,
                                            p(style='text-align:justify',"BBVA cuenta ya con una matriz de tenencia que permite diferenciar el grado de vinculación que tienen con cada uno de sus clientes, pero puede ser mejorada con la adición de la variable rentabilidad esto es: el posible aumento del volumen de las ventas ya que se hará con centro en el cliente, ayudando a ofrecer productos/servicios adaptados a sus preferencias de este modo, no solo se consigue vender más a través de la fidelización del cliente, sino, vender mejor."),
                                            br(),
                                            p(style='text-align:justify',"Incremento del margen de beneficios, reducción del riesgo del producto para los clientes y reducción del riesgo que representa el cliente para bbva, análisis de la rentabilidad cliente que es consecuencia de la rentabilidad que obtiene respecto a todos sus productos y el uso de la tecnología adecuada que es una  ‘lista de buenas prácticas’ que evita tener que destinar tiempo y recursos (ahorro de costes) a la realización de tareas que, perfectamente, pueden ser automatizadas y prevención de errores humanos.")
                                            ),
                                    column(4,offset = 1,img(src='Vinculación-rentable.png',height = 250, width = 250)))
                          ),
                          tabItem(tabName = "metodologia",
                                  h1("Metodología"),
                                  p("Creamos indicadores de riesgo y vincualcion para el de riesgo:"),
                                  br(),
                                  HTML("
                                       <p>Para el riesgo obtuvimos el <strong>componente principal</strong> de los indicadores Riesgo 1 y Riesgo 2 en la tabla 2.</p>
                                       <p>Para el indicador de vincualcion tomamos en cuenta los servicios como activos y pasivos, la vinculacion digital y la rapidez con la que adquiere mas servicios</p>
                                       <p>Para esto empleamos la siguiente metodología:</p>
                                       <div class = 'myimg'>
                                        <img src='vin_f.png' width=80%>
                                       </div>
                                       <br>
                                       <br>
                                       <br>
                                       <p>Una vez que obtuvimos los indicadores los agregamos a los datos sociodemograficos para generar clusters con los clientes</p>
                                       <div class = 'myimg'>
                                        <img src='Clusters.png' height=400px>
                                       </div>
                                       "),
                                  hr(),
                                  h1("Nuestros Perfiles"),
                                  p('Con la obtención de nuestros clusters hemos podido identificar 6 perfiles de clientes'),
                                  br(),
                                  h3("Perfil 1"),
                                  tags$div(class = 'myimg',img(src = "C1.png",width = 600)),
                                  
                                  h3("Perfil 2"),
                                  tags$div(class = 'myimg',img(src = "C2.png",width = 600)),
                                  
                                  h3("Perfil 3"),
                                  tags$div(class = 'myimg',
                                           img(src = "C3.png",width = 600)),
                                  
                                  h3("Perfil 4"),
                                  tags$div(class = 'myimg',
                                           img(src = "C4.png",width = 600)),
                                  
                                  h3("Perfil 5"),
                                  tags$div(class = 'myimg',
                                           img(src = "C5.png",width = 600)),
                                  
                                  h3("Perfil 6"),
                                  tags$div(class = 'myimg',img(src = "C6.png",width = 600)),
                          ),
                          tabItem(tabName = "propuesta",
                                  h1("Propuesta"),
                                  p("Para generar la propuesta visualizamos los productos mas frecuentes y la rentabilidad dentro los prefiles:"),
                                  br(),
                                  selectInput("cluster","Perfil",choices = c("C1","C2","C3","C4","C5","C6"),selected = "C1"),
                                  fluidRow(
                                      column(6,
                                             h3("Productos por perfil"),
                                             withSpinner(plotlyOutput("productos"))),
                                      column(6,
                                             h3("Rentabilidad del perfil"),
                                             withSpinner(plotlyOutput("rent")))),
                                  br(),
                                  p("Con base a esto podemos recomendar los productos con mayor rentabilidad por grupo y riesgo: "),
                                  h3("Productos"),
                                  tableOutput("recommend")
                                  
                                )
                          
                          
                          
                      )
                  )
    )
)
