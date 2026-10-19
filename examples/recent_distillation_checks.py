"""Finite-model checks of T50/T51, not automatic theorem verification."""
import itertools
import json
import math


def finite_envelope(values, beta):
    if beta <= 0 or not values or any(v < 0 for v in values.values()):
        raise ValueError("Need a nonnegative finite table and positive beta")
    return {s:max(value*math.exp(-beta*sum(a!=b for a,b in zip(s,t)))
                  for t,value in values.items()) for s in values}


def run_checks():
    n, beta, delta = 5, .6, .1
    samples = list(itertools.product((0,1),repeat=n))
    values = {s:.02+3*(sum(s)>=4) for s in samples}
    envelope = finite_envelope(values,beta)
    assert all(envelope[s] >= values[s]-1e-12 for s in samples)
    for s,t in itertools.product(samples,repeat=2):
        assert abs(math.log(envelope[s])-math.log(envelope[t])) <= beta*sum(a!=b for a,b in zip(s,t))+1e-12
    logs = [math.log(envelope[s]) for s in samples]
    mean_log = sum(logs)/len(logs)
    mgf = sum(math.exp(g-mean_log) for g in logs)/len(logs)
    assert mgf <= math.exp(n*beta*beta/8)+1e-12
    expected = sum(values.values())/len(values)
    factor = math.exp(beta*math.sqrt(n*math.log(1/delta)/2)+n*beta*beta/8)
    failure = sum(expected>envelope[s]*factor+1e-12 for s in samples)/len(samples)
    assert failure <= delta
    assert set(finite_envelope({s:0. for s in samples},beta).values()) == {0.}

    # Exact Gaussian moments for X'=0 and Y'=aY+b with shared N(0,1) initial state.
    flow_rows = []
    for a,b,time in itertools.product((-.4,0.,.3),(.2,.7),(.2,1.3)):
        scale = math.exp(a*time)
        mean = b*math.expm1(a*time)/a if a else b*time
        actual = (scale-1)**2+mean**2
        error = a*a+b*b  # E_{X~N(0,1)}(aX+b)^2.
        rate = 1+2*abs(a)
        upper = error*math.expm1(rate*time)/rate
        assert actual <= upper+1e-12
        flow_rows.append({"a":a,"time":time,"actual_squared_error":actual,"upper":upper})
    # If learned-field uniqueness is dropped, zero target-path error is insufficient.
    time = .7
    assert math.isclose(2*time,2*math.sqrt(time*time))
    return {"envelope":{"expected_value":expected,"true_failure_probability":failure,
                        "allowed_delta":delta,"centered_mgf":mgf,"mgf_upper":math.exp(n*beta*beta/8)},
            "flows":flow_rows,"nonunique_flow":{"target_error":0.,"selected_path_squared_error":time**4}}


if __name__ == "__main__":
    print(json.dumps(run_checks(),ensure_ascii=False,indent=2))
