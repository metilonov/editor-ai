from editai.utils.math import clamp,normalize,overlap_ratio

def test_math():
    assert clamp(2)==1
    assert normalize([1,2,3])==[0.0,0.5,1.0]
    assert overlap_ratio(0,10,5,15)==.5
