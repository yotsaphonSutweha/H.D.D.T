# Explore CLeaveland data to be used with the Diagnostic tool

getwd()

setwd(dir = '~/Documents/Year4/Software Project/Data Exploration/HeartDiseaseData')

getwd()

# Data descritpions
# age - age in years "Numerical data"
# sex - sex (1 = male, 0 = female) "Categorical data"
# cp - chest pain type: 1 - typical angina, 2 - atypical angina, 3 - non-anginal pain, 4 - asymptomatic "Categorical data"
# trestbps - resting blood pressure (in mm Hg on admission to the hospital) "Numerical data"
# chol - serum cholestoral in mg/dl "Numerical data"
# fbs - fasting blood sugar > 120 mg/dl (1 = true, 0 = false) "Categorical data" 
# restecg - resting electrocardiographic results: 0 - normal, 1 - having ST-T wave abnormality (T wave inversions and/or ST elevation or depression of > 0.05 mV)
# 2 - showing probable or definite left ventricular hypertrophy by Estes' criteria "Categorical data" 
# thalach - maximum heart rate achieved "Numerical data"
# exang - exercise induced angina (1 = yes; 0 = no) "Categorical data" 
# oldpeak - ST depression induced by exercise relative to rest "Numerical data"
# slope - the slope of the peak exercise ST segment: 1 - upsloping, 2 - flat, 3 - downsloping "Categorical data" 
# ca - number of major vessels (0-3) colored by flourosopy "Numerical data"
# thal - 3 = normal; 6 = fixed defect; 7 = reversable defect "Categorical data" 
# diagnosis - diagnosis of heart disease (angiographic disease status) "Categorical data" 0 = non-diagnosed 1-4 = diagnosed 
# -- Value 0: < 50% diameter narrowing
# -- Value 1: > 50% diameter narrowing
# (in any major vessel: attributes 59 through 68 are vessels)

data = read.csv(file = 'processed.cleveland.data', header = TRUE)

?read.csv()

class(data)
# Put in the headers for inside the dataset 
?colnames

colnames(data) = c('age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'diagnosis')

head(data)

tail(data)

names(data)

class(data)

typeof(data)

# Ge the summary of each att - ca and thal has missing values
summary(data)

# Deal with missing values in ca and thal comlumn, replace them with -9. Also Convert ca to numeric
ca = data$ca
thal = data$ca

ca
ca = as.numeric(as.character(ca)) # Convert factor to numeric
ca
class(ca)
typeof(ca)
ca[is.na(ca)] = -9
ca
data$ca = as.factor(ca)

thal
class(thal)
typeof(thal)
thal = as.numeric(as.character(thal))
thal
thal[is.na(thal)] = -9
thal
data$thal = as.factor(thal)

summary(data)

class(data$ca)
typeof(data$ca)

class(data$thal)
typeof(data$thal)


#----------------------------------

hist(data$age)
?hist

# Visualise data
library(ggplot2)

ggplot(data, aes(x = age)) +
  geom_histogram()
  +  theme_bw()


ggplot(data, aes(x = diagnosis)) +
  geom_bar()
+  theme_bw()

ggplot(data, aes(x = age, y = chol)) + geom_point()

ggplot(data, aes(x = aex)) + geom_bar()

#---------------------------------



str(data)
dim(data)

data$diagnosis

?write.csv
write.csv(data, "clevelandV2.csv")

pData = read.csv(file = 'clevelandV2.csv', header = TRUE)
str(pData)
head(pData)

# pData$predict = pData$diagnosis
# pData$predict[pData$predict == 2] = 1
# pData$predict[pData$predict == 3] = 1
# pData$predict[pData$predict == 4] = 1

pData$diagnosis = pData$diagnosis
pData$diagnosis[pData$diagnosis == 2] = 1
pData$diagnosis[pData$diagnosis == 3] = 1
pData$diagnosis[pData$diagnosis == 4] = 1
str(pData$diagnosis)
summary(pData$diagnosis)
pData$X = NULL
table(pData$diagnosis)
pData[1]


write.csv(pData, "clevelandV4.csv")


data2 = read.csv(file = 'processed.hungarian.data', header = FALSE)
head(data2)
colnames(data2) = c('age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'diagnosis')
summary(data2)

chol = data2$chol
fbs = data2$fbs
restecg = data2$restecg
exang = data2$exang
slope = data2$slope
ca = data2$ca
thal = data2$thal

ca
ca = as.numeric(as.character(ca)) # Convert factor to numeric
ca
class(ca)
typeof(ca)
ca[is.na(ca)] = -9
ca
data2$ca = as.factor(ca)

thal
class(thal)
typeof(thal)
thal = as.numeric(as.character(thal))
thal
thal[is.na(thal)] = -9
thal
data2$thal = as.factor(thal)


chol = as.numeric(as.character(chol)) # Convert factor to numeric
chol[is.na(chol)] = -9
data2$chol = as.factor(chol)


fbs = as.numeric(as.character(fbs)) # Convert factor to numeric
fbs[is.na(fbs)] = -9
data2$fbs = as.factor(fbs)

restecg = as.numeric(as.character(restecg)) # Convert factor to numeric
restecg[is.na(restecg)] = -9
data2$restecg = as.factor(restecg)

exang = as.numeric(as.character(exang)) # Convert factor to numeric
exang[is.na(exang)] = -9
data2$exang = as.factor(exang)

slope = as.numeric(as.character(slope)) # Convert factor to numeric
slope[is.na(slope)] = -9
data2$slope = as.factor(slope)

summary(data2)

write.csv(data2, "hungarianDataV1.csv")


cleavelandV4 = read.csv(file = 'clevelandV4.csv', header = TRUE)
tail(cleavelandV4)
hungarian = read.csv(file = 'hungarianDataV1.csv', header = TRUE)
tail(hungarian)

combined = merge(cleavelandV4, hungarian, by=c('age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'diagnosis'),all.x=T)
summary(combined)
tail(combined)