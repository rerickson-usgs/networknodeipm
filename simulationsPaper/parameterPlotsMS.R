library(reshape2)
library(ggplot2)

omega = 0:150
sizeRepo <- data.frame(Size = omega,
		   normal = Logistic(omega, 0, 1, 40, -4),
		   modified =Logistic(omega, 0, 1, 35, -4)) 
		   
sizeRepo2 <- melt(sizeRepo, id.var = 'Size', variable.name = "Type", value.name = "Probability")

ggSizeRepo <- ggplot(data = sizeRepo2, aes(x = Size, y = Probability, color = Type)) + geom_line(size = 1.5) +
		theme_minimal()
print(ggSizeRepo)


