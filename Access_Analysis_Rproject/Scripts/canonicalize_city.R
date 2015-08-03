library(stringi)

#data <- read.csv("../data/UW_Trip_Data_18mo_QC_b.csv", stringsAsFactors=FALSE)
comm_df <- read.csv("../data/communities.csv", stringsAsFactors=FALSE)
comm_df$replace_str <- tolower(paste(comm_df$neighborhoods,comm_df$places,
                                     comm_df$misspellings,sep=";"))
comm_df$replace <- stri_split(comm_df$replace_str, fixed=";")
city_replacements <- list()
for(i in seq(1,nrow(comm_df))) {
    replacements <- comm_df$replace[[i]]
    for(r in replacements) {
        if(r == "") next
        # make sure replacement is in expected format
        stopifnot(grepl("^[a-z][a-z -/]*[a-z]$", r))
        # make sure we don't have any clashes
        stopifnot(!(r %in% city_replacements))
        # construct the dictionary
        city_replacements[[r]] <- tolower(comm_df[i, "name"])
    }
}
# these strings can't be matched to a known community name
unrecognizable <- c("s", "city")
for(ustr in unrecognizable) city_replacements[[ustr]] <- ""
city_replacements <- unlist(city_replacements)


city1 <- data[,16]
u_city1 <- sort(unique(tolower(stri_trim_both(city1))))

city2 <- tolower(as.character(city1))
# trim ends of string of anything that isn't a letter
city2 <- stri_trim_both(city2, pattern="[a-z]")
# remove characters that are not a letter, space, hyphen, or slash
city2 <- gsub("[^a-z -/]", "", city2)
# remove extra spaces
city2 <- gsub(" +", " ", city2)
mask <- city2 %in% names(city_replacements)
city2[mask] <- city_replacements[city2[mask]]
# city2 now has the cleaned city names

u_city2 <- sort(unique(city2))
if(!all(u_city2 %in% c("",comm_df$name))) {
  stop("There are still unaccounted for city names")
}

data$city<-city2