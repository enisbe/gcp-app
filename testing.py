from mlib import multiply 
from mlib import keep, load_models
from mlib import load_test_data
import numpy as np
import pickle


def test_multiply():
     assert 12 == multiply(3,4)

def test_score():   
    """test model output with expected values"""
    expected_results ={"predicted=1": [
            0.08020394910646916,
            0.04135674900371706,
            0.01543703769387024,
            0.07310729402770287,
            0.10729297692992816,
            0.025973690929737003,
            0.05397958700198282,
            0.04371209879083955,
            0.007954856044590747,
            0.40790066865922314
        ]}
    expected_array =    np.array(expected_results['predicted=1'])
    rfr, med = load_models()  
    file = "./data/cs-test.csv"
    test_df = load_test_data(file)[0:10]
      
    test_df.fillna(med,inplace=True)
    predicted = rfr.predict_proba(test_df)[:,1]
    assert np.allclose(expected_array,predicted)
 
 
