from src.theory import exact

def test_no_information_risk():
    a=.28;alpha=.2;hs=[1,3,6]
    q=a*a*sum((1-alpha)**(2*h) for h in hs)
    assert abs(exact(0,a,alpha,hs)-q)<1e-12

def test_release_decreases_risk():
    assert exact(42,.28,.2,[1,3,6])<exact(9,.28,.2,[1,3,6])
