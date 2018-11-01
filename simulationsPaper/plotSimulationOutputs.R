library(ggplot2)
library(data.table)

outputFolder <- './modelOutputs'
modelOutputFiles <- list.files( outputFolder)

## Examine lake scenarios 
lakeScenarios <- paste(outputFolder,
                       modelOutputFiles[grep("groups_lake", modelOutputFiles)],
                       sep = "/")

lakeScenariosData <- data.table(Year  = integer(),
                                Group = character(),
                                Population = numeric(),
                                Node = character(),
                                Sex = character(),
                                Scenario = character())
           

for(lkScn in lakeScenarios){
    rawIn <- fread(lkScn)
    rawIn[ , Year := 0:( nrow(rawIn) - 1)]
    rawIn2 <- melt(rawIn, id.vars = 'Year',
                   value.name = "Population",
                   variable.name = "Group")   
    rawIn2[ , Group := as.character(Group)]
    rawIn2[ , Node := gsub("(_male|_female|_sterile-male)", "", Group)]
    rawIn2[ , Sex := "Female"]
    rawIn2[ grep("_male", Group), Sex := "Male"]
    rawIn2[ grep("-male", Group), Sex := "Sterile male"]
    rawIn2[ , Scenario := gsub( "./modelOutputs/groups_lake_|.csv", "", lkScn,)]
    lakeScenariosData = rbind(lakeScenariosData, rawIn2)
}

lakeScenariosData <- copy(lakeScenariosData[ Year != 101,])
lakeScenariosData


lakeScn <- fread("./inputParameters/lakeSummaryTable.csv")
lakeScn

setkey(lakeScenariosData, "Scenario")
setkey(lakeScn, "Scenario")

lakeScenariosData <- lakeScenariosData[ lakeScn, allow.cartesian = TRUE]
lakeScenariosData[ , unique(Stocking)]

lakeScenariosData[ , Stocking := factor(Stocking,
                                        levels = c("Reference", "Low", "Mid", "High"))]

allNodeGroup <- ggplot(lakeScenariosData, aes(x = Year, y = Population,
                                              color = Stocking, linetype = Sex)) +
    geom_vline(xintercept = 30, color = 'grey25') + 
    geom_line() +
    facet_grid( PlotLife ~ Node) +
    theme_minimal() +
    scale_color_manual(values = c("black", "red", "blue", "orange")) +
    scale_y_continuous( labels = scales::comma) 


allNodeGroup
ggsave(plot = allNodeGroup,
       filename = "./summaryFigures/lakePlotAllNodesAllGroups.pdf",
       width = 7, height = 5)

lakeScenariosData
lakeNodeTotalPop <- lakeScenariosData[ , .('Population' = sum(Population)),
                                      by = list(Year, Node, Scenario, Stocking, Lifespan, PlotLife)]

lakeTotalPop <- lakeScenariosData[ , .('Population' = sum(Population)),
                                  by = .(Year,  Scenario, Stocking, Lifespan, PlotLife,
                                            Sex == "Male" | Sex == "Female")]

lakeTotalPop[ , Type := "Sterile-males"]
lakeTotalPop[ Sex == TRUE, Type := "Non-released"]

lakeTotalPlot <- ggplot(lakeTotalPop, aes(x = Year,
                                          y = Population, color = Stocking,
                                          linetype = Type)) +
    geom_vline(xintercept = 30, color = 'grey25') + 
    geom_line() +
    facet_grid( PlotLife ~ ., scales = "free_y") +
    theme_minimal() +
    scale_color_manual(values = c("black", "red", "blue", "orange")) +
    scale_y_continuous( labels = scales::comma)
print(lakeTotalPlot )

ggsave(filename = "./summaryfigures/lakeTotalPop.pdf", plot = lakeTotalPlot, width = 6, height = 4)


##############################
## River Scenarios
riverScenarios <- paste(outputFolder,
                       modelOutputFiles[grep("groups_river", modelOutputFiles)],
                       sep = "/")

