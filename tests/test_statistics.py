from src.statistics import sign_flip_pvalue, holm

def test_five_seed_exact_floor():
    assert sign_flip_pvalue([1,2,3,4,5]) == 0.0625

def test_holm_monotone_and_family():
    x=holm([0.01,0.02,0.2])
    assert abs(x[0]-.03)<1e-10 and abs(x[1]-.04)<1e-10
