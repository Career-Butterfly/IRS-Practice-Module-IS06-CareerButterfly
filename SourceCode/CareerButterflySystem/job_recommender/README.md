### Job Recommender 

This service helps to recommend 5 most relevant jobs using a weighted average score based on `cosine similarity score between user's resume and job description`, `company reviews and rating score`, and `user priority score` (e.g. work life balance mean score from company reviews).

The weighted average score is calculated using the following formula:

$$Weighted Average Score = \frac{(W_1 \times S_1) + (W_2 \times S_2) + (W_3 \times S_3)}{(W_1 \times E_1) + (W_2 \times E_2)+ (W_3 \times E_3)}$$

where:

* $S_1$ = `Cosine similarity score between user's resume and job description`
* $S_2$ = `Company reviews and rating score`
* $S_3$ = `User priority score`
* $W_1$, $W_2$, $W_3$ = Weights (all set to 1/3)
* $E_1$ = `When cosine similarity score exist` (represents existence of S1, 1 if exists, 0 otherwise)
* $E_2$ = `When company reviews and rating score exist` (represents existence of S2, 1 if exists, 0 otherwise)
* $E_3$ = `When user priority score exist` (represents existence of S3, 1 if exists, 0 otherwise)
