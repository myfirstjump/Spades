rm(list=ls())
# install.packages("jiebaR")
library(mongolite)
library("jiebaR")

mongo = mongo(collection = "ptt_article", db = "text_mining", url = "mongodb://10.120.27.11:27017",
              verbose = FALSE, options = ssl_options())

mongo$count(query = "{}") 
PTT = mongo$find(query = "{}", fields = "{\"_id\":0}", sort = "{}", skip = 0, limit = 5, handler = NULL, pagesize = 1000)
search()

wk = worker()
wk["我是《R的极客理想》图书作者"]
str(PTT[1,5])
wk[PTT[3,5]]

