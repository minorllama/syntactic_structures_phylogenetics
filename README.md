# Syntactic structures and the general Markov models

Data and code for the article: 

Gakkhar, S., & Marcolli, M. (2021). [Syntactic structures and the general Markov models](https://arxiv.org/abs/2104.08462). arXiv preprint arXiv:2104.08462. 

which explores the consistency of data of syntactic structures with hypothesis about models of underlying evolution.

The initial analysis can be run with: 

    syntactic_structures_phylogenetics/evomarkov$ ./phylotrees3.sh 


In `evomarkov`, the following command does the subsampling analysis
    
    python trees.py <langfamily> -v -explore -skbio

For the romance family likelihood analyis, use 

    python  maxlikelihood.py  -log -tag:run1 -rom      

`-log` indicates using log likelihood for optimization

See the individual scripts for options available. 


The following packages will be required: 

    biopython 1.79    
    dendropy  4.4.0 
    numpy 1.20.3 
    pandas 1.3.4        
    scikit-bio 0.5.6         
    scipy 1.7.1

The raw syntactic structures data is available [here](evomarkov/raw). 



