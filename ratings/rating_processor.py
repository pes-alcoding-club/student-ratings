import logging
from math import sqrt, log

# this should be in db column
JSON_RATING = 'rating'
JSON_VOL = 'volatility'
JSON_TIMES = 'timesPlayed'


class RatingProcessor:
    """
    Takes a list of student
    """
    def __init__(self, player_dict_list):
        try:
            assert isinstance(player_dict_list, list)
            assert all(isinstance(x, dict) for x in player_dict_list)
            assert all(JSON_RATING in x for x in player_dict_list)
            assert all(JSON_VOL in x for x in player_dict_list)

        except AssertionError:
            logging.error('Invalid input to RatingProcessor')

    class ELO:
        """
        Implementation of ELO rating functions
        Source: https://www.codechef.com/ratings
        Comments contain older implementations
        """

        @staticmethod
        def Erank(Ra, Va, Rb_Vb_list):  # Expected Rank
            expected_rank = 0

            def Eab(Ra, Va, Rb, Vb):  # Probability that player A performs worse than player B
                return 1 / (1 + pow(4, ((Ra - Rb) / (sqrt(pow(Va, 2) + pow(Vb, 2))))))

            for Rb, Vb in Rb_Vb_list:
                expected_rank += Eab(Ra, Va, Rb, Vb)
            return expected_rank

        @staticmethod
        def Perf(rank, N):  # Performance
            return log(N / max(0.0001, rank - 0.9999)) / log(4)

        # Perf = lambda rank, N :  log(N/(rank-1)) / log(4) causes division by zero
        # Perf = lambda rank, N: log(N / (max(0.01, rank - 0.99))) / log(4)

        @classmethod
        def EPerf(cls, ERank, N):  # Expected Performance
            return cls.Perf(ERank, N)

        @classmethod
        def APerf(cls, ARank, N):  # Actual Performance
            return cls.Perf(ARank, N)

        @staticmethod
        def Cf(R_list, V_list, N):  # Competition Factor
            Ravg = sum(R_list) / len(R_list)
            term1 = sum(map(lambda x: x * x, V_list)) / N
            term2 = sum(map(lambda x: (x - Ravg) ** 2, R_list)) / (N - 1)
            return sqrt(term1 + term2)

        @staticmethod
        def RWa(timesPlayed):
            return (0.4 * timesPlayed + 0.2) / (0.7 * timesPlayed + 0.6)

        # RWa = lambda timesPlayed: (0.4 * timesPlayed + 0.2) / (0.7 * timesPlayed + 0.6)

        @staticmethod
        def VWa(timesPlayed):
            return (0.5 * timesPlayed + 0.8) / (timesPlayed + 0.6)

        # VWa = lambda timesPlayed: (0.5 * timesPlayed + 0.8) / (timesPlayed + 0.6)
        @staticmethod
        def NRa(Ra, APerf, EPerf, Cf, RWa):
            return Ra + (APerf - EPerf) * Cf * RWa

        # NRa = lambda Ra, APerf, EPerf, Cf, RWa: Ra + (APerf - EPerf) * Cf * RWa

        @staticmethod
        def NVa(VWa, NRa, Ra, Va):
            return sqrt((VWa * ((NRa - Ra) ** 2) + (Va ** 2)) / (VWa + 1.1))

        # NVa = lambda VWa, NRa, Ra, Va: sqrt((VWa * ((NRa - Ra) ** 2) + (Va ** 2)) / (VWa + 1.1))

        @staticmethod
        def Rcap(Ra, timesPlayed):
            return 100 + (75 / (timesPlayed + 1)) + ((100 * 500) / (abs(Ra - 1500) + 500))

        # Rcap = lambda Ra, timesPlayed: 100 + (75 / (timesPlayed + 1)) + ((100 * 500) / (abs(Ra - 1500) + 500))

        @staticmethod
        def Vcap(Va):
            return max(75, min(Va, 200))
        # Vcap = lambda Va: max(75, min(Va, 200))  # (75, 200) #the volatility can change maximum by these two