riverScenariosData <- data.table(Year  = integer(),
                                 Group = character(),
                                 Population = numeric(),
                                 Node = character(),
                                 Scenario = character(),
                                 Barrier= character(),
                                 Harvest = character())
           

for(rvScn in riverScenarios){
    rawIn <- fread(rvScn)
    rawIn[ , Year := 0:( nrow(rawIn) - 1)]
    rawIn2 <- melt(rawIn, id.vars = 'Year',
                   value.name = "Population",
                   variable.name = "Group")   
    rawIn2[ , Group := as.character(Group)]
    rawIn2[ , Node := gsub("(_Pool \\d all)", "", Group)]
    rawIn2[ , Scenario := sub("(./modelOutputs/groups_river_)(Scn_\\d)_(\\w*).csv",
                              "\\2-\\3", rvScn)]
    rawIn2[ , Barrier := sub("(./modelOutputs/groups_river_)(Scn_\\d)_(\\w*).csv",
                              "\\2", rvScn)]
    rawIn2[ , Harvest := gsub("(./modelOutputs/groups_river_)(Scn_\\d)_(\\w*).csv",
                              "\\3", rvScn)]
    riverScenariosData = rbind(riverScenariosData, rawIn2)
}

riverScenariosData <- copy(riverScenariosData[ Year < 99,])

riverScenariosData[, unique(Barrier)]
riverScenariosData[, Barrier := factor(Barrier, labels = c("Baseline", "10%", "50%"))]
riverScenariosData[ , HarvestSize := "Uniform"]
riverScenariosData[ grepl("size", Harvest), HarvestSize := "Larger fish"]
riverScenariosData[ , Harvest := factor(gsub("size", "", Harvest))]

riverScenariosData[ , Harvest := factor(Harvest,
                                        labels = c("Upriver-Low",
                                                   "Upriver-Medium",
                                                   "Upriver-High",
                                                   "Downriver-Low",
                                                   "Downriver-Medium",
                                                   "Downriver-High",
                                                   "None"))]
riverScenariosData[ , HarvestLevel := gsub("(\\w+)-(\\w+)", "\\2", Harvest)]
riverScenariosData[ , HarvestLocation := gsub("(\\w+)-(\\w+)", "\\1", Harvest)]


t1 <- riverScenariosData[ Harvest != "None",]
t2 <- riverScenariosData[ Harvest == "None",]
t3 <- riverScenariosData[ Harvest == "None",]

t2[ , HarvestLocation := "Upriver"]
t3[ , HarvestLocation := "Downriver"]

riverScenariosDataPlot <- rbind(t1, t2, t3)

unique(riverScenariosDataPlot$HarvestLocation)
unique(riverScenariosDataPlot$HarvestLevel)
unique(riverScenariosDataPlot$HarvestSize)

riverScenariosDataPlot[ ,
                       HarvestLevel := factor(HarvestLevel,
                                              levels =
                                                  unique(riverScenariosDataPlot$HarvestLevel)[c(4, 1:3)])]

## riverScenariosDataPlot[ , Barrier := factor(Barrier, levels = c("Baseline", "10%", "50%"))]
riverScenariosDataPlot[ , HarvestSize := factor(HarvestSize, levels = c("Uniform", "Larger fish"))]

levels(riverScenariosDataPlot$HarvestLevel)<-
                              c("No harvest",
                                "25% harvest",
                                "50% harvest",
                                "75% harvest")

riverPlotAll <- ggplot(riverScenariosDataPlot, aes(x = Year,
                                                  y = Population,
                                                  linetype = HarvestLocation,
                                                  color = Barrier)) +
    geom_vline(xintercept = 15, color = 'grey25') + 
    facet_grid(  Node + HarvestSize ~ HarvestLevel, scales = "free_y") +
    geom_line() +
    scale_color_manual(values = c("red", "blue", "black")) +
    scale_linetype("Harvest\nlocation")  +
    theme_minimal() +
    theme(panel.spacing = unit(1, "lines"))
print(riverPlotAll)

ggsave("./summaryfigures/riverPlotAll.pdf", riverPlotAll, width = 6, height = 6)
