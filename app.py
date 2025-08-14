import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from ibm_watsonx_gov.evaluators import MetricsEvaluator
from ibm_watsonx_gov.metrics import (
    HAPMetric, PIIMetric, HarmMetric, ProfanityMetric, JailbreakMetric, 
    EvasivenessMetric, SocialBiasMetric, SexualContentMetric, 
    UnethicalBehaviorMetric, ViolenceMetric, AnswerRelevanceMetric, 
    ContextRelevanceMetric, FaithfulnessMetric, TopicRelevanceMetric, 
    PromptSafetyRiskMetric
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Guardrails Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title and description
st.title("🛡️ AI Guardrails Dashboard")
st.markdown("**Powered by IBM watsonx.governance**")
st.markdown("Evaluate text content for various safety and quality metrics using advanced AI guardrails.")

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'evaluated_text' not in st.session_state:
    st.session_state.evaluated_text = ""

def initialize_evaluator():
    """Initialize the MetricsEvaluator with error handling"""
    try:
        # Load credentials from environment variables
        watsonx_apikey = os.getenv("WATSONX_APIKEY")
        wxg_service_instance_id = os.getenv("WXG_SERVICE_INSTANCE_ID")
        
        if not watsonx_apikey:
            st.error("❌ WATSONX_APIKEY not found in environment variables. Please check your .env file.")
            return None
        if not wxg_service_instance_id:
            st.error("❌ WXG_SERVICE_INSTANCE_ID not found in environment variables. Please check your .env file.")
            return None
        
        # Set environment variables for the evaluator
        os.environ["WATSONX_APIKEY"] = watsonx_apikey
        os.environ["WXG_SERVICE_INSTANCE_ID"] = wxg_service_instance_id
        
        # Initialize evaluator
        evaluator = MetricsEvaluator()
        return evaluator
    except Exception as e:
        st.error(f"❌ Failed to initialize evaluator: {str(e)}")
        return None

def get_available_metrics():
    """Return dictionary of available metrics with descriptions"""
    return {
        "HAP (Hate, Abuse, Profanity)": {
            "metric": HAPMetric(),
            "description": "Detects harmful language and offensive content",
            "column_name": "hap"
        },
        "PII Detection": {
            "metric": PIIMetric(),
            "description": "Identifies personally identifiable information",
            "column_name": "pii"
        },
        "Harm Detection": {
            "metric": HarmMetric(),
            "description": "Assesses content for potential harmful intent",
            "column_name": "harm.granite_guardian"
        },
        "Social Bias": {
            "metric": SocialBiasMetric(),
            "description": "Identifies biased or discriminatory language",
            "column_name": "social_bias.granite_guardian"
        },
        "Jailbreak Detection": {
            "metric": JailbreakMetric(),
            "description": "Prevents prompt injection and manipulation attempts",
            "column_name": "jailbreak.granite_guardian"
        },
        "Violence Detection": {
            "metric": ViolenceMetric(),
            "description": "Identifies violent or threatening content",
            "column_name": "violence.granite_guardian"
        },
        "Profanity Detection": {
            "metric": ProfanityMetric(),
            "description": "Filters inappropriate language",
            "column_name": "profanity.granite_guardian"
        },
        "Unethical Behavior": {
            "metric": UnethicalBehaviorMetric(),
            "description": "Identifies content promoting unethical activities",
            "column_name": "unethical_behavior.granite_guardian"
        },
        "Sexual Content": {
            "metric": SexualContentMetric(),
            "description": "Detects sexual or adult content",
            "column_name": "sexual_content.granite_guardian"
        },
        "Evasiveness": {
            "metric": EvasivenessMetric(),
            "description": "Detects evasive or non-responsive content",
            "column_name": "evasiveness.granite_guardian"
        }
    }

def get_rag_metrics():
    """Return dictionary of RAG-specific metrics"""
    return {
        "Answer Relevance": {
            "metric": AnswerRelevanceMetric(method="granite_guardian"),
            "description": "Evaluates how well responses address input questions",
            "column_name": "answer_relevance.granite_guardian"
        },
        "Context Relevance": {
            "metric": ContextRelevanceMetric(method="granite_guardian"),
            "description": "Assesses relevance of provided context to questions",
            "column_name": "context_relevance.granite_guardian"
        },
        "Faithfulness": {
            "metric": FaithfulnessMetric(method="granite_guardian"),
            "description": "Measures consistency between generated content and source",
            "column_name": "faithfulness.granite_guardian"
        }
    }

def get_advanced_metrics():
    """Return dictionary of advanced metrics that require system prompts"""
    return {
        "Topic Relevance": {
            "metric": TopicRelevanceMetric,
            "description": "Ensures content stays on-topic (requires system prompt)",
            "column_name": "topic_relevance",
            "requires_system_prompt": True
        },
        "Prompt Safety Risk": {
            "metric": PromptSafetyRiskMetric,
            "description": "Detects off-topic content and prompt injection (requires system prompt)",
            "column_name": "prompt_safety_risk.prompt_injection_125m_0.7_en",
            "requires_system_prompt": True
        }
    }

def style_results_table(df, threshold):
    """Apply color coding to results based on threshold"""
    def highlight_high_risk(val):
        if pd.isna(val):
            return ''
        try:
            if float(val) >= threshold:
                return 'background-color: #ffebee; color: #c62828; font-weight: bold'
            elif float(val) >= threshold * 0.7:
                return 'background-color: #fff3e0; color: #ef6c00'
            else:
                return 'background-color: #e8f5e8; color: #2e7d32'
        except (ValueError, TypeError):
            return ''
    
    return df.style.applymap(highlight_high_risk)

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

# Threshold setting
threshold = st.sidebar.slider(
    "Risk Threshold", 
    min_value=0.0, 
    max_value=1.0, 
    value=0.7, 
    step=0.05,
    help="Values above this threshold will be highlighted in red"
)

# Reset button
if st.sidebar.button("🔄 Reset", type="secondary", use_container_width=True):
    st.session_state.results = None
    st.session_state.evaluated_text = ""
    st.rerun()

st.sidebar.markdown("---")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📝 Text Input")
    
    # Text input area
    user_text = st.text_area(
        "Enter text to evaluate:",
        height=150,
        placeholder="Type or paste your text here...",
        help="Enter the text content you want to analyze with AI guardrails"
    )
    
    # Advanced options expander
    with st.expander("🔧 Advanced Options"):
        col_a, col_b = st.columns(2)
        
        with col_a:
            system_prompt = st.text_area(
                "System Prompt (for Topic Relevance & Prompt Safety):",
                height=100,
                placeholder="Optional: Enter system prompt for advanced metrics...",
                help="Required for Topic Relevance and Prompt Safety Risk metrics"
            )
        
        with col_b:
            context_text = st.text_area(
                "Context (for RAG metrics):",
                height=100,
                placeholder="Optional: Enter context for RAG evaluation...",
                help="Required for Answer Relevance, Context Relevance, and Faithfulness metrics"
            )
            
            generated_text = st.text_input(
                "Generated Response (for RAG metrics):",
                placeholder="Optional: Enter AI-generated response...",
                help="Required for RAG metrics evaluation"
            )

with col2:
    st.header("🛡️ Select Guardrails")
    
    # Content Safety Metrics
    st.subheader("Content Safety")
    available_metrics = get_available_metrics()
    selected_metrics = []
    
    for metric_name, metric_info in available_metrics.items():
        if st.checkbox(metric_name, help=metric_info["description"]):
            selected_metrics.append(metric_info)
    
    # RAG Metrics
    st.subheader("RAG Evaluation")
    rag_metrics = get_rag_metrics()
    
    for metric_name, metric_info in rag_metrics.items():
        if st.checkbox(metric_name, help=metric_info["description"]):
            selected_metrics.append(metric_info)
    
    # Advanced Metrics
    st.subheader("Advanced Metrics")
    advanced_metrics = get_advanced_metrics()
    
    for metric_name, metric_info in advanced_metrics.items():
        if st.checkbox(metric_name, help=metric_info["description"]):
            selected_metrics.append(metric_info)

# Run guardrails button
st.markdown("---")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    run_button = st.button(
        "🚀 Run Guardrails", 
        type="primary", 
        use_container_width=True,
        disabled=not user_text or not selected_metrics
    )

# Results section
if run_button and user_text and selected_metrics:
    with st.spinner("🔍 Evaluating content with selected guardrails..."):
        evaluator = initialize_evaluator()
        
        if evaluator:
            try:
                # Prepare metrics list
                metrics_to_run = []
                
                for metric_info in selected_metrics:
                    if 'requires_system_prompt' in metric_info and metric_info['requires_system_prompt']:
                        if system_prompt:
                            # For metrics that require system prompt
                            metric_class = metric_info['metric']
                            metrics_to_run.append(metric_class(system_prompt=system_prompt))
                        else:
                            st.warning(f"⚠️ System prompt required for {metric_info.get('description', 'this metric')}")
                            continue
                    else:
                        metrics_to_run.append(metric_info['metric'])
                
                if metrics_to_run:
                    # Prepare evaluation data
                    eval_data = {"input_text": user_text}
                    
                    # Add context and generated text for RAG metrics if provided
                    if context_text:
                        eval_data["context"] = [context_text]
                    if generated_text:
                        eval_data["generated_text"] = generated_text
                    
                    # Run evaluation
                    result = evaluator.evaluate(data=eval_data, metrics=metrics_to_run)
                    
                    # Store results in session state
                    st.session_state.results = result.to_df()
                    st.session_state.evaluated_text = user_text
                    
                    st.success("✅ Evaluation completed successfully!")
                else:
                    st.error("❌ No valid metrics to run. Please check your selections and inputs.")
                    
            except Exception as e:
                st.error(f"❌ Error during evaluation: {str(e)}")

# Display results
if st.session_state.results is not None:
    st.markdown("---")
    st.header("📊 Guardrail Results")
    
    # Show evaluated text
    with st.expander("📝 Evaluated Text", expanded=False):
        st.text(st.session_state.evaluated_text)
    
    # Display results table
    results_df = st.session_state.results
    
    if not results_df.empty:
        st.markdown(f"**Risk Threshold:** {threshold} (values above threshold are highlighted in red)")
        
        # Style and display the table
        styled_df = style_results_table(results_df, threshold)
        st.dataframe(styled_df, use_container_width=True)
        
        # Summary statistics
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        
        with col_stats1:
            high_risk_count = (results_df.select_dtypes(include=['number']) >= threshold).sum().sum()
            st.metric("High Risk Detections", high_risk_count)
        
        with col_stats2:
            max_score = results_df.select_dtypes(include=['number']).max().max()
            st.metric("Highest Risk Score", f"{max_score:.3f}" if pd.notna(max_score) else "N/A")
        
        with col_stats3:
            avg_score = results_df.select_dtypes(include=['number']).mean().mean()
            st.metric("Average Risk Score", f"{avg_score:.3f}" if pd.notna(avg_score) else "N/A")
        
        # Download results
        csv = results_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name=f"guardrail_results_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ No results to display.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit and IBM watsonx.governance</p>
        <p><small>Ensure your .env file contains valid WATSONX_APIKEY and WXG_SERVICE_INSTANCE_ID</small></p>
    </div>
    """, 
    unsafe_allow_html=True
)