library(shiny)
library(DT)
library(tidyverse)
models_list2 <- readRDS("models_list2.RDS")
big2 <- read.csv('big2.csv')

# Define UI for application that draws a histogram
ui <- fluidPage(
  
  # Application title
  titlePanel("Fantasy Faineants 2021 Draft Analysis"),
  h4('Predicting what factors lead to certain draft decisions.'),
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
      # Input: Select a file ----
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
      plotOutput("draft_plot")
      
      # Button
      # downloadButton("downloadData", "Download the Predictions")
    ),
    
    # Show the table with the predictions
    mainPanel(

      tabsetPanel(type = "tabs",
                  tabPanel("Results", br(), DT::dataTableOutput("mytable")),
                  tabPanel("Predictions", 
                           br(),
                           selectizeInput('position', label = 'Select a position',
                                                         choices = c('First Base' = '1B',
                                                                     'Second Base' = '2B',
                                                                     'Third Base' = '3B',
                                                                     'Shortstop' = 'SS',
                                                                     'Left Field' = 'LF',
                                                                     'Right Field' = 'RF',
                                                                     'Center Field' = 'CF',
                                                                     'Designated Hitter' = 'DH',
                                                                     'Catcher' = 'C',
                                                                     'Starting Pitcher' = 'SP',
                                                                     'Relief Pitcher' = 'RP')),
                           sliderInput("adp_slider",
                                       "Select Average Draft Position\n
                                       ADP:",
                                       value = 180,
                                       min = 1,
                                       max = 358),
                           sliderInput("rc_slider",
                                       "Select Relative Projected RC/ERA
                                       (bigger number = better RC or ERA)
                                       :",
                                       value = 0,
                                       min = -4,
                                       max = 4,
                                       step = .01),
                           h3(textOutput('prediction'))
                           )
      )
    )
  )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  
  reactiveDF<-reactive({
    req(input$name)
    df2 <- big2[big2$owner == input$name,
               c("Name", "position", "RC.ERA", "adp", "draft")]
    return(df2)
    
  })
  
  
  
  reactive_ggdata <- reactive({
    req(input$name)
    name <- input$name
    name
  })
  
    output$draft_plot <- renderPlot({
      name <- reactive_ggdata()
      ggplot(big2[big2$owner == name, ],
             aes(x = adp, y = draft, col = is_batter)) + geom_point() +
        ggtitle(paste(toupper(name), "'s 2021 Drafting Habits",
                      sep = '')) +
        xlab("Average Draft Position\nof All ESPN Users") + ylab("Actual Draft Choice")},
      height = 250,width = 350)
    
    
    output$mytable = DT::renderDataTable({
      req(input$name)
      
      return(DT::datatable(reactiveDF(),  options = list(list(pageLength = 10), 
                                                         order = list(5, 'asc')),
                           filter = c("top")))
    })
  
    reactive_predictions <-reactive({
      req(input$name)
      req(input$adp_slider)
      req(input$rc_slider)
      req(input$position)
      # Select relevant model for predictions
      this_model <- models_list2[input$name][[1]]
      new_data <- data.frame('position' = input$position,
                             'RC.ERA' = input$rc_slider,
                             'adp' = input$adp_slider)
      predicted_val <- predict(this_model, newdata = new_data)
      return(predicted_val)
    })
    
    output$prediction <- renderText(
      paste('We estimate ', toupper(reactive_ggdata()), ' would select a player with these attributes at
            pick ', round(reactive_predictions()), '.', sep = '')
    )
  
  
  
}

# Run the application 
shinyApp(ui = ui, server = server)