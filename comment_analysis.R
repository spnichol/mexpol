

require(RPostgreSQL)

pw <- {
  "dbpass"
}

drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname = "mexican_politics",
                 host = "192.168.1.6", port = 5432,
                 user = "presdb", password = pw)


df_comments<- dbGetQuery(con, "SELECT * from vid_comments")
df_vids <- dbGetQuery(con, "SELECT * FROM vid_list")
df_vids <- df_vids[! duplicated(df_vids$youid) ,]



df_comments <- df_comments[! duplicated(df_comments$content) ,]
df_comments<- gsub("[[:punct:]]", " ", df_comments)  # replace punctuation with space

library(quanteda)
df_combo <- merge(df_comments, df_vids, by="youid", all.x=TRUE)
df_combo$query <- ifelse(df_combo$query == "pena nieto", "EPN", "AMLO")
#df_comments$content <- gsub()
df_combo$content <- tolower(df_combo$content)
all_comms <- corpus(df_combo$content, docnames=df_combo$youid, docvars=data.frame(youid = df_combo$youid, query=df_combo$query))

usa <- c("estados unidos", "eau", "gringo", "gringolandia", "norte", "eeuu")
kwic(all_comms, usa, window=2)


comms.dfm <- dfm(tokenize(all_comms, removePunct=TRUE), remove=stopwords("spanish"))

topfeatures(comms.dfm)


nrc <- get_sentiments("nrc")
#tokenize at word level 
tidy_news <- precorpus %>%
  unnest_tokens(word, text)
tidy_news$Text <- NULL
#remove stopworks 
data("stop_words")
cleaned_trump <- tidy_news %>%
  anti_join(stop_words)

#add sentiments
nrc <- get_sentiments("nrc")
bing <- get_sentiments("bing")
trump_sentiment <- get_sentiment(cleaned_trump$word, method="bing")
cleaned_trump$score <- get_sentiment(cleaned_trump$word, method="bing")
summary(trump_sentiment)
cleaned_trump %>%
  join(nrc) %>%
  count(word, sort=TRUE)

