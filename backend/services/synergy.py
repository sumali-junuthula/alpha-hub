def estimate_synergy_deal(target_revenue, target_margin, expected_synergies, deal_cost):
  """
  Estimate post-merger value creation from synergy gains, using simplified logic.
  """
  base_operating_income = target_revenue * target_margin
  synergy_gain = expected_synergies - deal_cost
  total_value_creation = base_operating_income + synergy_gain

  return {
    "target_revenue": f"${target_revenue:,.0f}",
    "target_margin": f"{target_margin:.2%}",
    "expected_synergies": f"${expected_synergies:,.0f}",
    "deal_cost": f"${deal_cost:,.0f}",
    "value_creation": f"${total_value_creation:,.0f}",
    "summary": (
      f"Estimated post-merger value creation is ${round(total_value_creation / 1e6, 2)}M, "
      f"driven by synergy gains of ${expected_synergies / 1e6:.1f}M and deal costs of ${deal_cost / 1e6:.1f}M."
    )
  }
