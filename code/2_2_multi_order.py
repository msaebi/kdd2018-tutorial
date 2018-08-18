#%%
import markdown
from IPython.core.display import display, HTML
def md(str):
    display(HTML(markdown.markdown(str + "<br />")))

#%%
md("""
# Higher-Order Data Analytics for Temporal Network Data


## 2.2 Multi-Order Representation Learning

**Ingo Scholtes**  
Data Analytics Group  
Department of Informatics (IfI)  
University of Zurich  


**August 22 2018**
""")

#%%
md("""
## Detecting higher-order correlations

So far, we have studied higher-order network models for path data with a fixed, given order $k$. We have also seen that such higher-order models can yield better predictions compared to standard network models. But there are also a number of open questions, namely: 

1.) When do we need higher-order network models, and when are standard (first-order) models enough? 
2.) What is the optimal higher order to model a given data set? 
3.) Given that a model with order $k$ can only capture correlations in paths at a single fixed length $k$, how can we combine models with multiple higher orders into a multi-order model?

In this session, we will answer these questions. Let us again start with our simple toy example:

<span style="color:red">**TODO:** Import the package `pathpy` and rename it to `pp`. Create a new instance `p` of class `Paths` and add two paths $a \rightarrow c \rightarrow d$ and $b \rightarrow c \rightarrow e$, each occurring twice.</span>
""")

#%% In [2]


#%%
md("""
In session 1 we have seen that in this example we only observe two of four paths of length two that would be possible in the null model. Hence, this is a simple example for path statistics that exhibit correlations that warrant a second-order model. 

But how can we decide this in a principled and statistically sound way? We must take a statistical inference perspective on the problem. We can first use the (weighted) first-order network model to construct the transition matrix for a Markov chain model for paths in a network. We simply use the relative frequencies of edges to proportionally scale the probabilities of edges. 

<span style="color:red">**TODO:** Generate a first-order model of `toy_paths` and print the transition matrix of the model.</span>
""")

#%% In [3]


#%%
md("""
In fact, we can see this transition matrix as a (first-order) probabilistic generative model for paths in the underlying network topology. This probabilistic view allows us to calculate a likelihood of the first-order model, given the paths that we have observed. With `pathpy`, we can directly calculate the likelihood of higher-order models.

<span style="color:red">**TODO:** Use the `HigherOrderNetwork.likelihood` method to calculate the likelihood of the first-order model, given `toy_paths`.</span>
""")

#%% In [4]


#%%
md("""
This result is particularly easy to understand for our toy example. Each path of length two corresponds to two transitions in the transition matrix of our Markov chain model. For each of the four paths of length two in `toy_paths`, the first transition is deterministic because nodes $a$ and $b$ only point to node $c$. However, based on the network topology, for the second step we have a choice between nodes $d$ and $e$. Considering that we see as many transitions through edge $(c,d)$ as we see through edge $(c,e)$, in a first-order model we have no reason to prefer one over the other, so each has probability $0.5$.

Hence, for each of the ten observed paths we obtain a likelihood of $1 \cdot 0.5 = 0.5$, which yields a total likelihood for our (independent) observations of $0.5^{4} = 0.0625$.
""")

#%%
md("""
Let us compare this to the likelihood of a second-order model for our paths.

<span style="color:red">**TODO:** Generate a second-order model for `toy_paths` and print the transition matrix. Use the `HigherOrderNetwork.likelihood` method to calculate the likelihood of a second-order model, given `toy_paths`.</span>
""")

#%% In [7]


#%%
md("""
Here, the likelihood assumes its maximal value of $1.0$ because all transitions in the second-order model are deterministic, i.e. we simply multiply $1 \cdot 1$.

Let us have a look at the second-order null model, which is actually a first-order model represented in the second-order space.

<span style="color:red">**TODO:** Generate a second-order null model for `toy_paths` and print the transition matrix. Use the `HigherOrderNetwork.likelihood` method to calculate the likelihood of this model, given `toy_paths`.</span>
""")

#%% In [8]


