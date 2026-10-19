"""Finite/exact illustrations of the specialized cards; standard library only."""
import itertools
import json
import math
from statistics import NormalDist


def projected_square_train(features, labels, radius, steps):
    """Train only output coefficients; return the average of iterates 1..T."""
    n = len(labels)
    if n == 0 or len(features) != n or radius <= 0 or steps < 1:
        raise ValueError("Need matched data, positive radius and at least one step")
    width = len(features[0])
    if width == 0:
        raise ValueError("Need at least one feature")
    if any(len(row) != width or any(abs(x) > 1 for x in row) for row in features):
        raise ValueError("Features must have fixed width and absolute value <= 1")
    w, total = [0.0]*width, [0.0]*width
    for _ in range(steps):
        residual = [sum(a*b for a,b in zip(w,row))-y for row,y in zip(features,labels)]
        gradient = [sum(r*row[j] for r,row in zip(residual,features))/n for j in range(width)]
        nxt = [a-g/width for a,g in zip(w,gradient)]
        norm = math.sqrt(sum(a*a for a in nxt))
        scale = min(1.0,radius/norm) if norm else 1.0
        w = [a*scale for a in nxt]
        total = [a+b for a,b in zip(total,w)]
    return [a/steps for a in total]


def square_risk(weights, features, labels):
    return sum((sum(a*b for a,b in zip(weights,row))-y)**2/2
               for row,y in zip(features,labels))/len(labels)


def bernoulli_kl(q, p):
    if not 0 <= q <= 1 or not 0 < p < 1:
        raise ValueError("Need q in [0,1], p in (0,1)")
    return (q*math.log(q/p) if q else 0) + ((1-q)*math.log((1-q)/(1-p)) if q<1 else 0)


def wl_pair(first, second, rounds):
    colors = [[0]*len(first), [0]*len(second)]
    for _ in range(rounds):
        signatures = [[(colors[k][v],tuple(sorted(colors[k][u] for u in neighbors)))
                       for v,neighbors in enumerate(graph)] for k,graph in enumerate((first,second))]
        codes = {key:i for i,key in enumerate(sorted(set(signatures[0]+signatures[1])))}
        colors = [[codes[key] for key in row] for row in signatures]
    return tuple(sorted(colors[0])), tuple(sorted(colors[1]))


