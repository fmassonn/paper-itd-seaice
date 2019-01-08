# Configuration file for the data



def LIM_itd(N, hbar = 2.0, alpha = 0.05):
    """
    Function returning the category limits for the LIM3 formulation

    N    : number of categories
    hbar : expected mean thickness over the domain
    alpha: exponent controlling the shape of the ITD

    Returns: the N upper limits of the N categories
    """

    if (type(N) is not int) or (N < 1):
        sys.exit("(f) error: N not valid")


    def fun(i):
        return ((N * (3.0 * hbar + 1.0) ** alpha) / \
               ((N - i) * (3.0 * hbar + 1.0) ** alpha + i) ) ** (alpha ** (-1.0)) \
               - 1.0

    out = [fun(i) for i in range(1, N + 1)]
    out[-1] = 99.0 # LIM convention to replace last boundary

    return out



# Repository where the data is found
repo = "/storepelican/fmasson/paper-itd-seaice-data/"


#            Name in   NEMO ID   Color plot  ITD bounds
#            paper
metadata = [
            ["S1.01", "EXP_015", "#957DAD", LIM_itd(1), "(1 cat.)"], \
            ["S1.03", "EXP_016", "#2C1392", LIM_itd(3), "(3 cat.)"], \
            ["S1.05", "EXP_014", "#83AE44", LIM_itd(5), "(5 cat.)"], \
            ["S1.10", "EXP_017", "#FFD500", LIM_itd(10),"(10 cat.)"],\
            ["S1.30", "EXP_018", "#FFB661", LIM_itd(30),"(30 cat.)"],\
            ["S1.50", "EXP_019", "#FF6961", LIM_itd(50),"(50 cat.)"],\
            ["S2.03", "EXP_020", "#00332b", [0.25, 0.50,                                                                          99.0], "(3 cat.)"],\
            ["S2.05", "EXP_021", "#e7b382", [0.25, 0.50, 0.75, 1.00,                                                              99.0], "(5 cat.)"],\
            ["S2.07", "EXP_022", "#bbaa5e", [0.25, 0.50, 0.75, 1.00, 1.50, 2.00,                                                  99.0], "(7 cat.)"],\
            ["S2.09", "EXP_023", "#F09D9D", [0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00,                                      99.0], "(9 cat.)"],\
            ["S2.11", "EXP_024", "#8ba4ae", [0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00, 6.00, 8.00,                          99.0], "(11 cat.)"],\
            ["S2.15", "EXP_025", "#94d6ba", [0.25, 0.50, 0.75, 1.00, 1.50, 2.00, 3.00, 4.00, 6.00, 8.00, 11.00, 14.0, 17.0, 20.0, 99.0], "(15 cat.)"],\
            ["S3.05", "EXP_026", "#FE4365", [                                                    0.50,                                                     1.00,                                               2.00,                                           4.00, 99.0], "(5 cat.)"],\
            ["S3.17", "EXP_027", "#F9CDAD", [        0.125,         0.25,         0.375,         0.50,         0.625,         0.75,         0.875,         1.00,        1.25,        1.50,        1.75,        2.00,       2.50,       3.00,       3.50,       4.00, 99.0], "(17 cat.)"],\
            ["S3.33", "EXP_028", "#83AF9B", [0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.4375, 0.50, 0.5625, 0.625, 0.6875, 0.75, 0.8125, 0.875, 0.9375, 1.00, 1.125, 1.25, 1.375, 1.50, 1.625, 1.75, 1.875, 2.00, 2.25, 2.50, 2.75, 3.00, 3.25, 3.50, 3.75, 4.00, 99.0], "(33 cat.)"],\
            ["REF",   "REF"    , "#434343", [], ""],\
           ]


