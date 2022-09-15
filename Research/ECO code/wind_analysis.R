require("here")
require(ggplot2)
require(dplyr)

data_dir
df = read.csv(file.path("data", "data_Wind.csv"), sep=",")
head(df)

df2 = df[!(is.na(df$condition) | !(df$variable == "score")),]

df_trade =df[!(is.na(df$condition) | !(df$variable == "traded")),]
head(df_trade)

df2 = df2[c("subID", "value", "condition", "orderSeen")]

df_percent = df_trade[c("subID", "event", "value", "variable", "condition")]

head(df_percent)
head(df2)

tx = aggregate(orderSeen ~ subID + condition, data = df2, FUN = max, na.rm = TRUE)

tx_u = unique(tx$orderSeen, fromLast = F)

tx_u

df_detm = df2[(df2$condition == "detm"),]


df_detm

df_prob = df2[(df2$condition == "prob"),]

final = df_detm[(df_detm$orderSeen == 72| df_detm$orderSeen == 140| df_detm$orderSeen == 67| df_detm$orderSeen == 135),]


final2 = df_prob[(df_prob$orderSeen == 72| df_prob$orderSeen == 140| df_prob$orderSeen == 67| df_prob$orderSeen == 135),]


final
final2

merged_final = merge(x = final, y = final2, by = "subID")

merged_final

merged_final$difference = as.numeric(merged_final$value.y) - as.numeric(merged_final$value.x)

merged_final

diff_count = merged_final %>% 
  count(difference)

diff_count$TF <- ifelse(diff_count$difference>=0, 1, 0)

df_percent$value<-as.numeric(as.character(df_percent$value))

df_percent$TF <- ifelse((df_percent$event== "event" & df_percent$value == 50 | df_percent$event== "noEvent" & df_percent$value == 100), 1, 0)

head(df_percent)

df_percent %>% 
  count(condition) %>% 
  mutate(perc = TF / nrow(value)) -> tips2

detmc = sum(df_percent$condition == "detm" & df_percent$TF == 1)/ sum(df_percent$condition == "detm")
probc = sum(df_percent$condition == "prob" & df_percent$TF == 1) / sum(df_percent$condition == "prob")

condition <- c("detm", "prob")
percent <- c(detmc, probc)

df_stat <- data.frame(condition, percent)

df_stat

ggplot(df_stat, aes(x = condition, y = percent, fill=condition)) + geom_bar(stat = "identity") +ggtitle("Proportion of correct decisions based on deterministic vs. probabilistic forecasts") + 
  xlab("Forecast") + ylab("Proportion of Correct Decisions") + scale_y_continuous(labels = scales::percent, limits = c(0, 0.95))


ggplot(diff_count, aes(x=difference, y=n, fill=TF)) +
  geom_bar(stat="identity", position="dodge") +
  theme(axis.text.x = element_text(angle = 90)) + ggtitle("Forecast") + xlab("Balance Difference in Monetary Units") + ylab("Number of Participants")+
  xlim(-40000, 30000) + ylim(0, 10)

df_append= rbind(final, final2)

df_append

df_append = df_append %>% arrange(as.numeric(value))

df_append$value<-as.numeric(as.character(df_append$value))

ggplot(df_append, aes(x = condition, y = value) ) + geom_boxplot(aes(fill = condition))


df_append %>% 
  count(value)

det = final %>%
  count(value)

prob = final2 %>%
  count(value)

prob

det

prob$value<-as.numeric(as.character(prob$value))
det$value<-as.numeric(as.character(det$value))

prob$condition = "prob"
det$condition = "det"

full <- rbind(prob, det)

full
full$value<-as.numeric(as.character(full$value))
full$n<-as.numeric(as.character(full$n))

full

ggplot(full, aes(x=value, y=n, fill=condition)) +
  geom_bar(stat="identity", position="dodge") +
  theme(axis.text.x = element_text(angle = 90)) + ggtitle("Forecast") + xlab("Final Balance in Monetary Units") + ylab("Number of Participants")+
  xlim(-10000, 50000) + ylim(0, 12.5)

ggplot(mapping=aes(x=prob$value))+
  geom_bar(data=prob, aes(x=prob$value-0.1), fill="red", binwidth=0.1)+
  geom_bar(data=det, fill="blue", binwidth=0.1)

merged_pd = merge(x = prob, y = det, by = NULL)

ggplot(det, aes(x=value, y=n)) + 
  geom_bar(stat = "identity", fill = "red") 

ggplot(prob, aes(x=value, y=n)) + 
  geom_bar(stat = "identity", fill = "blue")



df_merged = merge(x = det, y = prob, by = "CustomerId", all = TRUE)

result <- df_detm %>% 
  group_by(username, value) %>%
  filter(value == max(value)) %>%
  arrange(username,value,condition)

result
df %>% 
  filter(df$value == max(y)) %>% # filter the data.frame to keep row where x is maximum
  select(x) # select column y

#Not looking for the max in this specific case
tx = aggregate(df_detm$value,list(df_detm$subID),max)

df_list = unique(df2$subID, fromLast=F)

df_list

for(val in df_list){
  for(val2 in df2){
    if(val == val2){
      if(df2$condition == "detm"){
        if(df2$orderSeen > orderSeenVal){
          orderSeenVal == which(df$orderSeen==count, arr.ind=TRUE)
        }
      }
      else{
        if(df2$orderSeen > orderSeenVal){
          orderSeenVal == 
        }
      }
    }
  }
}


df2["value"] = as.numeric(unlist(df2["value"]))

df3 = aggregate(.~username + condition, data = df2, FUN=sum)

count = 0

ggplot(df, aes(x = condition, y = value) ) + geom_boxplot(aes(fill = condition))