def run_checks():
    out = {}
    # T40: cos has gradient/Hessian Lipschitz constants 1 globally.
    epsilon_h = .5
    step = 2*epsilon_h
    actual = 1-math.cos(step)
    guaranteed = 2*epsilon_h**3/3
    assert actual >= guaranteed
    out["negative_curvature"] = {"decrease":actual,"guaranteed":guaranteed}

    # T41: enumerate all iid samples; compare MC error to exact Hilbert variance.
    atoms = [(1.,0.),(0.,1.)]
    mean, m = (.5,.5), 3
    samples = list(itertools.product(atoms,repeat=m))
    expected = sum(sum((sum(row[j] for row in sample)/m-mean[j])**2 for j in range(2))
                   for sample in samples)/len(samples)
    assert math.isclose(expected,.5/m,abs_tol=1e-12)
    out["random_features"] = {"expected_error":expected,"variance_over_width":.5/m}

    # T42: check the closed-form bilinear gradient-flow equation by finite differences.
    b0, time, dt = .09, .7, 1e-5
    b = lambda t: 1/(1+(1/b0-1)*math.exp(-2*t))
    derivative = (b(time+dt)-b(time-dt))/(2*dt)
    rhs = -2*b(time)*(b(time)-1)
    assert math.isclose(derivative,rhs,rel_tol=1e-8)
    assert 2*b(time) > 2*b0
    out["kernel_drift"] = {"initial_kernel":2*b0,"later_kernel":2*b(time)}

    # T43: token permutation commutes with unmasked attention, but not fixed positions.
    attention = lambda xs: [sum(math.exp(q*k)*v for k,v in zip(xs,xs)) /
                            sum(math.exp(q*k) for k in xs) for q in xs]
    xs, order, pos = [.2,-.4,.7], [2,0,1], [0.,.3,.8]
    expected_attention = [attention(xs)[j] for j in order]
    actual_attention = attention([xs[j] for j in order])
    assert all(math.isclose(a,b,abs_tol=1e-12) for a,b in zip(actual_attention,expected_attention))
    fixed_positions = attention([xs[j]+p for j,p in zip(order,pos)])
    reordered_positions = [attention([a+p for a,p in zip(xs,pos)])[j] for j in order]
    assert max(abs(a-b) for a,b in zip(fixed_positions,reordered_positions)) > .01
    out["attention_equivariance"] = {"permutation_holds":True,"fixed_positions_break_it":True}

    # T44: a cycle and two triangles remain 1-WL indistinguishable.
    cycle = [((v-1)%6,(v+1)%6) for v in range(6)]
    triangles = [(1,2),(0,2),(0,1),(4,5),(3,5),(3,4)]
    assert wl_pair(cycle,triangles,6)[0] == wl_pair(cycle,triangles,6)[1]
    out["gnn_limit"] = {"same_color_multiset":True,"different_connectivity":True}

    # T45: a half-space classifier attains the binary smoothing boundary.
    normal, sigma, x = NormalDist(), .4, .6
    pa = normal.cdf(x/sigma)
    radius = sigma*normal.inv_cdf(pa)
    assert math.isclose(radius,x,abs_tol=1e-12)
    assert normal.cdf((x-.99*radius)/sigma) > .5
    assert normal.cdf((x-1.01*radius)/sigma) < .5
    out["smoothing"] = {"radius":radius,"boundary":x}

    # T46: independent numerical integration of the Gaussian privacy-loss MGF.
    alpha, shift, segments = 2., .6, 6000
    low, high = -12., 12.
    spacing = (high-low)/segments
    total = 0.
    for i in range(segments+1):
        z = low+i*spacing
        privacy_loss = shift*shift/2+shift*z
        value = math.exp((alpha-1)*privacy_loss)*math.exp(-z*z/2)/math.sqrt(2*math.pi)
        total += value*(1 if i in (0,segments) else (4 if i%2 else 2))
    numeric_rdp = math.log(total*spacing/3)/(alpha-1)
    exact_rdp = alpha*shift*shift/2
    assert math.isclose(numeric_rdp,exact_rdp,abs_tol=1e-10)
    out["privacy"] = {"integrated_rdp":numeric_rdp,"formula_rdp":exact_rdp}

    # T47: unequal local curvatures create an exact averaged-gradient bias.
    clients, weights, eta = [0.,0.], [.5,.5], .2
    gradients = [lambda a:a+1, lambda a:2*(a-1)]
    for _ in range(2):
        clients = [a-eta*g(a) for a,g in zip(clients,gradients)]
    average = sum(p*a for p,a in zip(weights,clients))
    local_gradient = sum(p*g(a) for p,g,a in zip(weights,gradients,clients))
    global_gradient = sum(p*g(average) for p,g in zip(weights,gradients))
    bias = local_gradient-global_gradient
    drift = sum(p*(a-average)**2 for p,a in zip(weights,clients))
    assert bias != 0 and bias*bias <= 4*drift+1e-12
    out["client_drift"] = {"bias_squared":bias*bias,"L_squared_D":4*drift}

    # T48: observational equality does not identify the interventional effect.
    first_world = lambda u,a: a
    second_world = lambda u,a: u
    first_observed = [(u,first_world(u,u)) for u in (0,1)]
    second_observed = [(u,second_world(u,u)) for u in (0,1)]
    first_effect = sum(first_world(u,1)-first_world(u,0) for u in (0,1))/2
    second_effect = sum(second_world(u,1)-second_world(u,0) for u in (0,1))/2
    assert first_observed == second_observed and first_effect != second_effect
    out["causal_nonidentification"] = {"first_ate":first_effect,"second_ate":second_effect}

    # T49: all conditional probabilities, endpoint targets and threshold ties.
    for truth in (0.,.01,.2,.49,.5,.51,.8,.99,1.):
        for prediction in (.01,.1,.49,.5,.51,.9,.99):
            kl = bernoulli_kl(truth,prediction)
            excess = abs(2*truth-1)*int((prediction>=.5)!=(truth>=.5))
            assert kl+1e-12 >= 2*(truth-prediction)**2
            assert excess <= math.sqrt(2*max(kl,0))+1e-12
    out["surrogate_bridge"] = {"checked_pairs":63}

    # End-to-end: fixed ReLU features with a feasible exact comparison solution.
    grid = [-1.,-.5,0.,.5,1.]
    features = [[max(x,0),max(-x,0)] for x in grid]
    labels = [abs(x) for x in grid]
    steps, radius = 80, 1.5
    learned = projected_square_train(features,labels,radius,steps)
    risk = square_risk(learned,features,labels)
    comparator = square_risk([1.,1.],features,labels)
    gap_upper = len(features[0])*radius**2/(2*steps)
    assert risk-comparator <= gap_upper+1e-12
    assert math.sqrt(sum(a*a for a in learned)) <= radius+1e-12
    out["output_layer_training"] = {"empirical_gap":risk-comparator,"upper":gap_upper}
    return out


if __name__ == "__main__":
    print(json.dumps(run_checks(),ensure_ascii=False,indent=2))
