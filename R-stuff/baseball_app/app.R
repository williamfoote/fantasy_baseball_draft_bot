library(shiny)
library(DT)
library(tidyverse)
models_list <- readRDS("models_list.RDS")

# Define UI for application that draws a histogram
ui <- fluidPage(
  
  # Application title
  titlePanel("Iris Dataset Predictions"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
      # Input: Select a file ----
      fileInput("file1", "upload csv file here",
                multiple = FALSE,
                accept = c("text/csv",
                           "text/comma-separated-values,text/plain",
                           ".csv")), 
      selectInput('name', label = 'Select a person to analyze!',
                  choices = c('Alden' = 'alden',
                              'Alex' = 'alex',
                              'Brent' = 'brent',
                              'Cuyler' = 'cuyler',
                              'Dakota' = 'dakota',
                              'Kerry' = 'kerry',
                              'Korn' = 'korn',
                              'Jake' = 'jake',
                              'John' = 'john',
                              'Will' = 'will')
                  ),
      
      
      # Button
      # downloadButton("downloadData", "Download the Predictions")
    ),
    
    # Show the table with the predictions
    mainPanel(
      DT::dataTableOutput("mytable"),
      plotOutput("draft_plot")
    )
  )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  
  reactiveDF<-reactive({
    req(input$file1)
    df <- read.csv(input$file1$datapath, stringsAsFactors = TRUE)
    
    df$predictions<-predict(irisModel, newdata = iris, type ="class")
    return(df)
    
  })
  
  reactiveGraph <- reactive({
    req(input$name)
    name <- input$name
    ggplot(big2[big2$owner == name, ],
           aes(x = adp, y = draft, col = is_batter)) + geom_point()
  })
  
  output$draft_plot <- 
  
  output$mytable = DT::renderDataTable({
    req(input$file1)
    
    return(DT::datatable(reactiveDF(),  options = list(pageLength = 100), filter = c("top")))
  })
  
  
  # Downloadable csv of selected dataset ----
  output$downloadData <- downloadHandler(
    filename = function() {
      paste("data-", Sys.Date(), ".csv", sep="")
    },
    content = function(file) {
      write.csv(reactiveDF(), file, row.names = FALSE)
    }
  )
  
  
  
}

# Run the application 
shinyApp(ui = ui, server = server)