Persian NLP
------------

A project for processing persian texts

+cleaning initial corpus
+ Normalizing
+ Half space correction in Persian text
+ Word and sentence tokenizer (splitting words and sentences)
+ stemming
+ clustering 
+ Topic modeling

##requirements

+ [NLTK](http://nltk.org/) compatible
+ Python 2.7 support
+ libwapiti>=0.2.1 (if speed is an important factor)
+ nltk>=3.2.2


##discription 
1.PreProcess
 it is a package for preprocessing the given dataset before performing furthur NLP tasks. 
 
2.Initial_Analytics 
  It is a initial evaluation of the corpus which depicts a worldcloud presenting the most imporant words in the dataset
  
3.cleaning
  This function finds the most similar texts using Kmeans algorithm and then stores texts that beglong to the same cluster in the same folder(Clustering-Output)
  The nuumber of clusters is taken as an input, but hierarchical Kmeans can remove the need for input (which causes higher complexity)

4.TopicModeling-LDA
  this uses generative models to build a number of topics to discover hidden semantic structures in the corpus. Then we can infer  the topics that every text is related to. 
