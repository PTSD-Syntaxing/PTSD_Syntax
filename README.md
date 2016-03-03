# P-Text: NLP to identify PTSD

## Summary
#### The Problem
- 2.7 million veterans from OEF & OIF (as of Sep 2014)
- 20% suffer from PTSD
- 50% don't seek treatment

#### Our Work
We built a an nlp model that assesses the probability of PTSD in a suspected victim based on language gathered from correspondence and social media posts. Potential applications include:
- Families - Helping veteran families gauge depth of loved one's condition and provide them with the appropriate tools to help (implemented)
- Hotline triage - Crisis hotline prioritization based on assessed severity of caller's condition
- Veteran clinicians - Gentler questionnaires to guide veteran reintegration without forcing them to relive traumatic experiences

## The Data
We scraped posts from a variety of forums and social media sources, the most prominent of which was Reddit. Conversations from PTSD threads were labeled as PTSD-positive and conversations from threads of people telling painful stories were labeled as PTSD-negative.

## The Model
We tokenized and lemmatized the corpus in addition to removing stop words and key PTSD-giveaways (like the word "PTSD"). We then vectorized the data using a simple bag of words. The Naive Bayes Classifier performed best, outclassing the random forest classifier, adaboost classifier (XGBoost) in accuracy based on the five fold cross validation. We tried an SVC, but the train time proved prohibitively long given the size high dimensionality of the dataset.


## Next Steps
- Improve dataset - Collaborate with Johns Hopkins researchers to procure larger and more rigorously labeled dataset
- Improve model - Optimize model for precision and gridsearch broader variety of parameters
- Broaden application - Expand diagnostics to other key veteran injuries sucgh as Traumatic Brain Injury and depression
- Implement in use case - Work with Department of Veterans' Affairs to deploy model
