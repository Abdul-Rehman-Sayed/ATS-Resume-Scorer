from typing import Any, Dict, List
import streamlit as st

def display_strengths(strengths: List[str]) -> None:
    st.markdown("### Strengths")
    if not strengths:
        st.info("Keep improving your resume to unlock strengths!")
        return
    for item in strengths:
        st.markdown(f"- {item}")

def display_critical_issues(analysis: Dict[str, Any]) -> None:
    critical = analysis.get("critical_issues") or []
    summary = analysis.get("issues_summary") or []

    st.markdown("### Critical Issues")

    if critical:
        st.error("These issues should be addressed first for better ATS performance.")
        for item in critical:
            st.markdown(f"- {item}")
        extra = [s for s in summary if s not in critical]
        if extra:
            with st.expander("Additional flagged items", expanded=False):
                for item in extra:
                    st.markdown(f"- {item}")
        return

    st.success("No critical issues found. See Detailed Feedback and Action Items below for improvements.")
    if summary:
        with st.expander("Flagged items to review", expanded=False):
            for item in summary:
                st.markdown(f"- {item}")
