#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(ggplot2)
# Define UI for application that draws a histogram
ui <- tagList(
  navbarPage(
    "Yelp Gym Review Recommandation",
    tabPanel("General recommandation", 
             h4("General suggestions for gyms:"),
             h5("We recommend that you extend your opening time."),
             h5("Your staff should be more qualified, responsible and hospitable."),
             h5("We suggest you make the price of the gym reasonable.	"),
             h5("We recommend you provide some special appointment service for customers."),
             h5("You should create some kids-friendly area to accomodate kids and separate kids from exercise area.")
             ),
    tabPanel("Suggestions for gyms",
      sidebarPanel(
        textInput("name", "Gym name:"),
        textInput("city","City"),
        actionButton("search","Search")
      ),
      mainPanel(
        h4("Welcome to gym suggestion recommandation! Please enter the name and city of the gym."),
        verbatimTextOutput("txtout",placeholder=TRUE)
      )
    ),
    tabPanel("Contact information",
        h5("Chen Qian, cqian44@wisc.edu")
    )
  )
)

# Define server logic required to draw a histogram
server <- function(input,output,session) {
  
  data <- reactive({
    read.csv('gym_suggestion.csv',sep='|',header=TRUE)
  })
  
  a <- reactive({
    which(data()$name==input$name & data()$city==input$city)
  })
  
  
  observeEvent(input$search, {
    removeUI(selector="#groupinput")
    removeUI(selector="#suggest")
    removeUI(selector="#stars")
    groupoption <- list()
    if(length(a())>=1)
    {
      for(i in 1:length(a()))
      {
        groupoption[[paste(data()$name[a()[i]],paste0(data()$address[a()[i]],',',data()$city[a()[i]],',',data()$state[a()[i]]))]]<-paste0(data()$address[a()[i]],'\n',gsub('\t','\n',data()$suggestion[a()[i]]))
      }
      insertUI(
      selector = "#txtout",
      where = "afterEnd",
      ui = radioButtons("groupinput","Select the gym you want:",groupoption,width='100%')
    )
      insertUI(
      selector = "#groupinput",
      where = "afterEnd",
      ui = actionButton("suggest","Suggestion")
    )
      insertUI(
      selector = "#suggest",
      where = "afterEnd",
      ui = actionButton("stars","Review star")
    )
      
    }
  })

  
  outtext <- eventReactive(input$search,{
    if(length(a())==0)
      return('Your input maybe incorrect. Please check it!')
    else 
      return("Here are some gyms that you want. Please select one!")
    })
  
  output$txtout<- renderText({
      return(outtext())
    })

  
  textn <- eventReactive(input$suggest,{
    strsplit(input$groupinput,'\n')[[1]]
  })
  
  data1 <- reactive({
    read.csv('review_stars.csv',sep='|',header=TRUE)
  })
  
  plot <- eventReactive(input$stars,{
    ggplot(data1()[which(data1()$name==input$name & data1()$city==input$city & data1()$address==strsplit(input$groupinput,'\n')[[1]][1]),], aes(stars)) + geom_bar(stat="count",fill="#0066cc")+ theme(plot.margin=unit(rep(2,5),'lines'))
  })
  
  observeEvent(input$stars,{
    removeUI(selector="#result1")
    removeUI(selector="#result2")
    removeUI(selector="#result3")
    removeUI(selector="#result4")
    removeUI(selector="#result5")
    removeUI(selector="#result6")
    removeUI(selector="#plot")
    removeUI(selector="#result1")
    insertUI(
      selector = "#stars",
      where = "afterEnd",
      ui = plotOutput("plot",width='400px')
    )
  })
  output$plot<- renderPlot({
    plot()
  })
  
  observeEvent(input$suggest,{
    removeUI(selector="#result1")
    removeUI(selector="#result2")
    removeUI(selector="#result3")
    removeUI(selector="#result4")
    removeUI(selector="#result5")
    removeUI(selector="#result6")
    removeUI(selector="#plot")
    insertUI(
        selector = "#stars",
        where = "afterEnd",
        ui = verbatimTextOutput("result1")
      )
    insertUI(
      selector = "#result1",
      where = "afterEnd",
      ui = verbatimTextOutput("result2")
    )
    insertUI(
      selector = "#result2",
      where = "afterEnd",
      ui = verbatimTextOutput("result3")
    )
    insertUI(
      selector = "#result3",
      where = "afterEnd",
      ui = verbatimTextOutput("result4")
    )
    insertUI(
      selector = "#result4",
      where = "afterEnd",
      ui = verbatimTextOutput("result5")
    )
    insertUI(
      selector = "#result5",
      where = "afterEnd",
      ui = verbatimTextOutput("result6")
    )
  })
  output$result1 <- renderText({
    if(is.na(textn()[2]))
      return(NULL)
    else
      return(textn()[2])
    })
  output$result2 <- renderText({
    if(is.na(textn()[3]))
      return(NULL)
    else
      return(textn()[3]) 
    }) 
  output$result3 <- renderText({
    if(is.na(textn()[4]))
      return(NULL)
    else
      return(textn()[4])
    })  
  output$result4 <- renderText({
    if(is.na(textn()[5]))
      return(NULL)
    else
      return(textn()[5])
    })  
  output$result5 <- renderText({
    if(is.na(textn()[6]))
      return(NULL)
    else
      return(textn()[6])
    })  
  output$result6 <- renderText({
    if(is.na(textn()[7]))
      return(NULL)
    else
      return(textn()[7])
    })
  
  
  
}  
# Run the application 
shinyApp(ui = ui, server = server)

