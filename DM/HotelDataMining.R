#install.packages("mongolite")
library(mongolite)
library(ggplot2)
mongo = mongo(collection = "Booking", db = "bb102", url = "mongodb://10.120.27.11:27017",
      verbose = FALSE, options = ssl_options())

mongo$count(query = "{}") 
data1 = mongo$find(query = "{}", fields = "{\"_id\":0}", sort = "{}", skip = 0, limit = 124515, handler = NULL, pagesize = 1000)

str(data1)

data1$Price1Night = 4*  data1$Price


# plot 
UNI = data1$Price1Night[data1$ChiName == "京都四條烏丸UNIZO酒店"]
plot(UNI)
head(data1)

#ggplot
dataUNI = data1[data1$ChiName == "京都四條烏丸UNIZO酒店",]
g <- ggplot(dataUNI[1:5,],aes(x=CheckOut,y=Price1Night))
g + geom_col()
?geom_bar
#outliner
table(dataUNI$Price1Night)
length(dataUNI$Price1Night)

# lm ( Comment StarRate Score Price )


