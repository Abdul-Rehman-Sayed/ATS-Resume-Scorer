from typing import Any, Dict

import streamlit as st

from frontend.components.score_display import display_overall_score, display_score_breakdown
from frontend.components.strengths_issues import display_strengths, display_critical_issues
from frontend.components.skill_validation import display_skill_validation
from frontend.components.jd_comparison import display_jd_comparison
from frontend.components.detailed_feedback import display_detailed_feedback
from frontend.components.action_items import display_action_items
from frontend.components.recommendations import display_recommendations
from frontend.components.action_items import _collect_action_items

def display_results_dashboard(analysis: Dict[str, Any]) -> None:
    display_overall_score(analysis)
    st.markdown("---")

    display_score_breakdown(analysis)
    st.markdown("---")

    display_strengths(analysis.get("strengths") or [])
    st.markdown("---")

    display_critical_issues(analysis)
    st.markdown("---")

    display_skill_validation(analysis)

    jd_comparison = analysis.get("jd_comparison") or analysis.get("jd_match_analysis")
    if jd_comparison:
        st.markdown("---")
        display_jd_comparison(jd_comparison)

    if analysis.get("detailed_feedback"):
        st.markdown("---")
        display_detailed_feedback(analysis)

    if _collect_action_items(analysis):
        st.markdown("---")
        display_action_items(analysis)

    if analysis.get("suggestions"):
        st.markdown("---")
        display_recommendations(analysis)
