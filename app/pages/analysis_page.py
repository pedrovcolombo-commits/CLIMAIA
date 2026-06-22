"""
CLIMAIA – Analysis Page
Configure and run extreme event detection on loaded datasets.
"""

import customtkinter as ctk
import pandas as pd
from datetime import datetime
from app.theme import Colors, Fonts, Spacing
from app.components import (SectionHeader, ActionButton, LabeledEntry,
                             LabeledOptionMenu, ConsoleBox, StatusBadge)


class AnalysisPage(ctk.CTkFrame):
    """Analysis configuration and execution page."""

    def __init__(self, master, app_ref=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.app = app_ref
        self._build_ui()
        self._refresh_from_data()

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                         scrollbar_button_color=Colors.BORDER,
                                         scrollbar_button_hover_color=Colors.BORDER_LIGHT)
        scroll.pack(fill="both", expand=True)
        self._scroll = scroll

        # ── Header ────────────────────────────────────────────────────────
        ctk.CTkLabel(scroll, text="Análise de Eventos Extremos",
                     font=Fonts.HERO, text_color=Colors.TEXT_PRIMARY,
                     anchor="w").pack(fill="x")
        ctk.CTkLabel(scroll, text="Configure os parâmetros e execute a detecção estatística",
                     font=Fonts.BODY, text_color=Colors.TEXT_MUTED,
                     anchor="w").pack(fill="x", pady=(4, Spacing.XL))

        # ── Data Status Banner ────────────────────────────────────────────
        self.data_banner = ctk.CTkFrame(scroll, fg_color=Colors.BG_CARD,
                                         corner_radius=Spacing.CORNER,
                                         border_width=1, border_color=Colors.BORDER)
        self.data_banner.pack(fill="x", pady=(0, Spacing.XL))

        banner_inner = ctk.CTkFrame(self.data_banner, fg_color="transparent")
        banner_inner.pack(fill="x", padx=Spacing.CARD_PAD, pady=Spacing.MD)

        self.banner_icon = ctk.CTkLabel(banner_inner, text="⚠️",
                                         font=(Fonts.FAMILY, 20))
        self.banner_icon.pack(side="left")

        self.banner_text = ctk.CTkLabel(
            banner_inner,
            text="Nenhum dado carregado. Vá para a aba 'Dados' para importar os CSVs.",
            font=Fonts.BODY, text_color=Colors.TEXT_MUTED, anchor="w")
        self.banner_text.pack(side="left", padx=(Spacing.SM, 0))

        self.banner_btn = ActionButton(
            banner_inner, text="Ir para Dados", icon="📂",
            color=Colors.PRIMARY, width=160,
            command=lambda: self.app.navigate("data") if self.app else None)
        self.banner_btn.pack(side="right")

        # ── Configuration Grid ────────────────────────────────────────────
        config_row = ctk.CTkFrame(scroll, fg_color="transparent")
        config_row.pack(fill="x", pady=(0, Spacing.XL))
        config_row.columnconfigure((0, 1), weight=1, uniform="config")

        # Left: Period selection
        left_card = ctk.CTkFrame(config_row, fg_color=Colors.BG_CARD,
                                  corner_radius=Spacing.CORNER,
                                  border_width=1, border_color=Colors.BORDER)
        left_card.grid(row=0, column=0, padx=(0, Spacing.MD), sticky="nsew")

        left_inner = ctk.CTkFrame(left_card, fg_color="transparent")
        left_inner.pack(fill="both", expand=True, padx=Spacing.CARD_PAD,
                        pady=Spacing.CARD_PAD)

        ctk.CTkLabel(left_inner, text="📅  Período de Análise", font=Fonts.H3,
                     text_color=Colors.TEXT_PRIMARY).pack(fill="x",
                         pady=(0, Spacing.MD))

        # Period preset
        self.period_preset = LabeledOptionMenu(
            left_inner, label="Período Predefinido",
            values=["Personalizado", "Último Mês", "Últimos 3 Meses",
                    "Últimos 6 Meses", "Último Ano", "Todo o Dataset"],
            default="Todo o Dataset",
            command=self._on_period_change)
        self.period_preset.pack(fill="x", pady=(0, Spacing.MD))

        # Custom date inputs
        self.custom_dates_frame = ctk.CTkFrame(left_inner, fg_color="transparent")
        self.custom_dates_frame.pack(fill="x", pady=(0, Spacing.MD))

        dates_row = ctk.CTkFrame(self.custom_dates_frame, fg_color="transparent")
        dates_row.pack(fill="x")
        dates_row.columnconfigure((0, 1), weight=1, uniform="date")

        self.date_start = LabeledEntry(dates_row, label="Data Início",
                                        placeholder="YYYY-MM-DD")
        self.date_start.grid(row=0, column=0, padx=(0, Spacing.SM), sticky="ew")

        self.date_end = LabeledEntry(dates_row, label="Data Fim",
                                      placeholder="YYYY-MM-DD")
        self.date_end.grid(row=0, column=1, sticky="ew")

        # Granularity
        self.granularity = LabeledOptionMenu(
            left_inner, label="Granularidade Temporal",
            values=["Original (sem resample)", "10 min", "Horária", "Diária",
                    "Semanal", "Mensal"],
            default="Horária")
        self.granularity.pack(fill="x")

        # Right: Method selection
        right_card = ctk.CTkFrame(config_row, fg_color=Colors.BG_CARD,
                                   corner_radius=Spacing.CORNER,
                                   border_width=1, border_color=Colors.BORDER)
        right_card.grid(row=0, column=1, sticky="nsew")

        right_inner = ctk.CTkFrame(right_card, fg_color="transparent")
        right_inner.pack(fill="both", expand=True, padx=Spacing.CARD_PAD,
                         pady=Spacing.CARD_PAD)

        ctk.CTkLabel(right_inner, text="🔬  Método Estatístico", font=Fonts.H3,
                     text_color=Colors.TEXT_PRIMARY).pack(fill="x",
                         pady=(0, Spacing.MD))

        # Statistical method
        self.method = LabeledOptionMenu(
            right_inner, label="Método de Detecção",
            values=[
                "Percentil Adaptativo (P95/P99)",
                "Teoria de Valores Extremos (EVT)",
                "Distribuição de Gumbel",
                "Z-Score (Desvio Padrão)",
                "IQR (Interquartil Range)",
                "Todos os Métodos",
            ],
            default="Percentil Adaptativo (P95/P99)")
        self.method.pack(fill="x", pady=(0, Spacing.MD))

        # Threshold
        self.threshold = LabeledEntry(
            right_inner, label="Limiar de Sensibilidade (%)",
            placeholder="95")
        self.threshold.pack(fill="x", pady=(0, Spacing.MD))
        self.threshold.set("95")

        # Target datasets
        ctk.CTkLabel(right_inner, text="Aplicar Em", font=Fonts.SMALL_BOLD,
                     text_color=Colors.TEXT_SECONDARY, anchor="w").pack(
                         fill="x")

        check_frame = ctk.CTkFrame(right_inner, fg_color="transparent")
        check_frame.pack(fill="x", pady=(Spacing.XS, 0))

        self.apply_raw = ctk.CTkCheckBox(
            check_frame, text="Dados Brutos", font=Fonts.BODY,
            fg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            border_color=Colors.BORDER_LIGHT)
        self.apply_raw.pack(anchor="w", pady=2)
        self.apply_raw.select()

        self.apply_treated = ctk.CTkCheckBox(
            check_frame, text="Dados Tratados", font=Fonts.BODY,
            fg_color=Colors.SECONDARY, hover_color=Colors.SECONDARY_HOVER,
            text_color=Colors.TEXT_PRIMARY,
            border_color=Colors.BORDER_LIGHT)
        self.apply_treated.pack(anchor="w", pady=2)
        self.apply_treated.select()

        # ── Variable Selection ────────────────────────────────────────────
        SectionHeader(scroll, title="Variáveis para Análise",
                      subtitle="Selecione quais variáveis meteorológicas serão analisadas").pack(
                          fill="x", pady=(0, Spacing.MD))

        self.var_card = ctk.CTkFrame(scroll, fg_color=Colors.BG_CARD,
                                 corner_radius=Spacing.CORNER,
                                 border_width=1, border_color=Colors.BORDER)
        self.var_card.pack(fill="x", pady=(0, Spacing.XL))

        self.var_inner = ctk.CTkFrame(self.var_card, fg_color="transparent")
        self.var_inner.pack(fill="both", padx=Spacing.CARD_PAD,
                       pady=Spacing.CARD_PAD)

        # Actions for variables
        self.var_actions = ctk.CTkFrame(self.var_inner, fg_color="transparent")
        self.var_actions.pack(fill="x", pady=(0, Spacing.SM))
        
        ActionButton(self.var_actions, text="Selecionar Todos", icon="☑️",
                     color=Colors.PRIMARY, width=150, height=28,
                     command=self._select_all_vars).pack(side="left", padx=(0, Spacing.SM))
        ActionButton(self.var_actions, text="Desmarcar Todos", icon="☐",
                     color=Colors.BG_CARD_HOVER, hover_color=Colors.BORDER, width=150, height=28,
                     command=self._deselect_all_vars).pack(side="left")

        self.var_checkboxes = {}
        self._var_grid = None

        # Default variables (shown when no data is loaded)
        self._default_vars = [
            ("Velocidade do Vento", True),
            ("Temperatura", True),
            ("Radiação Solar (POA)", True),
            ("Pressão Atmosférica", False),
            ("Umidade Relativa", False),
            ("Precipitação", False),
        ]
        self._build_variable_checkboxes(self._default_vars)

        # Info
        self.var_info_label = ctk.CTkLabel(
            self.var_inner,
            text="💡 Carregue os dados para que as variáveis sejam detectadas automaticamente das colunas do CSV.",
            font=Fonts.SMALL, text_color=Colors.TEXT_MUTED,
            anchor="w")
        self.var_info_label.pack(fill="x", pady=(Spacing.MD, 0))

        # ── Run Analysis ──────────────────────────────────────────────────
        run_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        run_frame.pack(fill="x", pady=(0, Spacing.MD))

        ActionButton(run_frame, text="Executar Análise", icon="▶️",
                     color=Colors.ACCENT_EMERALD,
                     hover_color="#059669",
                     command=self._run_analysis, width=220).pack(side="left")

        ActionButton(run_frame, text="Limpar Console", icon="🗑️",
                     color=Colors.BG_CARD_HOVER,
                     hover_color=Colors.DANGER,
                     command=self._clear_console, width=180).pack(
                         side="left", padx=(Spacing.SM, 0))

        self.run_status = StatusBadge(run_frame, status="idle",
                                       text="AGUARDANDO")
        self.run_status.pack(side="left", padx=(Spacing.MD, 0))

        # ── Console ───────────────────────────────────────────────────────
        SectionHeader(scroll, title="Log da Análise").pack(
            fill="x", pady=(Spacing.MD, Spacing.SM))

        self.console = ConsoleBox(scroll, height=180)
        self.console.pack(fill="x")

    def _build_variable_checkboxes(self, var_list):
        """Build or rebuild the variable checkbox grid."""
        # Destroy old grid if exists
        if self._var_grid:
            self._var_grid.destroy()
        self.var_checkboxes = {}

        self._var_grid = ctk.CTkFrame(self.var_inner, fg_color="transparent")
        pack_args = {"fill": "x"}
        if hasattr(self, 'var_info_label') and self.var_info_label.winfo_exists():
            pack_args["before"] = self.var_info_label
        self._var_grid.pack(**pack_args)

        # Use 3 columns
        cols = 3
        self._var_grid.columnconfigure(tuple(range(cols)), weight=1, uniform="var")

        for i, (name, default) in enumerate(var_list):
            cb = ctk.CTkCheckBox(
                self._var_grid, text=name, font=Fonts.BODY,
                fg_color=Colors.PRIMARY, hover_color=Colors.PRIMARY_HOVER,
                text_color=Colors.TEXT_PRIMARY,
                border_color=Colors.BORDER_LIGHT)
            cb.grid(row=i // cols, column=i % cols, sticky="w",
                    padx=Spacing.SM, pady=Spacing.XS)
            if default:
                cb.select()
            self.var_checkboxes[name] = cb

    def _select_all_vars(self):
        """Selecionar todas as variáveis."""
        for cb in self.var_checkboxes.values():
            cb.select()

    def _deselect_all_vars(self):
        """Desmarcar todas as variáveis."""
        for cb in self.var_checkboxes.values():
            cb.deselect()

    def _refresh_from_data(self):
        """Update the page based on currently loaded data."""
        if not self.app:
            return

        has_data = self.app.has_data("any")

        # Update banner
        if has_data:
            datasets = []
            if self.app.has_data("raw"):
                raw_df = self.app.app_state["raw_df"]
                datasets.append(f"Bruto ({len(raw_df):,} linhas)")
            if self.app.has_data("treated"):
                treated_df = self.app.app_state["treated_df"]
                datasets.append(f"Tratado ({len(treated_df):,} linhas)")

            self.banner_icon.configure(text="✅")
            self.banner_text.configure(
                text=f"Dados carregados: {' | '.join(datasets)}",
                text_color=Colors.ACCENT_EMERALD)
            self.banner_btn.configure(text="📂  Recarregar Dados")

            # Build variable checkboxes from actual CSV columns
            numeric_cols = self.app.get_numeric_columns()
            if numeric_cols:
                # Create checkbox list from detected columns (all selected by default)
                var_list = [(col, True) for col in numeric_cols]
                self._build_variable_checkboxes(var_list)
                self.var_info_label.configure(
                    text=f"✅ {len(numeric_cols)} variáveis numéricas detectadas automaticamente dos dados carregados.")

            # Restore analysis status if previously run
            if self.app.app_state.get("analysis_ran"):
                self.run_status.set_status("ready", "CONCLUÍDA")
        else:
            self.banner_icon.configure(text="⚠️")
            self.banner_text.configure(
                text="Nenhum dado carregado. Vá para a aba 'Dados' para importar os CSVs.",
                text_color=Colors.TEXT_MUTED)
            self.banner_btn.configure(text="📂  Ir para Dados")
            self._build_variable_checkboxes(self._default_vars)

    def _on_period_change(self, value):
        """Handle period preset changes — auto-fill date fields from data."""
        if value == "Todo o Dataset" and self.app and self.app.has_data("any"):
            # Try to detect date range from data
            for dtype in ["raw_df", "treated_df"]:
                df = self.app.app_state.get(dtype)
                if df is not None:
                    # Try to find a date column
                    date_col = self.app.app_state.get("csv_date_col", "Auto-detectar")
                    if date_col == "Auto-detectar":
                        # Heuristic: look for common date column names
                        possible = [c for c in df.columns if any(
                            x in c.lower() for x in ["date", "time", "timestamp", "data"])]
                        if possible:
                            date_col = possible[0]
                    if date_col and date_col in df.columns:
                        try:
                            dates = pd.to_datetime(df[date_col], errors="coerce")
                            self.date_start.set(str(dates.min().date()))
                            self.date_end.set(str(dates.max().date()))
                            self.console.log(
                                f"Período detectado: {dates.min().date()} a {dates.max().date()}")
                            return
                        except Exception:
                            pass
            self.date_start.set("")
            self.date_end.set("")
        elif value == "Personalizado":
            self.date_start.set("")
            self.date_end.set("")
            self.console.log("Modo personalizado: insira as datas manualmente.")

    def _run_analysis(self):
        """Execute the analysis pipeline — validates data and logs config."""
        # ── Validation ────────────────────────────────────────────────────
        if not self.app:
            return

        has_raw = self.app.has_data("raw")
        has_treated = self.app.has_data("treated")
        want_raw = self.apply_raw.get()
        want_treated = self.apply_treated.get()

        if not want_raw and not want_treated:
            self.console.log("❌ ERRO: Selecione pelo menos um dataset (Bruto ou Tratado) para analisar.")
            self.run_status.set_status("error", "SEM SELEÇÃO")
            return

        if want_raw and not has_raw:
            self.console.log("❌ ERRO: 'Dados Brutos' selecionado mas não carregado.")
            self.console.log("   → Vá para a aba 'Dados' e carregue o CSV bruto.")
            self.run_status.set_status("error", "SEM DADOS")
            return
        if want_treated and not has_treated:
            self.console.log("❌ ERRO: 'Dados Tratados' selecionado mas não carregado.")
            self.console.log("   → Vá para a aba 'Dados' e carregue o CSV tratado.")
            self.run_status.set_status("error", "SEM DADOS")
            return

        # Get selected variables
        selected_vars = [name for name, cb in self.var_checkboxes.items() if cb.get()]
        if not selected_vars:
            self.console.log("❌ ERRO: Selecione pelo menos uma variável para analisar.")
            self.run_status.set_status("error", "SEM VARIÁVEIS")
            return

        # Validate threshold
        try:
            threshold_val = float(self.threshold.get())
            if not (0 < threshold_val <= 100):
                raise ValueError
        except ValueError:
            self.console.log("❌ ERRO: Limiar deve ser um número entre 1 e 100.")
            self.run_status.set_status("error", "LIMIAR INVÁLIDO")
            return

        # ── Get config ────────────────────────────────────────────────────
        method = self.method.get()
        granularity = self.granularity.get()
        period = self.period_preset.get()

        self.run_status.set_status("running", "EXECUTANDO...")
        self.console.log("━" * 50)
        self.console.log("🔬 Iniciando análise de eventos extremos...")
        self.console.log(f"  📊 Método: {method}")
        self.console.log(f"  🎯 Limiar: {threshold_val}%")
        self.console.log(f"  ⏱️  Granularidade: {granularity}")
        self.console.log(f"  📅 Período: {period}")

        if want_raw:
            raw_rows = len(self.app.app_state["raw_df"])
            self.console.log(f"  📄 Dataset Bruto: {raw_rows:,} registros")
        if want_treated:
            treated_rows = len(self.app.app_state["treated_df"])
            self.console.log(f"  ✨ Dataset Tratado: {treated_rows:,} registros")

        self.console.log(f"  🔢 Variáveis ({len(selected_vars)}): {', '.join(selected_vars)}")

        # ── Save config to app state ──────────────────────────────────────
        config = {
            "method": method,
            "threshold": threshold_val,
            "granularity": granularity,
            "period": period,
            "variables": selected_vars,
            "apply_raw": bool(want_raw),
            "apply_treated": bool(want_treated),
            "timestamp": datetime.now().isoformat(),
        }
        self.app.app_state["analysis_config"] = config

        # ── Execute statistical engine ────────────────────────────────────
        from src.statistical.extreme_detection import detect_extremes

        results = {"raw": {}, "treated": {}}
        
        try:
            # Helper to filter DataFrame by dates if columns exist
            def filter_by_date(df_in):
                df_out = df_in.copy()
                date_col = self.app.app_state.get("csv_date_col", "Auto-detectar")
                if date_col == "Auto-detectar":
                    possible = [c for c in df_out.columns if any(
                        x in c.lower() for x in ["date", "time", "timestamp", "data"])]
                    if possible:
                        date_col = possible[0]
                
                if date_col in df_out.columns:
                    try:
                        df_out[date_col] = pd.to_datetime(df_out[date_col], errors="coerce")
                        start_str = self.date_start.get().strip()
                        end_str = self.date_end.get().strip()
                        if start_str:
                            df_out = df_out[df_out[date_col] >= pd.to_datetime(start_str)]
                        if end_str:
                            df_out = df_out[df_out[date_col] <= pd.to_datetime(end_str)]
                    except Exception as e:
                        self.console.log(f"  ⚠️ Erro ao filtrar período por data: {e}")
                return df_out

            if want_raw:
                self.console.log("\n⏳ Processando dados brutos...")
                raw_df = filter_by_date(self.app.app_state["raw_df"])
                results["raw"]["events"] = {}
                results["raw"]["summary"] = {}
                
                for var in selected_vars:
                    if var in raw_df.columns:
                        mask = detect_extremes(raw_df, var, method, threshold_pct=threshold_val)
                        results["raw"]["events"][var] = mask
                        n_events = mask.sum()
                        pct = (n_events / len(mask)) * 100 if len(mask) > 0 else 0
                        results["raw"]["summary"][var] = {
                            "count": int(n_events),
                            "pct": float(pct),
                            "mean": float(raw_df.loc[mask, var].mean()) if n_events > 0 else 0
                        }
                        self.console.log(f"  ✅ {var}: {n_events:,} eventos extremos detectados ({pct:.2f}%)")
                    else:
                        self.console.log(f"  ⚠️ Coluna '{var}' não encontrada no dataset bruto.")

            if want_treated:
                self.console.log("\n⏳ Processando dados tratados...")
                treated_df = filter_by_date(self.app.app_state["treated_df"])
                results["treated"]["events"] = {}
                results["treated"]["summary"] = {}
                
                for var in selected_vars:
                    if var in treated_df.columns:
                        mask = detect_extremes(treated_df, var, method, threshold_pct=threshold_val)
                        results["treated"]["events"][var] = mask
                        n_events = mask.sum()
                        pct = (n_events / len(mask)) * 100 if len(mask) > 0 else 0
                        results["treated"]["summary"][var] = {
                            "count": int(n_events),
                            "pct": float(pct),
                            "mean": float(treated_df.loc[mask, var].mean()) if n_events > 0 else 0
                        }
                        self.console.log(f"  ✅ {var}: {n_events:,} eventos extremos detectados ({pct:.2f}%)")
                    else:
                        self.console.log(f"  ⚠️ Coluna '{var}' não encontrada no dataset tratado.")

            self.app.app_state["analysis_results"] = results
            self.app.app_state["analysis_ran"] = True
            
            self.console.log("\n🎉 Análise concluída com sucesso! Os resultados podem ser visualizados na aba 'Comparação'.")
            self.console.log("━" * 50)
            self.run_status.set_status("ready", "CONCLUÍDA")

        except Exception as e:
            self.console.log(f"\n❌ ERRO durante a execução da análise: {e}")
            self.console.log("━" * 50)
            self.run_status.set_status("error", "FALHA")
            self.app.app_state["analysis_ran"] = False

        # Log to app
        self.app.log(f"Análise executada: {method} | {len(selected_vars)} variáveis | Limiar {threshold_val}%")

    def _clear_console(self):
        """Clear the analysis console."""
        self.console.clear()
        self.console.log("Console limpo.")
