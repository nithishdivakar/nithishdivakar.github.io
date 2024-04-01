---
title: Notes on NLP and Transformers
layout: post
tags: [nlp]
date: 2024-04-01T07:50:00+05:30
start_date: 2024-04-01T07:50:00+05:30
draft: true
---


[Course Link](https://huggingface.co/learn/nlp-course/chapter1/4?fw=pt)


Causal language modelling
- Predicting next word
- Output depends on past and present inputs but not future ones

Masked Language modelling
- predict Masked word in a sentence

model Sizes
- GPT-1 : 110M 
- GPT-2 : 1.5B 
- T5: 11B
- BERT : 340M
- BART : 400M 


Base Model -> Pretrained Language Model -> [Fine tuning] -> fine Tuned Language Model

## Encoder and Decoder
+ In the encoder, the attention layers can use all the words in a sentence (since, as we just saw, the translation of a given word can be dependent on what is after as well as before it in the sentence). 
+ The decoder, however, works sequentially and can only pay attention to the words in the sentence that it has already translated (so, only the words before the word currently being generated). 

**Masking**
To speed things up during training (when the model has access to target sentences), the decoder is fed the whole target, but it is not allowed to use future words (if it had access to the word at position 2 when trying to predict the word at position 2, the problem would not be very hard!). For instance, when trying to predict the fourth word, the attention layer will only have access to the words in positions 1 to 3.

**types of models**

- Encoder-only models: 
    - Good for tasks that require understanding of the input, such as sentence classification and named entity recognition. 
    - Have bi-directional attention.
    - Pre-Training: Somhow corrupt a sentence and training the model to reconstruct original sentence. Ex: Maked Language Model 
    - Best suited for task requiring full sentence understanding. NER, Sentence Classification, QA etc.
    - Ex: BERT, RoBERTa
- Decoder-only models: 
    - Good for generative tasks such as text generation.
    - Auto-Regressive models. Can only access words past words from a given position. 
    - Pre-training: predict next word in the sentence.
    - Ex: GPT, GPT-2
- Encoder-decoder models or sequence-to-sequence models: 
    - Good for generative tasks that require an input, such as translation or summarization or generative question answering.
    - Pre-Training : Mix of both encoder only and decoder only objective. 
    - Ex: BART, T5

- [?] How is decoder only model trained with out encoder? Is the input only tokenised and the word embeddings feed to decoder? how does this fit into transformer architecture
