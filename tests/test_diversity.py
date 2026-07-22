from editai.analysis.diversity import select_diverse
from editai.domain.models import Candidate

def test_diversity():
    x=[Candidate(0,30,score=.9),Candidate(5,35,score=.8),Candidate(40,70,score=.7)]
    y=select_diverse(x,2)
    assert len(y)==2
    assert y[0].start==0 and y[1].start==40
