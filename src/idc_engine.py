from scipy.stats import beta as beta_dist


def beta_expenditure_profile(
    construction_years: int, alpha: float = 2.0, beta_param: float = 2.0
) -> list[float]:
    """Fraction of CAPEX spent in each year of construction (sums to 1.0).

    Modeled as a beta(alpha, beta_param) distribution over the normalized
    construction timeline [0, 1]; the default alpha=beta_param=2 gives the
    classic S-curve shape (slow start, peak mid-construction, tapering
    off), unlike a flat or single-point expenditure assumption.
    """
    dist = beta_dist(alpha, beta_param)
    edges = [i / construction_years for i in range(construction_years + 1)]
    cdf_values = [dist.cdf(edge) for edge in edges]
    return [cdf_values[i + 1] - cdf_values[i] for i in range(construction_years)]


def calculate_idc(
    capex_usd: float,
    construction_years: int,
    wacc: float,
    alpha: float = 2.0,
    beta_param: float = 2.0,
) -> float:
    """Interest during construction (USD), accrued period by period.

    Each year's expenditure (per the beta profile) is added to the
    outstanding balance, and interest accrues on the full balance every
    year until commercial operation — unlike a single compound markup
    applied to the whole CAPEX at one assumed midpoint.
    """
    profile = beta_expenditure_profile(construction_years, alpha, beta_param)
    balance = 0.0
    for fraction in profile:
        expenditure = capex_usd * fraction
        balance = (balance + expenditure) * (1 + wacc)
    return balance - capex_usd


def calculate_idc_simplified_compound(
    capex_usd: float, construction_years: int, wacc: float
) -> float:
    """Legacy IDC approximation: compounds the entire CAPEX as if spent in
    one lump sum at the midpoint of construction. Kept here only as the
    baseline the S-curve method (calculate_idc) is meant to replace.
    """
    return capex_usd * ((1 + wacc) ** (construction_years / 2) - 1)
