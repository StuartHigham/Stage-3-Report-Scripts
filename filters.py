def integrate_twice_live(accel, dt):
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

def integrate_twice_live_filtered(accel, dt, alpha=0.995):
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