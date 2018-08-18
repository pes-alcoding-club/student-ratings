"""
Implementation of ELO rating functions
Source: https://www.codechef.com/ratings
"""

from math import log, sqrt

DEFAULT_RATING = 1500
DEFAULT_VOLATILITY = 125


def Eab(Ra, Va, Rb, Vb):  # Probability that player A performs worse than player B
    return 1 / (1 + pow(4, ((Ra - Rb) / (sqrt(pow(Va, 2) + pow(Vb, 2))))))


def ERank(Ra, Va, Rb_Vb_list):  # Expected Rank
    expected_rank = 0
    for Rb, Vb in Rb_Vb_list:
        expected_rank += Eab(Ra, Va, Rb, Vb)
    return expected_rank


def Perf(rank, N):  # Performance
    return log(N / max(0.0001, rank - 0.9999)) / log(4)


def EPerf(expected_rank, N):  # Expected Performance
    return Perf(expected_rank, N)


def APerf(actual_rank, N):  # Actual Performance
    return Perf(actual_rank, N)


def Cf(R_list, V_list, N):  # Competition Factor
    Ravg = sum(R_list) / len(R_list)
    term1 = sum(map(lambda x: x * x, V_list)) / N
    term2 = sum(map(lambda x: (x - Ravg) ** 2, R_list)) / (N - 1)
    return sqrt(term1 + term2)


def RWa(timesPlayed):  # Rating weight
    return (0.4 * timesPlayed + 0.2) / (0.7 * timesPlayed + 0.6)


def VWa(timesPlayed):  # Volatility weight
    return (0.5 * timesPlayed + 0.8) / (timesPlayed + 0.6)


def NRa(Ra, APerf, EPerf, Cf, RWa):  # New rating
    return Ra + (APerf - EPerf) * Cf * RWa


def NVa(VWa, NRa, Ra, Va):  # New volatility
    return sqrt((VWa * ((NRa - Ra) ** 2) + (Va ** 2)) / (VWa + 1.1))


def Rcap(Ra, NRa, timesPlayed):  # Cap to how much rating can change
    cap = 100 + (75 / (timesPlayed + 1)) + ((100 * 500) / (abs(Ra - 1500) + 500))
    if NRa > Ra:
        return min(NRa, Ra + cap)
    return max(NRa, Ra - cap)


def Vcap(Va):  # Cap to how much the volatility can change
    return max(75, min(Va, 200))


def process(Ra, Va, timesPlayed, actual_rank, Rb_Vb_list, N, Cf):
    """
    :param Ra: Current rating
    :param Va: Current volatility
    :param timesPlayed: Current timesPlayed
    :param actual_rank: Actual rank in the contest
    :param Rb_Vb_list: Rating and volatility of remaining players
    :param N: Total players
    :param Cf: Competition factor
    :return: 2-tuple of new rating and new volatility
    """

    new_rating = NRa(Ra,
                     APerf(actual_rank, N),
                     EPerf(ERank(Ra, Va, Rb_Vb_list), N),
                     Cf,
                     RWa(timesPlayed)
                     )

    new_volatility = NVa(VWa(timesPlayed), new_rating, Ra, Va)

    new_rating = Rcap(Ra, new_rating, timesPlayed)
    new_volatility = Vcap(new_volatility)

    return new_rating, new_volatility

if __name__ == "__main__":
    print(Eab(10, 3, 5, 4))