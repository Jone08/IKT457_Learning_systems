import numpy as np


def compute_stationary_distribution(P_Y, P_L_given_Y, P_notL_given_notY, s):
    """
    P_Y                 ->  P(Y)   
    P_notY              ->  P(Ȳ)
    P_L_given_Y         ->  P(L|Y)
    P_L_given_notY      ->  P(L|Ȳ)
    P_notL_given_Y      ->  P(L̅|Y)
    P_notL_given_notY   ->  P(L̅|Ȳ)
    """

    P_notY = 1 - P_Y
    P_notL_given_Y = 1 - P_L_given_Y

    # Combined forgetting factor
    f = (P_L_given_Y * P_Y + P_notL_given_notY * P_notY)

    # Alpha
    a = 1

    # Pi values
    pi = np.zeros(8)
    pi[0] = a * P_Y**4  * 1                 * P_notL_given_Y**7     * 1         * 1
    pi[1] = a * P_Y**3  * 1                 * P_notL_given_Y**6     * s         * f
    pi[2] = a * P_Y**2  * 1                 * P_notL_given_Y**5     * s**2      * f**2
    pi[3] = a * P_Y     * 1                 * P_notL_given_Y**4     * s**3      * f**3
    pi[4] = a * 1       * 1                 * P_notL_given_Y**3     * s**4      * f**4
    pi[5] = a * 1       * P_L_given_Y       * P_notL_given_Y**2     * s**5      * f**4
    pi[6] = a * 1       * P_L_given_Y**2    * P_notL_given_Y**1     * s**6      * f**4
    pi[7] = a * 1       * P_L_given_Y**3    * 1                     * s**7      * f**4


    # Normalize so probabilities sum to 1
    total = np.sum(pi)
    pi = pi / total

    return pi


P_Y                 = 0.5
P_L_given_Y         = 0.5
P_notL_given_notY   = 0.5
s                   = 5.0


pi = compute_stationary_distribution(P_Y=P_Y, P_L_given_Y=P_L_given_Y, P_notL_given_notY=P_notL_given_notY, s=s)

print(pi)
print(f"Sum = {np.sum(pi)}")