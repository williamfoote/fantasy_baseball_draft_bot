source("helpers.R")
counties <- readRDS("data/counties.rds")
library(maps)
library(mapproj)

ui <- fluidPage(
  titlePanel("censusVis"),
  
  sidebarLayout(
    sidebarPanel(
      helpText("Create demographic maps with 
               information from the 2010 US Census."),
      
      selectInput("var", 
                  label = "Choose a variable to display",
                  choices = c("Percent White", 
                              "Percent Black",
                              "Percent Hispanic", 
                              "Percent Asian"),
                  selected = "Percent White"),
      
      sliderInput("range", 
                  label = "Range of interest:",
                  min = 0, max = 100, value = c(0, 100))
    ),
    
    mainPanel(
      textOutput("selected_var"),
      textOutput("range_var")
    )
  )
)

server <- function(input, output) {
  
  output$selected_var <- renderText({ 
    paste("You have selected", input$range[1], "to", input$range[2])
  })
  
  output$range_var <- renderText({ 
    paste("You have chosen a range that goes from", input$var)
  })
  
}

# Run the app ----
shinyApp(ui = ui, server = server)
