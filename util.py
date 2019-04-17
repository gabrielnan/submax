
def get_mean(fn, num_samples):
    sum = 0
    for i in range(num_samples):
        sum += fn()
    return sum / num_samples
