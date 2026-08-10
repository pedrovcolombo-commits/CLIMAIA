"""
CLIMAIA – Comparison Page
Side-by-side comparison of extreme event detection between raw and treated data.
"""

import os
import customtkinter as ctk
import numpy as np
from tkinter import filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from app.theme import Colors, Fonts, Spacing
from app.components import SectionHeader, ActionButton, StatCard, ConsoleBox, StatusBadge


class ComparisonPage(ctk.CTkFrame):
    """Raw vs Treated data comparison page."""

    def __init__(self, master, app_ref=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.app = app_ref
        self._build_ui()
        self._refresh_state()

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                         scrollbar_button_color=Colors.BORDER,
                                         scrollbar_button_hover_color=Colors.BORDER_LIGHT)
        scroll.pack(fill="both", expand=True)

        # ── Header ────────────────────────────────────────────────────────
        ctk.CTkLabel(scroll, text="Comparação Bruto vs Tratado",
                     font=Fonts.HERO, text_color=Colors.TEXT_PRIMARY,
                     anchor="w").pack(fill="x")
        ctk.CTkLabel(scroll,
                     text="Análise comparativa da integridade dos dados após tratamento",
                     font=Fonts.BODY, text_color=Colors.TEXT_MUTED,
                     anchor="w").pack(fill="x", pady=(4, Spacing.XL))

        # ── Prerequisites Banner ──────────────────────────────────────────
        self.prereq_banner = ctk.CTkFrame(scroll, fg_color=Colors.BG_CARD,
                                           corner_radius=Spacing.CORNER,
                                           border_width=1,
                                           border_color=Colors.BORDER)
        self.prereq_banner.pack(fill="x", pady=(0, Spacing.XL))

        banner_inner = ctk.CTkFrame(self.prereq_banner, fg_color="transparent")
        banner_inner.pack(fill="x", padx=Spacing.CARD_PAD, pady=Spacing.MD)

        self.prereq_icon = ctk.CTkLabel(banner_inner, text="⚠️",
                                         font=(Fonts.FAMILY, 20))
        self.prereq_icon.pack(side="left")

        self.prereq_text = ctk.CTkLabel(
            banner_inner,
            text="Pré-requisitos: Carregue ambos os datasets e execute a análise primeiro.",
            font=Fonts.BODY, text_color=Colors.TEXT_MUTED, anchor="w")
        self.prereq_text.pack(side="left", padx=(Spacing.SM, 0), fill="x", expand=True)

        # Prerequisite checklist
        self.check_frame = ctk.CTkFrame(self.prereq_banner, fg_color="transparent")
        self.check_frame.pack(fill="x", padx=Spacing.CARD_PAD, pady=(0, Spacing.MD))

        self.check_labels = {}
        checks = [
            ("raw", "Dados Brutos carregados"),
            ("treated", "Dados Tratados carregados"),
            ("analysis", "Análise estatística executada"),
        ]
        for key, label in checks:
            row = ctk.CTkFrame(self.check_frame, fg_color="transparent")
            row.pack(fill="x", pady=1)
            icon_lbl = ctk.CTkLabel(row, text="❌", font=Fonts.SMALL, width=24)
            icon_lbl.pack(side="left")
            ctk.CTkLabel(row, text=label, font=Fonts.SMALL,
                         text_color=Colors.TEXT_SECONDARY).pack(side="left")
            self.check_labels[key] = icon_lbl

        # ── Comparison Stats ──────────────────────────────────────────────
        stats_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, Spacing.XL))
        stats_frame.columnconfigure((0, 1, 2, 3), weight=1, uniform="cstat")

        self.card_total_raw = StatCard(
            stats_frame, icon="📄", label="Eventos (Bruto)",
            value="—", accent=Colors.PRIMARY)
        self.card_total_raw.grid(row=0, column=0, padx=(0, Spacing.MD),
                                  sticky="nsew")

        self.card_total_treated = StatCard(
            stats_frame, icon="✨", label="Eventos (Tratado)",
            value="—", accent=Colors.SECONDARY)
        self.card_total_treated.grid(row=0, column=1, padx=(0, Spacing.MD),
                                      sticky="nsew")

        self.card_created = StatCard(
            stats_frame, icon="🆕", label="Criados pelo Tratamento",
            value="—", accent=Colors.WARNING)
        self.card_created.grid(row=0, column=2, padx=(0, Spacing.MD),
                                sticky="nsew")

        self.card_suppressed = StatCard(
            stats_frame, icon="🚫", label="Suprimidos pelo Tratamento",
            value="—", accent=Colors.DANGER)
        self.card_suppressed.grid(row=0, column=3, sticky="nsew")

        # ── Comparison Detail Table ───────────────────────────────────────
        SectionHeader(scroll, title="Diagnóstico Detalhado",
                      subtitle="Resultado da sobreposição de eventos entre os dois datasets").pack(
                          fill="x", pady=(0, Spacing.MD))

        detail_card = ctk.CTkFrame(scroll, fg_color=Colors.BG_CARD,
                                    corner_radius=Spacing.CORNER,
                                    border_width=1, border_color=Colors.BORDER)
        detail_card.pack(fill="x", pady=(0, Spacing.XL))

        # Table header
        header_row = ctk.CTkFrame(detail_card, fg_color=Colors.BG_DARKEST,
                                   corner_radius=0)
        header_row.pack(fill="x", padx=1, pady=(1, 0))

        columns = ["Variável", "Eventos Brutos", "Eventos Tratados",
                    "Coincidentes", "Criados", "Suprimidos", "Concordância"]
        for i, col in enumerate(columns):
            ctk.CTkLabel(header_row, text=col, font=Fonts.SMALL_BOLD,
                         text_color=Colors.TEXT_MUTED, anchor="center",
                         width=130).pack(side="left", padx=2, pady=Spacing.SM)

        # Table body (dynamic)
        self.table_frame = ctk.CTkFrame(detail_card, fg_color="transparent")
        self.table_frame.pack(fill="x", padx=1, pady=(0, 1))

        self._build_placeholder_rows()

        # ── Chart Placeholder ─────────────────────────────────────────────
        SectionHeader(scroll, title="Visualização Gráfica",
                      subtitle="Gráficos comparativos serão exibidos após a análise").pack(
                          fill="x", pady=(0, Spacing.MD))

        self.chart_card = ctk.CTkFrame(scroll, fg_color=Colors.BG_CARD,
                                   corner_radius=Spacing.CORNER,
                                   border_width=1, border_color=Colors.BORDER,
                                   height=300)
        self.chart_card.pack(fill="x", pady=(0, Spacing.XL))
        self.chart_card.pack_propagate(False)

        # Placeholder content
        placeholder = ctk.CTkFrame(self.chart_card, fg_color="transparent")
        placeholder.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(placeholder, text="📊", font=(Fonts.FAMILY, 48),
                     text_color=Colors.TEXT_DISABLED).pack()
        ctk.CTkLabel(placeholder,
                     text="Execute a comparação para gerar os gráficos",
                     font=Fonts.BODY, text_color=Colors.TEXT_DISABLED).pack(
                         pady=(Spacing.SM, 0))

        # ── Actions ───────────────────────────────────────────────────────
        actions = ctk.CTkFrame(scroll, fg_color="transparent")
        actions.pack(fill="x", pady=(0, Spacing.MD))

        ActionButton(actions, text="Executar Comparação", icon="🔄",
                     color=Colors.ACCENT_EMERALD,
                     command=self._run_comparison, width=220).pack(side="left")

        ActionButton(actions, text="Exportar Relatório", icon="📋",
                     color=Colors.PRIMARY,
                     command=self._export_report, width=200).pack(
                         side="left", padx=(Spacing.MD, 0))

        self.comparison_status = StatusBadge(actions, status="idle",
                                              text="AGUARDANDO")
        self.comparison_status.pack(side="left", padx=(Spacing.MD, 0))

        # ── Console ───────────────────────────────────────────────────────
        SectionHeader(scroll, title="Log de Comparação").pack(
            fill="x", pady=(Spacing.MD, Spacing.SM))

        self.console = ConsoleBox(scroll, height=150)
        self.console.pack(fill="x")

    def _build_placeholder_rows(self):
        """Build rows in the comparison table based on current state or results."""
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        state = self.app.app_state if self.app else {}
        comp_results = state.get("comparison_results")
        config = state.get("analysis_config") or {}
        vars_to_show = config.get("variables") or []

        if not vars_to_show:
            vars_to_show = ["Velocidade do Vento", "Temperatura", "Radiação Solar"]

        for var in vars_to_show:
            row = ctk.CTkFrame(self.table_frame, fg_color="transparent", height=36)
            row.pack(fill="x")

            if comp_results and var in comp_results:
                r = comp_results[var]
                vals = [
                    var,
                    f"{r['total_raw_episodes']:,}",
                    f"{r['total_treated_episodes']:,}",
                    f"{r['coincident']:,}",
                    f"{r['created']:,}",
                    f"{r['suppressed']:,}",
                    f"{r['agreement_pct']:.1f}%"
                ]
            else:
                vals = [var, "—", "—", "—", "—", "—", "—"]

            for val in vals:
                ctk.CTkLabel(row, text=val, font=Fonts.SMALL,
                             text_color=Colors.TEXT_SECONDARY,
                             anchor="center", width=130).pack(
                                 side="left", padx=2, pady=4)

    def _refresh_state(self):
        """Update prerequisite checks from app state."""
        if not self.app:
            return

        state = self.app.app_state
        all_ok = True

        # Check raw data
        if state.get("raw_df") is not None:
            self.check_labels["raw"].configure(text="✅")
        else:
            self.check_labels["raw"].configure(text="❌")
            all_ok = False

        # Check treated data
        if state.get("treated_df") is not None:
            self.check_labels["treated"].configure(text="✅")
        else:
            self.check_labels["treated"].configure(text="❌")
            all_ok = False

        # Check analysis ran
        if state.get("analysis_ran"):
            self.check_labels["analysis"].configure(text="✅")
        else:
            self.check_labels["analysis"].configure(text="❌")
            all_ok = False

        # Update banner style
        if all_ok:
            self.prereq_icon.configure(text="✅")
            self.prereq_text.configure(
                text="Todos os pré-requisitos atendidos. Pronto para executar a comparação.",
                text_color=Colors.ACCENT_EMERALD)
        else:
            self.prereq_icon.configure(text="⚠️")
            self.prereq_text.configure(
                text="Pré-requisitos pendentes:",
                text_color=Colors.ACCENT_WARM)

        # Update table with analysis variables or comparison results
        self._build_placeholder_rows()

        # If comparison was already run, show stats and chart
        if state.get("comparison_ran") and state.get("comparison_results"):
            self.comparison_status.set_status("ready", "CONCLUÍDA")
            self._update_stats_cards(state["comparison_results"])
            self._update_chart(state["comparison_results"])
        else:
            self._reset_stats_cards()

    def _reset_stats_cards(self):
        self.card_total_raw.set_value("—")
        self.card_total_treated.set_value("—")
        self.card_created.set_value("—")
        self.card_suppressed.set_value("—")

    def _update_stats_cards(self, results):
        """Update stat cards with aggregated metrics from results."""
        if not results:
            self._reset_stats_cards()
            return
        
        tot_raw = sum(r["total_raw_episodes"] for r in results.values())
        tot_treated = sum(r["total_treated_episodes"] for r in results.values())
        tot_created = sum(r["created"] for r in results.values())
        tot_suppressed = sum(r["suppressed"] for r in results.values())
        
        self.card_total_raw.set_value(f"{tot_raw:,}")
        self.card_total_treated.set_value(f"{tot_treated:,}")
        self.card_created.set_value(f"{tot_created:,}")
        self.card_suppressed.set_value(f"{tot_suppressed:,}")

    def _update_chart(self, results):
        """Embed a beautiful Matplotlib comparison chart."""
        # Clear existing widgets in the chart card
        for widget in self.chart_card.winfo_children():
            widget.destroy()

        if not results:
            # Fallback placeholder
            placeholder = ctk.CTkFrame(self.chart_card, fg_color="transparent")
            placeholder.place(relx=0.5, rely=0.5, anchor="center")
            ctk.CTkLabel(placeholder, text="📊", font=(Fonts.FAMILY, 48),
                         text_color=Colors.TEXT_DISABLED).pack()
            ctk.CTkLabel(placeholder, text="Sem dados de comparação para exibir",
                         font=Fonts.BODY, text_color=Colors.TEXT_DISABLED).pack(pady=(Spacing.SM, 0))
            return

        # Prepare data for matplotlib
        vars_list = list(results.keys())
        raw_events = [results[v]["total_raw_episodes"] for v in vars_list]
        treated_events = [results[v]["total_treated_episodes"] for v in vars_list]
        coincident = [results[v]["coincident"] for v in vars_list]

        fig = Figure(figsize=(7, 2.8), facecolor=Colors.BG_CARD)
        ax = fig.add_subplot(111)
        ax.set_facecolor(Colors.BG_CARD)

        x = np.arange(len(vars_list))
        width = 0.25

        # Hex to RGB normalizado para matplotlib
        def hex_to_rgb(hex_str):
            h = hex_str.lstrip('#')
            return tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))

        color_raw = hex_to_rgb(Colors.PRIMARY)
        color_treated = hex_to_rgb(Colors.SECONDARY)
        color_coin = hex_to_rgb(Colors.ACCENT_EMERALD)

        ax.bar(x - width, raw_events, width, label='Eventos Brutos', color=color_raw, edgecolor='none')
        ax.bar(x, treated_events, width, label='Eventos Tratados', color=color_treated, edgecolor='none')
        ax.bar(x + width, coincident, width, label='Coincidentes', color=color_coin, edgecolor='none')

        ax.set_title("Comparação de Eventos Extremos Detectados", color=Colors.TEXT_PRIMARY, fontsize=10, pad=8)
        ax.set_xticks(x)
        # Truncate long variable names for x-axis readability
        ax.set_xticklabels([v[:15] + "..." if len(v) > 15 else v for v in vars_list], color=Colors.TEXT_SECONDARY, fontsize=8)
        ax.tick_params(colors=Colors.TEXT_MUTED, labelsize=8)
        ax.grid(True, color=Colors.BORDER, linestyle='--', alpha=0.3, axis='y')
        
        # Style spines
        for spine in ax.spines.values():
            spine.set_color(Colors.BORDER)
            spine.set_alpha(0.5)

        # Legend with matching colors
        leg = ax.legend(facecolor=Colors.BG_DARKEST, edgecolor=Colors.BORDER, labelcolor=Colors.TEXT_SECONDARY, fontsize=8)
        leg.get_frame().set_alpha(0.8)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_card)
        canvas.draw()
        canvas.get_tkwidget().pack(fill="both", expand=True, padx=Spacing.MD, pady=Spacing.MD)

    def _run_comparison(self):
        """Execute comparison — validates all prerequisites first."""
        if not self.app:
            return

        state = self.app.app_state

        # ── Validation ────────────────────────────────────────────────────
        errors = []
        if state.get("raw_df") is None:
            errors.append("Dados Brutos não carregados")
        if state.get("treated_df") is None:
            errors.append("Dados Tratados não carregados")
        if not state.get("analysis_ran") or "analysis_results" not in state:
            errors.append("Análise estatística não executada")

        if errors:
            self.console.log("━" * 50)
            self.console.log("❌ Não é possível executar a comparação:")
            for err in errors:
                self.console.log(f"   → {err}")
            self.console.log("")
            self.console.log("💡 Resolva os pré-requisitos e tente novamente:")
            if state.get("raw_df") is None or state.get("treated_df") is None:
                self.console.log("   1. Vá para a aba 'Dados' e carregue ambos os CSVs")
            if not state.get("analysis_ran"):
                self.console.log("   2. Vá para a aba 'Análise' e execute a detecção de eventos")
            self.console.log("━" * 50)
            self.comparison_status.set_status("error", "PRÉ-REQUISITOS")
            return

        # ── Execute comparison ────────────────────────────────────────────
        config = state.get("analysis_config") or {}
        variables = config.get("variables", [])
        method = config.get("method", "N/A")
        min_gap = config.get("min_gap", 12)
        min_duration = config.get("min_duration", 6)

        self.comparison_status.set_status("running", "EXECUTANDO...")
        self.console.log("━" * 50)
        self.console.log("🔄 Iniciando comparação Bruto vs Tratado...")
        self.console.log(f"  Método de análise: {method}")
        self.console.log(f"  Variáveis avaliadas: {', '.join(variables)}")

        from src.statistical.comparison import compare_event_masks

        comp_results = {}
        analysis_res = state["analysis_results"]

        try:
            for var in variables:
                raw_exists = "raw" in analysis_res and "events" in analysis_res["raw"] and var in analysis_res["raw"]["events"]
                treated_exists = "treated" in analysis_res and "events" in analysis_res["treated"] and var in analysis_res["treated"]["events"]
                
                if raw_exists and treated_exists:
                    raw_mask = analysis_res["raw"]["events"][var]
                    treated_mask = analysis_res["treated"]["events"][var]
                    
                    metrics = compare_event_masks(
                        raw_mask, treated_mask, min_gap=min_gap, min_duration=min_duration
                    )
                    comp_results[var] = metrics
                    
                    self.console.log(f"\n📈 Resultados para: {var}")
                    self.console.log(f"  - Eventos Brutos (episódios): {metrics['total_raw_episodes']:,}")
                    self.console.log(f"  - Eventos Tratados (episódios): {metrics['total_treated_episodes']:,}")
                    self.console.log(f"  - Coincidentes: {metrics['coincident']:,}")
                    self.console.log(f"  - Criados pelo Tratamento: {metrics['created']:,}")
                    self.console.log(f"  - Suprimidos pelo Tratamento: {metrics['suppressed']:,}")
                    self.console.log(f"  - Pontos extremos (bruto/tratado): {metrics['total_raw']:,} / {metrics['total_treated']:,}")
                    self.console.log(f"  - Taxa de Concordância: {metrics['agreement_pct']:.2f}%")
                else:
                    self.console.log(f"\n⚠️ Não foi possível comparar '{var}': dados ausentes em um dos datasets.")

            state["comparison_results"] = comp_results
            state["comparison_ran"] = True
            
            # Update UI views
            self._update_stats_cards(comp_results)
            self._build_placeholder_rows()
            self._update_chart(comp_results)
            
            self.console.log("\n🎉 Comparação finalizada com sucesso!")
            self.console.log("━" * 50)
            self.comparison_status.set_status("ready", "CONCLUÍDA")

        except Exception as e:
            self.console.log(f"\n❌ ERRO durante a comparação: {e}")
            self.console.log("━" * 50)
            self.comparison_status.set_status("error", "FALHA")
            state["comparison_ran"] = False

        self.app.log(f"Comparação executada para {len(variables)} variáveis.")

    def _export_report(self):
        """Export comparison report as a text file."""
        if not self.app:
            return

        state = self.app.app_state
        comp_results = state.get("comparison_results")

        if not state.get("comparison_ran") or not comp_results:
            self.console.log("❌ Execute a comparação antes de exportar o relatório.")
            return

        # Open save dialog
        filepath = filedialog.asksaveasfilename(
            title="Exportar Relatório de Comparação",
            defaultextension=".txt",
            filetypes=[
                ("Texto", "*.txt"),
                ("CSV", "*.csv"),
                ("Todos os arquivos", "*.*"),
            ],
            initialfile="CLIMAIA_Relatorio_Comparacao.txt")

        if not filepath:
            return

        try:
            config = state.get("analysis_config") or {}
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("CLIMAIA - Relatório de Comparação Bruto vs Tratado\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Data de Geração: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write(f"Método Analítico: {config.get('method', 'N/A')}\n")
                f.write(f"Limiar de Sensibilidade: {config.get('threshold', 'N/A')}%\n")
                f.write(f"Granularidade: {config.get('granularity', 'N/A')}\n")
                f.write(f"Período Selecionado: {config.get('period', 'N/A')}\n\n")

                # General counts
                f.write("-" * 40 + "\n")
                f.write("Resumo Geral da Análise\n")
                f.write("-" * 40 + "\n")
                tot_raw = sum(r["total_raw_episodes"] for r in comp_results.values())
                tot_treated = sum(r["total_treated_episodes"] for r in comp_results.values())
                tot_created = sum(r["created"] for r in comp_results.values())
                tot_suppressed = sum(r["suppressed"] for r in comp_results.values())
                
                f.write(f"Total de Eventos Brutos (episódios): {tot_raw:,}\n")
                f.write(f"Total de Eventos Tratados (episódios): {tot_treated:,}\n")
                f.write(f"Total de Eventos Criados: {tot_created:,}\n")
                f.write(f"Total de Eventos Suprimidos: {tot_suppressed:,}\n\n")

                # Variable detail
                f.write("-" * 40 + "\n")
                f.write("Detalhes por Variável\n")
                f.write("-" * 40 + "\n")
                for var, r in comp_results.items():
                    f.write(f"\nVariável: {var}\n")
                    f.write(f"  - Eventos Brutos (episódios): {r['total_raw_episodes']:,}\n")
                    f.write(f"  - Eventos Tratados (episódios): {r['total_treated_episodes']:,}\n")
                    f.write(f"  - Pontos extremos (bruto/tratado): {r['total_raw']:,} / {r['total_treated']:,}\n")
                    f.write(f"  - Coincidentes: {r['coincident']:,}\n")
                    f.write(f"  - Criados (só no Tratado): {r['created']:,}\n")
                    f.write(f"  - Suprimidos (só no Bruto): {r['suppressed']:,}\n")
                    f.write(f"  - Índice de Concordância: {r['agreement_pct']:.2f}%\n")
                
                f.write("\n" + "=" * 60 + "\n")
                f.write("Relatório gerado automaticamente pelo CLIMAIA.\n")
                f.write("=" * 60 + "\n")

            self.console.log(f"✅ Relatório exportado: {os.path.basename(filepath)}")
            self.app.log(f"Relatório de comparação exportado para: {filepath}")

        except Exception as e:
            self.console.log(f"❌ Erro ao exportar: {e}")
            messagebox.showerror("Erro ao Exportar", f"Não foi possível salvar o relatório:\n{e}")

