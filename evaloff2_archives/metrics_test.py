import metrics as m

actual_items = ['item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9']

rec_items = ['item0', 'item11', 'item2', 'item13', 'item4', 'item15', 'item6', 'item17', 'item18', 'item9']

def test_is_relevant_yes():
    assert m.is_relevant('item1', actual_items) == 1

def test_is_relevant_no():
    assert m.is_relevant('item10', actual_items) == 0

def test_precision_1():
    assert m.precision_k(['item0'], set(actual_items), 1) == 1

def test_precision_1_bis():
    assert m.precision_k(['item10'], set(actual_items), 1) == 0
    
def test_precision_3():
    assert m.precision_k(rec_items, set(actual_items), 3) == 2/3
    
def test_precision_5():
    assert m.precision_k(rec_items, set(actual_items), 5) == 3/5

def test_avg_precision_1():
    assert m.avg_precision_k(rec_items, set(actual_items), 1) == 1

def test_avg_precision_3():
    assert m.avg_precision_k(rec_items, set(actual_items), 3) == (1+2/3)/3

def test_avg_precision_5():
    assert m.avg_precision_k(rec_items, set(actual_items), 5) == (1+2/3+3/5)/5

def test_mean_avg_prevision_1():
    assert m.mean_avg_precision_k([rec_items, rec_items], [set(actual_items), set(actual_items)], 1)

def test_mean_avg_prevision_3():
    assert m.mean_avg_precision_k([rec_items, rec_items], [set(actual_items), set(actual_items)], 3) == (1+2/3)/3

def test_mean_avg_prevision_5():
    assert m.mean_avg_precision_k([rec_items, rec_items], [set(actual_items), set(actual_items)], 5) == (1+2/3+3/5)/5

def test_recall_1():
    assert m.recall_k(['item0'], set(actual_items), 1) == 1/10

def test_recall_1_bis():
    assert m.recall_k(['item10'], set(actual_items), 1) == 0

def test_recall_3():
    assert m.recall_k(rec_items, set(actual_items), 3) == 2/10

def test_recall_5():
    assert m.recall_k(rec_items, set(actual_items), 5) == 3/10

def test_mean_recall_1():
    assert m.mean_recall_k([rec_items, rec_items], [set(actual_items), set(actual_items)], 1) == 1/10

def test_mean_recall_3():
    assert m.mean_recall_k([rec_items, rec_items], [set(actual_items), set(actual_items)], 3) == 2/10

def test_mean_recall_5():
    assert m.mean_recall_k([rec_items, rec_items], [set(actual_items), set(actual_items)], 5) == 3/10

def test_reciprocal_rank():
    assert m.reciprocal_rank(rec_items, set(actual_items)) == 1
    
def test_mean_reciprocal_rank():
    assert m.mean_reciprocal_rank([rec_items, rec_items], [set(actual_items), set(actual_items)]) == 1
    
def test_item_coverage():
    assert m.item_coverage([rec_items[:5], rec_items[2:6]], set(rec_items)) == 6/10
    
def test_item_similarity():
    # TODO
    assert True
