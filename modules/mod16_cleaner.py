"""
AgroBiometrix: Interactive Agricultural Data Cleaning & Transformation Studio (Suite 2)
Provides full interactive missing data imputation, outlier winsorization/trimming,
biological range bounds, treatment factor harmonization, and agronomic transformations.
"""

import os
import numpy as np
import pandas as pd
import streamlit as pd_st  # will use st directly
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from datetime import datetime


def _is_fr():
    return st.session_state.get("app_lang", "en") == "fr"


def log_cleaning_action(action_desc: str):
    """Appends an action to the session cleaning history audit log."""
    if "cleaning_history" not in st.session_state:
        st.session_state["cleaning_history"] = []
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state["cleaning_history"].append(f"[{timestamp}] {action_desc}")


def render_data_cleaning_studio():
    """
    Main interactive entry point for the Data Cleaning & Transformation Studio.
    """
    is_fr = _is_fr()

    if is_fr:
        st.markdown("### 🧹 Studio Interactif de Nettoyage & Transformation des Données")
        st.caption(
            "Nettoyage biométrique de bout en bout : imputation des données manquantes (moyenne globale ou par traitement), "
            "détection et winsorisation des valeurs aberrantes (IQR / bornes biologiques), harmonisation des facteurs et export certifié."
        )
    else:
        st.markdown("### 🧹 Interactive Agricultural Data Cleaning & Transformation Studio")
        st.caption(
            "End-to-end biometrical data sanitation: missing value imputation (global or group-aware), "
            "outlier detection & winsorization (Tukey IQR / biological bounds), treatment harmonization, and audit-ready export."
        )

    # -------------------------------------------------------------
    # DATASET INGESTION & SELECTION
    # -------------------------------------------------------------
    if is_fr:
        src_label = "Source du Jeu de Données à Nettoyer :"
        src_options = [
            "🧪 Charger l'Essai Champêtre avec Anomalies (Démonstration)",
            "🌽 Charger l'Essai Agronomique Maïs (NPK x Irrigation)",
            "🐄 Charger l'Essai Tolérance Bovine",
            "📁 Téléverser un Fichier CSV / Excel Personnalisé"
        ]
    else:
        src_label = "Choose Dataset Source to Clean:"
        src_options = [
            "🧪 Load Messy Field Trial with Anomalies (Demonstration)",
            "🌽 Load Pre-loaded Maize Agronomy Trial (NPK x Irrigation)",
            "🐄 Load Pre-loaded Cattle Trial",
            "📁 Upload Custom CSV / Excel File"
        ]

    data_source = st.radio(src_label, src_options, horizontal=True, key="cleaner_data_source")

    # Handle dataset loading into session state
    df_loaded = None
    ds_name = "dataset"

    if data_source in ["🧪 Load Messy Field Trial with Anomalies (Demonstration)", "🧪 Charger l'Essai Champêtre avec Anomalies (Démonstration)"]:
        messy_path = os.path.join("data", "sample_messy_field_trial.csv")
        if os.path.exists(messy_path):
            df_loaded = pd.read_csv(messy_path)
            ds_name = "messy_field_trial"
        else:
            st.error("Demonstration dataset not found on disk.")
    elif data_source in ["🌽 Load Pre-loaded Maize Agronomy Trial (NPK x Irrigation)", "🌽 Charger l'Essai Agronomique Maïs (NPK x Irrigation)"]:
        maize_path = os.path.join("data", "sample_maize_agronomy_trials.csv")
        if os.path.exists(maize_path):
            df_loaded = pd.read_csv(maize_path)
            ds_name = "maize_agronomy_trial"
    elif data_source in ["🐄 Load Pre-loaded Cattle Trial", "🐄 Charger l'Essai Tolérance Bovine"]:
        cattle_path = os.path.join("data", "sample_cattle_heat_tolerance.csv")
        if os.path.exists(cattle_path):
            df_loaded = pd.read_csv(cattle_path)
            ds_name = "cattle_trial"
    else:
        up_label = "Téléverser un jeu de données expérimental (CSV ou Excel)" if is_fr else "Upload Experimental Dataset (CSV or Excel)"
        up_file = st.file_uploader(up_label, type=["csv", "xlsx", "xls"], key="cleaner_file_uploader")
        if up_file is not None:
            try:
                if up_file.name.endswith(".csv"):
                    df_loaded = pd.read_csv(up_file)
                else:
                    df_loaded = pd.read_excel(up_file)
                ds_name = up_file.name.split('.')[0]
            except Exception as e:
                st.error(f"Error loading file: {e}")

    # Synchronize with session state
    current_src_key = f"cleaner_loaded_src_{ds_name}"
    if df_loaded is not None:
        if st.session_state.get("cleaner_current_dataset") != current_src_key:
            st.session_state["cleaning_raw_df"] = df_loaded.copy()
            st.session_state["cleaning_active_df"] = df_loaded.copy()
            st.session_state["cleaning_history"] = [
                f"[{datetime.now().strftime('%H:%M:%S')}] Dataset '{ds_name}' loaded ({len(df_loaded)} rows, {len(df_loaded.columns)} columns)."
            ]
            st.session_state["cleaner_current_dataset"] = current_src_key

    if "cleaning_active_df" not in st.session_state or st.session_state["cleaning_active_df"] is None:
        st.info("👋 Veuillez sélectionner ou téléverser un jeu de données pour démarrer le nettoyage." if is_fr else "👋 Please select or upload a dataset above to start data cleaning.")
        return

    df_active = st.session_state["cleaning_active_df"]
    df_raw = st.session_state.get("cleaning_raw_df", df_active)

    # -------------------------------------------------------------
    # TOP STATUS DASHBOARD & REVERSIBILITY CONTROLS
    # -------------------------------------------------------------
    st.markdown("---")
    
    # Calculate real-time health metrics
    n_rows, n_cols = df_active.shape
    raw_rows, _ = df_raw.shape
    row_delta = n_rows - raw_rows

    total_cells = n_rows * n_cols
    missing_count = int(df_active.isnull().sum().sum())
    missing_pct = (missing_count / total_cells * 100) if total_cells > 0 else 0.0

    dup_count = int(df_active.duplicated().sum())

    # Count outliers across all numeric columns via 1.5 IQR
    num_cols = df_active.select_dtypes(include=[np.number]).columns.tolist()
    total_outliers = 0
    for col in num_cols:
        series = df_active[col].dropna()
        if len(series) >= 4:
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            if iqr > 0:
                low = q1 - 1.5 * iqr
                high = q3 + 1.5 * iqr
                total_outliers += int(((series < low) | (series > high)).sum())

    # Metric Cards
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric(
        "Enregistrements" if is_fr else "Total Rows",
        f"{n_rows:,}",
        delta=f"{row_delta} vs Raw" if row_delta != 0 else None
    )
    c2.metric("Variables" if is_fr else "Columns", f"{n_cols}")
    c3.metric(
        "Valeurs Manquantes" if is_fr else "Missing Cells",
        f"{missing_count:,}",
        delta=f"{missing_pct:.1f}%" if missing_count > 0 else "0% (Clean)",
        delta_color="inverse"
    )
    c4.metric(
        "Lignes Dupliquées" if is_fr else "Duplicate Rows",
        f"{dup_count:,}",
        delta="Needs Dedup" if dup_count > 0 else "Zero",
        delta_color="inverse"
    )
    c5.metric(
        "Valeurs Aberrantes (IQR)" if is_fr else "IQR Outliers",
        f"{total_outliers:,}",
        delta="Suspicious" if total_outliers > 0 else "Normal",
        delta_color="inverse"
    )

    # Action Toolbar
    tb1, tb2, tb3 = st.columns([2, 1, 1])
    with tb2:
        if st.button("🔄 " + ("Réinitialiser à l'Original" if is_fr else "Reset to Original Raw"), key="btn_reset_cleaning"):
            st.session_state["cleaning_active_df"] = df_raw.copy()
            log_cleaning_action("Dataset reset to original raw state.")
            st.rerun()
    with tb3:
        if st.button("✨ " + ("Diffuser vers Biométrie" if is_fr else "Send to Biometrics & ANOVA"), key="btn_push_to_biometrics"):
            st.session_state["cleaned_active_df"] = df_active.copy()
            st.session_state["cleaned_active_name"] = ds_name
            st.success("✅ " + ("Jeu de données nettoyé synchronisé avec la Suite Biométrie !" if is_fr else "Cleaned dataset synchronized with Biometrics Suite!"))

    # Preview Collapsible
    with st.expander("👁️ " + ("Aperçu du Jeu de Données Actuel" if is_fr else "Preview Active Dataset"), expanded=False):
        st.dataframe(df_active.head(10), use_container_width=True)

    # -------------------------------------------------------------
    # 5 FUNCTIONAL CLEANING TABS
    # -------------------------------------------------------------
    if is_fr:
        tab_names = [
            "🧩 1. Données Manquantes",
            "🎯 2. Valeurs Aberrantes & Bornes",
            "🏷️ 3. Harmonisation des Facteurs",
            "📐 4. Transformations Agronomiques",
            "📜 5. Journal d'Audit & Export"
        ]
    else:
        tab_names = [
            "🧩 1. Missing Values",
            "🎯 2. Outliers & Range Bounds",
            "🏷️ 3. Treatment Harmonization",
            "📐 4. Agronomic Transforms",
            "📜 5. Audit Log & Export"
        ]

    tab_miss, tab_out, tab_text, tab_trans, tab_audit = st.tabs(tab_names)

    # -------------------------------------------------------------
    # TAB 1: MISSING VALUE IMPUTATION
    # -------------------------------------------------------------
    with tab_miss:
        st.markdown("#### 🧩 " + ("Gestion & Imputation des Données Manquantes" if is_fr else "Missing Data Diagnostics & Imputation"))
        
        miss_summary = df_active.isnull().sum()
        cols_with_miss = miss_summary[miss_summary > 0]

        if cols_with_miss.empty:
            st.success("🎉 " + ("Aucune valeur manquante détectée dans ce jeu de données ! Les analyses biométriques sont valides." if is_fr else "No missing values detected in this dataset! Complete case analysis is valid."))
        else:
            st.warning(
                f"⚠️ **{len(cols_with_miss)}** " + 
                (f"colonnes contiennent des valeurs manquantes ({missing_count} cellules au total)." if is_fr else f"columns contain missing data ({missing_count} total cells).")
            )
            
            # Table of missing details
            miss_df = pd.DataFrame({
                "Column": cols_with_miss.index,
                "Type": [df_active[c].dtype for c in cols_with_miss.index],
                "Missing Count": cols_with_miss.values,
                "Missing %": [(v / n_rows * 100) for v in cols_with_miss.values]
            })
            st.dataframe(miss_df.style.format({"Missing %": "{:.1f}%"}), use_container_width=True)

            st.markdown("##### " + ("Options d'Imputation Biométrique" if is_fr else "Biometrical Imputation Strategies"))
            
            # Quick Global Operations
            q_col1, q_col2 = st.columns(2)
            with q_col1:
                if st.button("🗑️ " + ("Supprimer les Lignes avec Manquants (Cas Complets)" if is_fr else "Drop Rows with Missing Values (Complete Cases)"), key="btn_drop_na_rows"):
                    before_n = len(df_active)
                    df_active = df_active.dropna().reset_index(drop=True)
                    st.session_state["cleaning_active_df"] = df_active
                    dropped = before_n - len(df_active)
                    log_cleaning_action(f"Dropped {dropped} rows containing missing values (Complete Case Analysis).")
                    st.success(f"Removed {dropped} rows.")
                    st.rerun()

            with q_col2:
                col_thresh = st.slider("Drop columns with missingness exceeding %:", min_value=10, max_value=90, value=50, step=5, key="slider_miss_thresh")
                if st.button("✂️ " + ("Élaguer les Colonnes Hautement Incomplètes" if is_fr else "Drop Highly Incomplete Columns"), key="btn_drop_na_cols"):
                    before_cols = df_active.columns.tolist()
                    thresh_val = col_thresh / 100.0
                    to_drop = [c for c in cols_with_miss.index if (df_active[c].isnull().sum() / n_rows) >= thresh_val]
                    if to_drop:
                        df_active = df_active.drop(columns=to_drop)
                        st.session_state["cleaning_active_df"] = df_active
                        log_cleaning_action(f"Dropped {len(to_drop)} columns exceeding {col_thresh}% missingness: {to_drop}")
                        st.success(f"Dropped columns: {to_drop}")
                        st.rerun()
                    else:
                        st.info("No columns exceeded the selected threshold.")

            st.markdown("---")
            st.markdown("##### " + ("Imputation Ciblée par Colonne" if is_fr else "Column-Specific Targeted Imputation"))

            target_miss_col = st.selectbox(
                "Select Column to Impute:" if not is_fr else "Sélectionner la Colonne à Imputer :",
                cols_with_miss.index.tolist(),
                key="select_miss_col"
            )

            is_col_num = np.issubdtype(df_active[target_miss_col].dtype, np.number)
            
            if is_col_num:
                impute_methods = [
                    "Global Median (Recommended for Skewed Field Yields)",
                    "Global Mean (Standard for Normal Agronomic Traits)",
                    "Group-Aware Mean by Treatment / Block (Agronomic Gold Standard)",
                    "Constant Value (e.g., 0)"
                ]
            else:
                impute_methods = [
                    "Most Frequent Value (Mode)",
                    "Constant Label (e.g., 'Unobserved' or 'Missing')"
                ]

            imp_choice = st.selectbox(
                "Choose Imputation Method:" if not is_fr else "Choisir la Méthode d'Imputation :",
                impute_methods,
                key="select_imp_method"
            )

            group_col_selected = None
            const_val_input = None

            if "Group-Aware Mean" in imp_choice:
                cat_candidates = df_active.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
                if not cat_candidates:
                    cat_candidates = [c for c in df_active.columns if c != target_miss_col]
                group_col_selected = st.selectbox(
                    "Select Grouping Factor (e.g., Treatment, Genotype, Block):" if not is_fr else "Sélectionner le Facteur de Regroupement (ex: Traitement, Bloc) :",
                    cat_candidates,
                    key="select_group_for_impute"
                )
            elif "Constant Value" in imp_choice or "Constant Label" in imp_choice:
                const_val_input = st.text_input(
                    "Enter Constant Value:" if not is_fr else "Entrer la Valeur Constante :",
                    value="0" if is_col_num else "Missing",
                    key="input_const_val"
                )

            if st.button("🚀 " + ("Appliquer l'Imputation" if is_fr else "Apply Imputation to Column"), key="btn_apply_impute"):
                missing_in_target = int(df_active[target_miss_col].isnull().sum())
                
                if "Global Median" in imp_choice:
                    med_val = df_active[target_miss_col].median()
                    df_active[target_miss_col] = df_active[target_miss_col].fillna(med_val)
                    log_cleaning_action(f"Imputed {missing_in_target} missing values in '{target_miss_col}' using Global Median ({med_val:.3f}).")
                elif "Global Mean" in imp_choice:
                    mean_val = df_active[target_miss_col].mean()
                    df_active[target_miss_col] = df_active[target_miss_col].fillna(mean_val)
                    log_cleaning_action(f"Imputed {missing_in_target} missing values in '{target_miss_col}' using Global Mean ({mean_val:.3f}).")
                elif "Group-Aware Mean" in imp_choice and group_col_selected:
                    # Impute missing within each group mean, fallback to global mean
                    group_means = df_active.groupby(group_col_selected)[target_miss_col].transform('mean')
                    df_active[target_miss_col] = df_active[target_miss_col].fillna(group_means)
                    # Any remaining filled with global mean
                    global_mean = df_active[target_miss_col].mean()
                    df_active[target_miss_col] = df_active[target_miss_col].fillna(global_mean)
                    log_cleaning_action(f"Imputed {missing_in_target} missing values in '{target_miss_col}' using Group-Aware Mean on '{group_col_selected}'.")
                elif "Most Frequent" in imp_choice:
                    mode_val = df_active[target_miss_col].mode()
                    if not mode_val.empty:
                        df_active[target_miss_col] = df_active[target_miss_col].fillna(mode_val[0])
                        log_cleaning_action(f"Imputed {missing_in_target} missing values in '{target_miss_col}' using Mode ('{mode_val[0]}').")
                elif const_val_input is not None:
                    try:
                        val_to_use = float(const_val_input) if is_col_num else str(const_val_input)
                    except ValueError:
                        val_to_use = str(const_val_input)
                    df_active[target_miss_col] = df_active[target_miss_col].fillna(val_to_use)
                    log_cleaning_action(f"Imputed {missing_in_target} missing values in '{target_miss_col}' using Constant '{val_to_use}'.")

                st.session_state["cleaning_active_df"] = df_active
                st.success("✅ " + (f"Imputation réussie pour '{target_miss_col}' !" if is_fr else f"Successfully imputed '{target_miss_col}'!"))
                st.rerun()

    # -------------------------------------------------------------
    # TAB 2: OUTLIER DETECTION & BIOLOGICAL BOUNDS
    # -------------------------------------------------------------
    with tab_out:
        st.markdown("#### 🎯 " + ("Détection & Traitement des Valeurs Aberrantes" if is_fr else "Outlier Detection, Trimming & Biological Bounds"))
        
        if not num_cols:
            st.info("No numeric columns found in this dataset.")
        else:
            target_num_col = st.selectbox(
                "Select Numerical Trait to Inspect:" if not is_fr else "Sélectionner la Variable Numérique à Inspecter :",
                num_cols,
                key="select_outlier_col"
            )

            series_clean = df_active[target_num_col].dropna()
            
            if len(series_clean) < 4:
                st.warning("Insufficient non-null observations for outlier detection.")
            else:
                q1 = series_clean.quantile(0.25)
                q3 = series_clean.quantile(0.75)
                iqr = q3 - q1
                iqr_low = q1 - 1.5 * iqr
                iqr_high = q3 + 1.5 * iqr

                mean_val = series_clean.mean()
                std_val = series_clean.std()
                z_low = mean_val - 3 * std_val
                z_high = mean_val + 3 * std_val

                # Outlier method selection
                out_method = st.radio(
                    "Detection Method:" if not is_fr else "Méthode de Détection :",
                    ["Tukey IQR Rule (1.5x IQR)", "Tukey Extreme Outliers (3.0x IQR)", "Z-Score (±3 Standard Deviations)", "Biological Domain Bounds (Min - Max)"],
                    horizontal=True,
                    key="radio_out_method"
                )

                if "1.5x IQR" in out_method:
                    lower_bound, upper_bound = iqr_low, iqr_high
                elif "3.0x IQR" in out_method:
                    lower_bound, upper_bound = q1 - 3.0 * iqr, q3 + 3.0 * iqr
                elif "Z-Score" in out_method:
                    lower_bound, upper_bound = z_low, z_high
                else:
                    # Biological custom bounds
                    b_col1, b_col2 = st.columns(2)
                    with b_col1:
                        lower_bound = st.number_input(
                            "Minimum Biological Feasible Bound:" if not is_fr else "Borne Biologique Minimale :",
                            value=float(np.floor(series_clean.min())),
                            key="input_bio_low"
                        )
                    with b_col2:
                        upper_bound = st.number_input(
                            "Maximum Biological Feasible Bound:" if not is_fr else "Borne Biologique Maximale :",
                            value=float(np.ceil(series_clean.max())),
                            key="input_bio_high"
                        )

                # Identify flagged rows
                outlier_mask = (df_active[target_num_col] < lower_bound) | (df_active[target_num_col] > upper_bound)
                outlier_rows = df_active[outlier_mask]
                n_flagged = len(outlier_rows)

                m_c1, m_c2, m_c3 = st.columns(3)
                m_c1.metric("Lower Bound", f"{lower_bound:.2f}")
                m_c2.metric("Upper Bound", f"{upper_bound:.2f}")
                m_c3.metric(
                    "Flagged Outliers" if not is_fr else "Valeurs Aberrantes",
                    f"{n_flagged:,}",
                    delta=f"{(n_flagged / len(series_clean) * 100):.1f}%" if n_flagged > 0 else "Clean",
                    delta_color="inverse"
                )

                if n_flagged > 0:
                    st.warning(f"⚠️ Flagged **{n_flagged}** observations outside [{lower_bound:.2f}, {upper_bound:.2f}]:")
                    st.dataframe(outlier_rows[[target_num_col]], use_container_width=True)

                    st.markdown("##### " + ("Traitement des Valeurs Aberrantes" if is_fr else "Outlier Remediation Actions"))
                    
                    act_col1, act_col2, act_col3 = st.columns(3)
                    with act_col1:
                        if st.button("🛡️ " + ("Winsoriser (Plafonner aux Bornes)" if is_fr else "Winsorize (Cap to Bounds)"), key="btn_winsorize"):
                            df_active[target_num_col] = df_active[target_num_col].clip(lower=lower_bound, upper=upper_bound)
                            st.session_state["cleaning_active_df"] = df_active
                            log_cleaning_action(f"Winsorized {n_flagged} outliers in '{target_num_col}' to bounds [{lower_bound:.2f}, {upper_bound:.2f}].")
                            st.success("✅ Capped outliers to threshold bounds.")
                            st.rerun()

                    with act_col2:
                        if st.button("❓ " + ("Convertir en Manquants (NaN)" if is_fr else "Convert to NaN (For Imputation)"), key="btn_outlier_to_nan"):
                            df_active.loc[outlier_mask, target_num_col] = np.nan
                            st.session_state["cleaning_active_df"] = df_active
                            log_cleaning_action(f"Converted {n_flagged} outliers in '{target_num_col}' to NaN.")
                            st.success("✅ Converted outliers to NaN.")
                            st.rerun()

                    with act_col3:
                        if st.button("🗑️ " + ("Supprimer les Lignes Aberrantes" if is_fr else "Drop Outlier Rows"), key="btn_drop_outlier_rows"):
                            before_n = len(df_active)
                            df_active = df_active[~outlier_mask].reset_index(drop=True)
                            st.session_state["cleaning_active_df"] = df_active
                            log_cleaning_action(f"Dropped {n_flagged} outlier rows in '{target_num_col}'.")
                            st.success(f"Removed {n_flagged} rows.")
                            st.rerun()

                # Visual distribution boxplot
                fig = px.box(
                    df_active,
                    y=target_num_col,
                    points="all",
                    color_discrete_sequence=["#1B5E20"],
                    title=f"Distribution & Outlier Boundary Analysis: {target_num_col}"
                )
                fig.add_hline(y=lower_bound, line_dash="dash", line_color="#BA0C2F", annotation_text=f"Lower Bound ({lower_bound:.2f})")
                fig.add_hline(y=upper_bound, line_dash="dash", line_color="#BA0C2F", annotation_text=f"Upper Bound ({upper_bound:.2f})")
                st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------------
    # TAB 3: TREATMENT & TEXT HARMONIZATION
    # -------------------------------------------------------------
    with tab_text:
        st.markdown("#### 🏷️ " + ("Harmonisation des Traitements & Normalisation du Texte" if is_fr else "Treatment Harmonization & String Sanitation"))
        
        # Batch quick cleans
        st.markdown("##### " + ("Nettoyages Rapides en Lot" if is_fr else "Batch Quick Actions"))
        q1, q2, q3 = st.columns(3)
        
        with q1:
            if st.button("✂️ " + ("Élaguer les Espaces Inutiles" if is_fr else "Trim Whitespace (All Columns)"), key="btn_trim_spaces"):
                str_cols = df_active.select_dtypes(include=['object', 'string']).columns.tolist()
                for c in str_cols:
                    df_active[c] = df_active[c].astype(str).str.strip()
                st.session_state["cleaning_active_df"] = df_active
                log_cleaning_action("Trimmed leading and trailing whitespace across all string columns.")
                st.success("✅ Stripped whitespace across all text columns.")
                st.rerun()

        with q2:
            if st.button("🧼 " + ("Supprimer les Doublons Exacts" if is_fr else "Remove Exact Duplicate Rows"), key="btn_remove_duplicates"):
                before_d = len(df_active)
                df_active = df_active.drop_duplicates().reset_index(drop=True)
                removed_dups = before_d - len(df_active)
                st.session_state["cleaning_active_df"] = df_active
                log_cleaning_action(f"Removed {removed_dups} duplicate rows.")
                st.success(f"Removed {removed_dups} duplicate rows.")
                st.rerun()

        with q3:
            if st.button("🏷️ " + ("Normaliser les En-têtes (snake_case)" if is_fr else "Sanitize Headers (snake_case)"), key="btn_sanitize_headers"):
                clean_cols = [
                    c.strip().replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "").replace("/", "_").replace("#", "num")
                    for c in df_active.columns
                ]
                df_active.columns = clean_cols
                st.session_state["cleaning_active_df"] = df_active
                log_cleaning_action(f"Normalized column headers to snake_case format: {clean_cols}")
                st.success("✅ Normalized headers to clean snake_case format.")
                st.rerun()

        st.markdown("---")
        st.markdown("##### " + ("Harmonisation des Niveaux de Facteurs (Traitements)" if is_fr else "Factor Level Value Harmonizer (e.g., merging 'CTRL' and 'Control')"))
        
        cat_cols = df_active.select_dtypes(include=['object', 'category', 'string']).columns.tolist()
        if not cat_cols:
            st.info("No categorical/text columns found for harmonization.")
        else:
            target_cat = st.selectbox(
                "Select Factor / Categorical Column:" if not is_fr else "Sélectionner la Colonne Catégorielle :",
                cat_cols,
                key="select_cat_harmonize"
            )

            val_counts = df_active[target_cat].value_counts(dropna=False)
            st.markdown(f"**Current Unique Levels in `{target_cat}` ({len(val_counts)} levels):**")
            
            # Show interactive counts
            cnt_df = pd.DataFrame({"Factor Level": val_counts.index.astype(str), "Count": val_counts.values})
            st.dataframe(cnt_df, use_container_width=True)

            h_c1, h_c2, h_c3 = st.columns([2, 2, 1])
            with h_c1:
                val_to_replace = st.selectbox(
                    "Value to Replace:" if not is_fr else "Valeur à Remplacer :",
                    val_counts.index.astype(str).tolist(),
                    key="sel_val_to_replace"
                )
            with h_c2:
                target_new_val = st.text_input(
                    "Replace With Target Standard Value:" if not is_fr else "Remplacer par la Valeur Standard :",
                    value=val_to_replace.strip().title(),
                    key="input_new_val_target"
                )
            with h_c3:
                st.write("")
                st.write("")
                if st.button("Apply Mapping" if not is_fr else "Remplacer", key="btn_apply_mapping"):
                    n_replaced = (df_active[target_cat].astype(str) == val_to_replace).sum()
                    df_active[target_cat] = df_active[target_cat].astype(str).replace({val_to_replace: target_new_val})
                    st.session_state["cleaning_active_df"] = df_active
                    log_cleaning_action(f"Mapped {n_replaced} occurrences of '{val_to_replace}' -> '{target_new_val}' in column '{target_cat}'.")
                    st.success(f"Harmonized {n_replaced} rows.")
                    st.rerun()

    # -------------------------------------------------------------
    # TAB 4: AGRONOMIC TRANSFORMATIONS
    # -------------------------------------------------------------
    with tab_trans:
        st.markdown("#### 📐 " + ("Transformations Agronomiques Spécialisées" if is_fr else "Specialized Agronomic Variance-Stabilizing Transformations"))
        st.caption(
            "Agricultural field trial data frequently violate ANOVA homoscedasticity and normality assumptions. "
            "Applying mathematical transformations restores Gaussian properties before running F-tests."
        )

        if not num_cols:
            st.info("No numeric columns available for transformation.")
        else:
            trans_col = st.selectbox(
                "Select Variable to Transform:" if not is_fr else "Sélectionner la Variable à Transformer :",
                num_cols,
                key="select_trans_col"
            )

            trans_type = st.radio(
                "Transformation Type:" if not is_fr else "Type de Transformation :",
                [
                    "Logarithmic: log10(x + 1) (For highly skewed positive biological traits)",
                    "Square Root: sqrt(x + 0.5) (For Poisson-distributed pest or count data)",
                    "Arcsine Square Root: arcsin(sqrt(p / 100)) (For percentage/proportion data like disease %)",
                    "Z-Score Standardization: (x - μ) / σ (Zero mean, unit variance)"
                ],
                key="radio_trans_type"
            )

            dest_name = st.text_input(
                "New Column Name:" if not is_fr else "Nom de la Nouvelle Colonne :",
                value=f"{trans_col}_transformed",
                key="input_trans_dest_name"
            )

            if st.button("🚀 " + ("Exécuter la Transformation" if is_fr else "Apply Transformation"), key="btn_execute_trans"):
                series_v = df_active[trans_col].copy()
                
                try:
                    if "Logarithmic" in trans_type:
                        transformed = np.log10(np.maximum(series_v + 1.0, 1e-9))
                    elif "Square Root" in trans_type:
                        transformed = np.sqrt(np.maximum(series_v + 0.5, 0.0))
                    elif "Arcsine" in trans_type:
                        p_norm = np.clip(series_v / 100.0, 0.0, 1.0)
                        transformed = np.arcsin(np.sqrt(p_norm))
                    else:
                        m_v = series_v.mean()
                        s_v = series_v.std()
                        transformed = (series_v - m_v) / (s_v if s_v > 0 else 1.0)

                    df_active[dest_name] = transformed
                    st.session_state["cleaning_active_df"] = df_active
                    log_cleaning_action(f"Created transformed column '{dest_name}' from '{trans_col}' using {trans_type[:20]}.")
                    st.success(f"✅ Generated transformed column '{dest_name}'.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Transformation failed: {e}")

    # -------------------------------------------------------------
    # TAB 5: AUDIT LOG & EXPORT
    # -------------------------------------------------------------
    with tab_audit:
        st.markdown("#### 📜 " + ("Journal d'Audit des Nettoyages & Export Certifié" if is_fr else "Cleaning Audit Trail & Certified Dataset Export"))
        
        # Display Audit History
        history = st.session_state.get("cleaning_history", [])
        if history:
            st.markdown("##### " + ("Historique des Opérations Réalisées" if is_fr else "Step-by-Step Cleaning History"))
            for entry in history:
                st.text(entry)
        else:
            st.info("No cleaning actions recorded yet.")

        st.markdown("---")
        st.markdown("##### " + ("Téléchargement du Jeu de Données Nettoyé" if is_fr else "Download Sanitized Dataset"))

        csv_bytes = df_active.to_csv(index=False).encode('utf-8')
        export_filename = f"cleaned_{ds_name}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.download_button(
                label="📥 " + ("Télécharger le Fichier CSV Nettoyé" if is_fr else "Download Cleaned CSV Dataset"),
                data=csv_bytes,
                file_name=export_filename,
                mime="text/csv",
                key="btn_download_cleaned_csv"
            )
        with d_col2:
            if st.button("🚀 " + ("Envoyer vers la Suite Biométrique (DMRT/ANOVA)" if is_fr else "Send Directly to Biometrics & ANOVA Suite"), key="btn_final_send_biometrics"):
                st.session_state["cleaned_active_df"] = df_active.copy()
                st.session_state["cleaned_active_name"] = ds_name
                st.balloons()
                st.success("🎉 " + ("Jeu de données synchronisé avec succès ! Rendez-vous sur l'onglet 'Statistiques Biométriques & DMRT'." if is_fr else "Dataset successfully synchronized! Head to the 'Statistical Biometrics & DMRT' tab to analyze."))
