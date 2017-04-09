install.packages("RPostgreSQL")

require(RPostgreSQL)

pw <- {
  "dbpass"
}

# loads the PostgreSQL driver
drv <- dbDriver("PostgreSQL")
# creates a connection to the postgres database
# note that "con" will be used later in each connection to the database
con <- dbConnect(drv, dbname = "mexican_politics",
                 host = "192.168.1.6", port = 5432,
                 user = "presdb", password = pw)
rm(pw) # removes the password


df_comments<- dbGetQuery(con, "SELECT * from vid_comments")

df_comments <- df_comments[! duplicated(df_comments$content) ,]

summary(df_comments$pubdate)
length(unique(df_comments$youid))
