import numpy as np
import catch_errors


def relative_strength_index(data, period):
    """
    Relative Strength Index.

    RSI = 100 - (100 / 1 + (prevGain/prevLoss))
    """
    catch_errors.check_for_period_error(data, period)

    period = int(period)
    changes = map(lambda data_tup: data_tup[1] - data_tup[0], zip(data[::1], data[1::1]))

    filtered_gain = map(lambda val: val < 0, changes)
    gains = map(lambda idx: 0 if filtered_gain[idx] is True else changes[idx], range(0, len(filtered_gain)))

    filtered_loss = map(lambda val: val > 0, changes)
    losses = map(lambda idx: 0 if filtered_loss[idx] is True else abs(changes[idx]), range(0, len(filtered_loss)))

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    rsi = []
    if avg_loss == 0:
        rsi.append(100)
    else:
        rs = avg_gain / avg_loss
        rsi.append(100 - (100 / (1 + rs)))

    for idx in range(1, len(data) - period):
        avg_gain = ((avg_gain * (period - 1) + gains[idx + (period - 1)]) / period)
        avg_loss = ((avg_loss * (period - 1) + losses[idx + (period - 1)]) / period)

        if avg_loss == 0:
            rsi.append(100)
        else:
            rs = avg_gain / avg_loss
            rsi.append(100 - (100 / (1 + rs)))

    non_computable_values = np.repeat(np.nan, len(data) - len(rsi))
    rsi = np.append(non_computable_values, rsi)

    return rsi
