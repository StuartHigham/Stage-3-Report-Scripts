import numpy as np

def integrate(accel, dt):
    """
    Performs double integration on the fly, yielding each new displacement value.

    Arguments:
        accel (iterable): Acceleration data (e.g., in mm/s²).
        dt (float): Time interval between samples.

    Returns:
        (i, velocity, displacement)
    """
    velocity = 0.0
    displacement = 0.0
    prev_acc = accel[0]
    prev_vel = velocity

    yield 0, velocity, displacement

    for i in range(1, len(accel)): # This will run through only one individual data point
        acc = accel[i]
        # Trapezoidal integration
        velocity += 0.5 * (acc + prev_acc) * dt
        displacement += 0.5 * (velocity + prev_vel) * dt

        yield i, velocity, displacement

        prev_acc = acc
        prev_vel = velocity

def HPfilter(accel, dt, alpha=0.995):
    """
    Performs double integration with high-pass filtering on displacement to reduce drift.

    Arguments:
        accel (iterable): Acceleration in mm/s².
        dt (float): Time step in seconds.
        alpha (float): High-pass filter coefficient (0.9–0.999 typical).

    Returns:
        (i, velocity, filtered_displacement)
    """
    velocity = 0.0
    displacement = 0.0
    filtered_displacement = 0.0
    prev_acc = accel[0]
    prev_vel = velocity
    prev_disp = 0.0
    prev_filtered = 0.0

    yield 0, velocity, filtered_displacement

    for i in range(1, len(accel)):
        acc = accel[i]
        # Trapezoidal integration
        velocity += 0.5 * (acc + prev_acc) * dt
        displacement += 0.5 * (velocity + prev_vel) * dt

        # High-pass filter to remove drift
        filtered_displacement = alpha * (prev_filtered + displacement - prev_disp)

        yield i, velocity, filtered_displacement

        prev_acc = acc
        prev_vel = velocity
        prev_disp = displacement
        prev_filtered = filtered_displacement

def kalman(accel, dt, correct_every=5):
    """
    Aggressive Kalman filter with frequent zero-velocity updates to minimize drift.
    """
    v = 0.0
    d = 0.0

    p11, p22 = 1e-4, 1e-4  # start confident
    q11, q22 = 5e-6, 1e-6  # assume low process noise

    r = 1e-4  # TRUST zero-velocity corrections more

    yield 0, v, d

    for i in range(1, len(accel)):
        a = accel[i]

        # Predict
        v_pred = v + a * dt
        d_pred = d + v * dt + 0.5 * a * dt * dt

        p11 += q11
        p22 += q22

        # Aggressive ZUPT: correct every few samples
        if i % correct_every == 0:
            z = 0.0  # assume chest pauses
            K = p11 / (p11 + r)
            v = v_pred + K * (z - v_pred)
            p11 = (1 - K) * p11
        else:
            v = v_pred

        d = d_pred

        yield i, v, d