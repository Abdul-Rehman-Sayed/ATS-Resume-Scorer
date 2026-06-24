import streamlit as st


def render():
    authed = bool(st.session_state.get("access_token"))

    # Hero (flat, solid color — styled via .hero in styles.css)
    st.markdown(
        """
        <div class="hero">
            <h1>ATS Resume Scorer</h1>
            <h3>Optimize Your Resume for Applicant Tracking Systems</h3>
            <p>Get instant feedback on your resume's ATS compatibility with AI-powered analysis.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Call-to-action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        label = "Start Analyzing Your Resume" if authed else "Get Started"
        if st.button(label, use_container_width=True, type="primary"):
            st.session_state.current_view = "scorer" if authed else "auth"
            st.rerun()

    st.markdown("---")

    # Features
    st.markdown("## Key Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            ### Comprehensive Scoring
            Detailed scores across 5 key dimensions:
            - Formatting (20%)
            - Keywords & Skills (25%)
            - Content Quality (25%)
            - Skill Validation (15%)
            - ATS Compatibility (15%)
            """
        )
    with col2:
        st.markdown(
            """
            ### Skill Validation
            Verify that your claimed skills are actually demonstrated in your
            projects and experience using AI-powered semantic analysis.

            **No more empty claims.**
            """
        )
    with col3:
        st.markdown(
            """
            ### Actionable Feedback
            Get clear, prioritized recommendations and a downloadable PDF report
            to improve your resume.

            **Know exactly what to fix.**
            """
        )

    st.markdown("---")

    # How it works
    st.markdown("## How It Works")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            #### Step 1 — Upload Your Resume
            Supports PDF and DOCX formats.
            """
        )
    with col2:
        st.markdown(
            """
            #### Step 2 — AI Analysis
            Our models analyze your resume across multiple dimensions.
            """
        )
    with col3:
        st.markdown(
            """
            #### Step 3 — Get Feedback
            Receive detailed recommendations to improve your resume.
            """
        )
