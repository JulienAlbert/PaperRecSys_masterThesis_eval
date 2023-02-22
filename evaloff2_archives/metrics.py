import numpy as np
import networkx as nx

# source : http://sdsawtelle.github.io/blog/output/mean-average-precision-MAP-for-recommender-systems.html

def is_relevant(item, items):
    """Return 1 if item in items, 0 if not."""
    return int(item in items)

def precision_k(rec_items, actual_items, k):
    """Compute the precision at k.

    Keyword_arguments:
    rec_items -- list of recommended items
    actual_items -- set of actual items
    k -- int limit (k > 0)
    """
    assert k > 0
    assert isinstance(rec_items, list)
    assert isinstance(actual_items, set)
    assert len(rec_items) >= k
    
    actual_rec_items = [item for item in rec_items[:k] if is_relevant(item, actual_items)]

    return len(actual_rec_items) / k

def avg_precision_k(rec_items, actual_items, k):
    """Compute the average precision at k.

    Keyword_arguments:
    rec_items -- list of recommended items
    actual_items -- set of actual items
    k -- int limit (k > 0)
    """
    assert k > 0
    assert isinstance(rec_items, list)
    assert isinstance(actual_items, set)
    assert len(rec_items) >= k

    m = min(len(actual_items), k)

    values = [precision_k(rec_items, actual_items, i+1) * is_relevant(rec_items[i], actual_items) for i in range(k)] 

    return sum(values) / m

def mean_avg_precision_k(rec_items_list, actual_items_list, k):
    """Compute the mean average precision at k.

    Keyword_arguments:
    rec_items_list -- list of lists of recommended items
    actual_items_list -- list of sets of actual items
    k -- int limit (k > 0)
    """
    assert len(rec_items_list) == len(actual_items_list)
    assert isinstance(rec_items_list, list)
    assert isinstance(actual_items_list, list)
    assert k > 0    
    
    values = [avg_precision_k(rec_items, actual_items, k) for rec_items, actual_items in zip(rec_items_list, actual_items_list)]

    return sum(values) / len(rec_items_list)

def recall_k(rec_items, actual_items, k):
    """Compute the recall at k.

    Keyword_arguments:
    rec_items -- list of recommended items
    actual_items -- set of actual items
    k -- int limit (k > 0)
    """
    assert k > 0
    assert isinstance(rec_items, list)
    assert isinstance(actual_items, set)
    assert len(rec_items) >= k

    actual_rec_items = [item for item in rec_items[:k] if item in actual_items]

    return len(actual_rec_items) / len(actual_items)

def mean_recall_k(rec_items_list, actual_items_list, k):
    """Compute the mean recall at k.
    
    Keyword_arguments:
    rec_items -- list of recommended items
    actual_items -- set of actual items
    k -- int limit (k > 0)
    """
    assert len(rec_items_list) == len(actual_items_list)
    assert isinstance(rec_items_list, list)
    assert isinstance(actual_items_list, list)
    assert k > 0
    
    values = [recall_k(rec_items, actual_items, k) for rec_items, actual_items in zip(rec_items_list, actual_items_list)]

    return sum(values) / len(rec_items_list)

def reciprocal_rank(rec_items, actual_items):
    """Compute the reciprocal rank.

    Keyword_arguments:
    rec_items -- list of recommended items
    actual_items -- set of actual items
    """
    assert isinstance(rec_items, list)
    assert isinstance(actual_items, set)
    
    for pos, item in enumerate(rec_items):
        if item in actual_items:
            return 1 / (pos+1)

    return 1 / len(rec_items)

def mean_reciprocal_rank(rec_items_list, actual_items_list):
    """Compute the mean reciprocal rank.

    Keyword_arguments:
    rec_items_list -- list of lists of recommended items
    actual_items_list -- list of sets of actual items
    """
    assert len(rec_items_list) == len(actual_items_list)
    assert isinstance(rec_items_list, list)
    assert isinstance(actual_items_list, list)
    
    scores = [reciprocal_rank(rec_items, actual_items) for rec_items, actual_items in zip(rec_items_list, actual_items_list)]

    return sum(scores) / len(rec_items_list)

def item_coverage(rec_items_list, items_set):
    """Compute the item coverage.

    Keyword_arguments:
    rec_items_list -- list of lists of recommended items
    items_set -- set of recommendable items
    """
    rec_items_set = set()
    for rec_items in rec_items_list:
        for item in rec_items:
            rec_items_set.add(item)

    return len(rec_items_set) / len(items_set)

def item_similarity(item1, item2):
    """Compute similarity index between item1 and item2."""
    return 0.5

def dissimilarity_infra_list(rec_items):
    """Compute average dissimilarity between items in rec_items."""
    scores = []
    for item1 in rec_items:
        for item2 in rec_items:
            if item1 != item2:
                scores.append(item_similarity(item1, item2))
    return 1 / np.mean(scores)

def mean_dissimilarity_infra_list(rec_items_list):
    """Compute mean of average dissimilarities of lists of items."""
    scores = [dissimilarity_infra_list(rec_items) for rec_items in rec_items_list]

    return np.mean(scores)

def user_similarity(item, user):
    """Computer similarity between item and user."""
    return 0.5

def dissimilarity_with_user(rec_items, user):
    """Compute average dissimilarity between items in rec_items and user."""
    scores = [user_similarity(item, user) for item in rec_items]

    return 1 / np.mean(scores)

def mean_dissimilarity_with_user(rec_items_list, users):
    """Compute mean of average dissimilarities of lists of items."""
    scores = [dissimilarity_with_user(rec_items, user) for rec_items, user in zip(rec_items_list, users)]
    
    return np.mean(scores)

def item_popularity(item):
    """Compute item popularity."""
    return item['citation_count']

def average_inverse_popularity(rec_items):
    """Compute average inverse popularity of items in rec_items"""
    scores = [item_popularity(item) for item in rec_items]

    return 1 / np.mean(scores)

def mean_average_inverse_popularity(rec_items_list):
    """Compute mean of average inverse popularities of lists of items in rec_items_list."""
    scores = [average_inverse_popularity(rec_items) for rec_items in rec_items_list]
    
    return np.mean(scores)

def avg_shortest_path_length(G, rec_items):
    """Compute average shortest parth between items in rec_items.
    
    Keyword_arguments:
    G -- citation undirected graph
    rec_items -- list of recommended items
    """
    lengths = 0
    nb_errors = 0
    for item1 in rec_items:
        for item2 in rec_items:
            if item1 != item2:
                try:
                    lengths += nx.shortest_path_length(G, source=item1, target=item2)

    return np.mean(lengths)

def mean_avg_shortest_path_length(G, rec_items_list):
    """Compute mean of average shortest path length for lists of items in rec_items_list.
    
    Keyword_arguments:
    G -- citation directed graph
    rec_items_list -- list of lists of recommended items
    """
    undirected_G = G.to_undirected()    
    scores = [avg_shortest_path_length(undirected_G, rec_items) for rec_items in rec_items_list]

    return np.mean(scores)
