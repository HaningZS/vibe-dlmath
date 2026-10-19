"""Small exact/numerical illustrations; these checks are not theorem certification."""
import itertools
import math
import json


def relu_interpolant(values, x):
    if len(values) < 2 or not 0 <= x <= 1:
        raise ValueError("Need at least two grid values and x in [0,1]")
    m = len(values)-1
    slopes = [m*(values[k+1]-values[k]) for k in range(m)]
    return values[0]+slopes[0]*x+sum(
        (slopes[k]-slopes[k-1])*max(x-k/m,0) for k in range(1,m)
    )


def run_checks():
    results = {}

    # T32: finite-class risk decomposition with an approximate ERM.
    losses = [[0,.8,.8],[.3,.2,.2],[.2,.3,.1]]
    population, empirical = [.2,.3,.5], [.3,.2,.5]
    risk = [sum(a*b for a,b in zip(row,population)) for row in losses]
    train = [sum(a*b for a,b in zip(row,empirical)) for row in losses]
    chosen = 1
    approximation = min(risk)  # Larger comparison class has risk infimum 0.
    deviation = max(abs(a-b) for a,b in zip(risk,train))
    optimization = train[chosen]-min(train)
    upper = approximation+2*deviation+optimization
    assert risk[chosen] <= upper+1e-12
    results["risk_decomposition"] = {"risk":risk[chosen],"upper":upper}

    # T34: exact ReLU representation of piecewise-linear interpolation.
    m = 8
    values = [(k/m)**2 for k in range(m+1)]
    max_error = max(abs(relu_interpolant(values,(k+.5)/m)-((k+.5)/m)**2) for k in range(m))
    assert math.isclose(max_error, 2/(8*m*m), abs_tol=1e-12)
    for k in range(m+1):
        assert math.isclose(relu_interpolant(values,k/m),values[k],abs_tol=1e-12)
    results["relu_interpolation"] = {"max_midpoint_error":max_error}

    # T33/T35: exact Rademacher expectation for a bounded linear class.
    xs = [(1.,0.),(0.,1.),(-1.,0.),(0.,-1.)]
    W, n = 2., len(xs)
    norms = []
    for signs in itertools.product((-1,1),repeat=n):
        vec = [sum(sign*x[j] for sign,x in zip(signs,xs)) for j in range(2)]
        norms.append(math.sqrt(sum(v*v for v in vec)))
    rad = W/n*sum(norms)/len(norms)
    assert rad <= W/math.sqrt(n)+1e-12
    results["linear_rademacher"] = {"exact":rad,"upper":W/math.sqrt(n)}

    # T36: finite-path illustration of decreasing loss and growing parameter.
    w, previous_loss = 0., math.log(2)
    for _ in range(1000):
        old = w
        w += .5/(1+math.exp(w))
        loss = math.log1p(math.exp(-w))
        assert w > old and loss < previous_loss
        previous_loss = loss
    results["logistic_path"] = {"parameter":w,"loss":previous_loss}

    # T37: enumerate the one-positive / one-independent-negative sampling law.
    K, accuracy = 2, .8
    nce, kl, total = 0., 0., 0.
    for index,x,ys in itertools.product(range(K),range(2),itertools.product(range(2),repeat=K)):
        conditional = [accuracy if y==x else 1-accuracy for y in ys]
        p = (1/K)*.5*conditional[index]*(.5**(K-1))
        q = (1/K)*.5*(.5**K)
        posterior = conditional[index]/sum(conditional)
        nce += p*(-math.log(posterior))
        kl += p*math.log(p/q)
        total += p
    mi = accuracy*math.log(2*accuracy)+(1-accuracy)*math.log(2*(1-accuracy))
    assert math.isclose(total,1.,abs_tol=1e-12)
    assert math.isclose(kl,mi,abs_tol=1e-12)
    assert math.log(K)-nce <= mi+1e-12
    results["infonce"] = {"lower_bound":math.log(K)-nce,"mutual_information":mi}

    # T38: a prefix-free code respects the allocated union-bound budget.
    codes, delta = ["0","10","110"], .05
    assert not any(b.startswith(a) for a in codes for b in codes if a!=b)
    budget = sum(delta*2**(-len(code)) for code in codes)
    assert budget <= delta
    results["coding"] = {"allocated_delta":budget,"allowed_delta":delta}

    # T39: exact soft-thresholding prox for a quadratic plus L1 penalty.
    eta, penalty, T = .4, .5, 30
    objective = lambda x: .5*(x-3)**2+penalty*abs(x)
    x = -2.
    initial = objective(x)
    total_mapping = 0.
    for _ in range(T):
        u = x-eta*(x-3)
        nxt = math.copysign(max(abs(u)-eta*penalty,0),u)
        mapping = (x-nxt)/eta
        assert objective(nxt) <= objective(x)-eta/2*mapping*mapping+1e-12
        total_mapping += mapping*mapping
        x = nxt
    upper = 2*(initial-objective(2.5))/(eta*T)
    assert total_mapping/T <= upper+1e-12
    results["proximal"] = {"average_mapping_squared":total_mapping/T,"upper":upper}
    return results


if __name__ == "__main__":
    print(json.dumps(run_checks(),ensure_ascii=False,indent=2))
