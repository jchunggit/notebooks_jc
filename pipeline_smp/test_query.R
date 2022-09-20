#install.packages("RPostgreSQL")

require(RPostgreSQL)

dsn_database = "<db>"   # specify db
dsn_hostname = "<host>" # specify host name
dsn_port = "<port>" # specify port
dsn_uid = "<username>" # specify username
dsn_pwd = "<pwd>" # specify password

tryCatch({
  drv <- dbDriver("PostgreSQL")
  print("Connecting to PostgreSQL database")
  connec <- dbConnect(drv, 
                      dbname = dsn_database,
                      host = dsn_hostname, 
                      port = dsn_port,
                      user = dsn_uid, 
                      password = dsn_pwd)
  print("Connected to PostgreSQL database!")
},
error=function(cond) {
  print("Unable to connect.")
})

df <- dbGetQuery(connec, "SELECT * FROM <schema>.<table>")
df