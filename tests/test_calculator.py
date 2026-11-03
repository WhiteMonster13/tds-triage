import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tds_triage import compute_tds

def case(**k):
    d = dict(payee="other", pan=True, gross=100000, gst=0, prior_ytd=0)
    d.update(k)
    return d

def test_gst_excluded():            # c01
    assert compute_tds(case(gross=236000, gst=36000), "194J_professional")["tds"] == 20000
def test_no_pan_20pct():            # c12
    assert compute_tds(case(payee="individual", pan=False), "194J_professional")["tds"] == 20000
def test_threshold_catchup():       # c02
    assert compute_tds(case(payee="individual", gross=80000, prior_ytd=560000), "194I_building")["tds"] == 64000
def test_below_threshold_zero():
    assert compute_tds(case(gross=500000), "194I_building")["tds"] == 0
def test_individual_rate_194C():    # c08
    assert compute_tds(case(payee="individual", gross=45000), "194C_contractor")["tds"] == 450

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("pass", name)