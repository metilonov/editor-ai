from editai.services.rate_limit import SlidingRateLimit

def test_rate_limit():
    x=SlidingRateLimit(2,60)
    assert x.allow(1) and x.allow(1) and not x.allow(1)