#%%
md("""
This confirms our expectation that the second-order null model actually has the same likelihood as the first-order model. It also highlights an interesting way to test hypotheses about higher-order correlations. We can use a likelihgood ratio test to compare the likelihood of the null hypothesis (i.e. a second-order representation of the first-order model) with the likelihood of our alternative hypothesis (the actual *fitted* second-order model).

This test requires us to additionally compare the degrees of freedom (or complexity) of the two models. With this, we automatically account for Occam's razor, which states that we should favor models that make fewer assumptions. Moreover, in our case we have, by definition, the case of a nested model, where the null model is a special point in the parameter space of the general higher-order models. 

This implies that we can use Wilk's theorem to analytically calculate a p-value for the null hypothesis that second-order correlations are absent (i.e. a first-order model is sufficient to explain the observed paths), compared to the alternative hypothesis that a second-order model is needed. You can find the mathematical details of this hypothesis testing technique in:

I Scholtes: [When is a Network a Network? Multi-Order Graphical Model Selection in Pathways and Temporal Networks](http://dl.acm.org/citation.cfm?id=3098145), In KDD'17 - Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, Halifax, Nova Scotia, Canada, August 13-17, 2017

Let us apply a likelihood ratio test to our example. We only have to calculate the degrees of freedom and then calculate the test statistic for the likelihood ratio test. Using Wilk's theorem, we then calculate a p-value based on the CDF of the chi-square distribution (see in paper above).

<span style="color:red">**TODO:** Perform the likelihood ratio test for the null hypothesis that the observed paths can be explained by a first-order model. Use the function `HigherOrderNetwork.degrees_of_freedom` to calculate the degrees of freedom of a k-th order model. Use `chi2.cdf` from `scipy.stats` to calculate the p-value.</span>
""")

#%% In [9]


#%%
md("""
In our example, the p-value of the null hypothesis that we can explain those four paths based on the network topology alone is (borderline) 0.019. This is intuitive, as we have only observed four paths, which is hardly enough to robustly reject the null model. Let's see what happens if we observe those same paths more often.

<span style="color:red">**TODO:** Use the arithmetic operators defined on `Paths` to multiply all observation counts with two. Repeat the likelihood ratio test and output the new p-value.</span>
""")

#%% In [10]


#%%
md("""
We can now reject the null hypothesis, as it is very unlikely to not observe two out of four paths a single time in eight observations. Increasing the number of observations of the two paths naturally decreases the p-value, which tells us that we need a second-order model to explain the path statistics in our toy model.
""")

#%%
md("""
## Multi-order graphical model learning
""")

#%%
md("""
Unofortunately, our toy is too simple in multiple ways: First, it only contains correlations at a single length two, thus justifying a second-order model. Real data are likely to exhibit multiple correlation lengths at the same time. 

Even more importantly, in more realistic examples the model selection will actually not work as described above. The reason is that we cannnot directly compare likelihoods of models with different order, as they are nto calculated on the same 

That becomes clear in the following simple example path.

<span style="color:red">**TODO:** Create an empty `Paths` instance and add the following path:</span>

`('a','b','c','d','e','c','b','a','c','d','e','c','e','d','c','a')`

<span style="color:red">Generate a first-order model, as well as a second- and third-order null model. Plot the first-order model and compare the likelihoods between the three models.</span>
""")

#%% In [12]


#%%
md("""
This is strange! Shouldn't these three models be identical? In fact, they are not identical and this turns out to be a major issue in the modelling of sequence data that consist of large numbers of short sequences: in terms of the number of transitions entering the likelihood calculation, a model of order $k$ discards the first $k$ nodes on the path. That is, a second-order model can necessarily only account for all but the first edge traversals on the path. This means that we compare likelihoods that are computed for different sample spaces, which is not meaningful! 

<span style="color:red">**TODO:** Calculate the number of transitions involved in the likelihood calculation of each model.</span>
""")

#%% In [13]


#%%
md("""
I Scholtes: [When is a Network a Network? Multi-Order Graphical Model Selection in Pathways and Temporal Networks](http://dl.acm.org/citation.cfm?id=3098145), In KDD'17 - Proceedings of the 23rd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, Halifax, Nova Scotia, Canada, August 13-17, 2017

<span style="color:red">**TODO:** Create an instance of class `MultiOrderModel` and fit it to the path in the example from above. Use the method `pp.visualisation.plot` to visualise the entries of `MultiOrderModel.layers` for the the resulting instance.</span>
""")

#%% In [16]


#%%
md("""
<span style="color:red">**TODO:** Create an instance of class `MultiOrderModel` and fit it to `toy_paths`. Perform the ... .</span>
""")

#%% In [17]


#%%
md("""
<span style="color:red">**TODO:** Create an instance of class `MultiOrderModel` and fit it to `toy_paths`. Perform the ... .</span>
""")

#%% In [None]


#%%
md("""
<span style="color:red">**TODO:** Generate a ....</span>
""")

#%% In [None]


#%%
md("""
We can visualise and analyse the layers of a multi-order model as follows:
""")

#%% In [None]


#%%
md("""
<span style="color:red">**TODO:** Perform the order detection for the synthetic temporal network wirth cluster structures introduced in 2.1.</span>
""")

#%%
md("""
## Representation learning in real data sets

<span style="color:red">**TODO:** Apply the model selection algorithm to real pathway data. What orders do you observe?</span>
""")

#%% In [None]


#%% In [None]


#%% In [None]


#%% In [None]


#%% In [None]


#%% In [None]


#%% In [None]


