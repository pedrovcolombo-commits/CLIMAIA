"""
CLIMAIA – Data Management Page
Load, preview, and manage raw & treated climate datasets.
"""

import os
import zipfile
import tempfile
import customtkinter as ctk
import pandas as pd
from tkinter import filedialog, messagebox
from app.theme import Colors, Fonts, Spacing
from app.components import SectionHeader, ActionButton, StatusBadge


class DataPage(ctk.CTkFrame):
    """Data loading, preview and management page."""

    def __init__(self, master, app_ref=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.app = app_ref
        self._build_ui()
        self._restore_state()

    def _build_ui(self):
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                         scrollbar_button_color=Colors.BORDER,
                                         scrollbar_button_hover_color=Colors.BORDER_LIGHT)
        scroll.pack(fill="both", expand=True)

        # ── Header ────────────────────────────────────────────────────────
        ctk.CTkLabel(scroll, text="Gestão de Dados", font=Fonts.HERO,
                     text_color=Colors.TEXT_PRIMARY, anchor="w").pack(
                         fill="x")
        ctk.CTkLabel(scroll, text="Carregue e visualize os datasets brutos e tratados",
                     font=Fonts.BODY, text_color=Colors.TEXT_MUTED,
                     anchor="w").pack(fill="x", pady=(4, Spacing.XL))

        # ── Upload Cards ──────────────────────────────────────────────────
        upload_row = ctk.CTkFrame(scroll, fg_color="transparent")
        upload_row.pack(fill="x", pady=(0, Spacing.XL))
        upload_row.columnconfigure((0, 1), weight=1, uniform="upload")

        # Raw Data Card
        self.raw_card = self._build_upload_card(
            upload_row, "📄  Dados Brutos",
            "Carregue CSVs, Excel ou um ZIP com todos os dados do período.",
            "raw")
        self.raw_card.grid(row=0, column=0, padx=(0, Spacing.MD), sticky="nsew")

        # Treated Data Card
        self.treated_card = self._build_upload_card(
            upload_row, "✨  Dados Tratados",
            "Carregue CSVs, Excel ou um ZIP com todos os dados tratados.",
            "treated")
        self.treated_card.grid(row=0, column=1, sticky="nsew")

        # ── Data Preview Section ──────────────────────────────────────────
        SectionHeader(scroll, title="Pré-visualização dos Dados",
                      subtitle="Primeiras linhas de cada dataset carregado").pack(
                          fill="x", pady=(0, Spacing.MD))

        preview_row = ctk.CTkFrame(scroll, fg_color="transparent")
        preview_row.pack(fill="x", pady=(0, Spacing.XL))
        preview_row.columnconfigure((0, 1), weight=1, uniform="preview")

        # Raw preview
        raw_preview = ctk.CTkFrame(preview_row, fg_color=Colors.BG_CARD,
                                    corner_radius=Spacing.CORNER,
                                    border_width=1, border_color=Colors.BORDER)
        raw_preview.grid(row=0, column=0, padx=(0, Spacing.MD), sticky="nsew")

        ctk.CTkLabel(raw_preview, text="Dados Brutos", font=Fonts.H3,
                     text_color=Colors.TEXT_PRIMARY).pack(
                         padx=Spacing.CARD_PAD, pady=(Spacing.CARD_PAD, Spacing.SM),
                         anchor="w")

        self.raw_preview_text = ctk.CTkTextbox(
            raw_preview, font=Fonts.MONO_SMALL, fg_color=Colors.BG_DARKEST,
            text_color=Colors.TEXT_SECONDARY, height=250, wrap="none",
            activate_scrollbars=True)
        self.raw_preview_text.pack(fill="both", expand=True,
                                    padx=Spacing.CARD_PAD,
                                    pady=(0, Spacing.CARD_PAD))
        self.raw_preview_text.insert("1.0", "Nenhum dado carregado.")
        self.raw_preview_text.configure(state="disabled")

        # Treated preview
        treated_preview = ctk.CTkFrame(preview_row, fg_color=Colors.BG_CARD,
                                        corner_radius=Spacing.CORNER,
                                        border_width=1, border_color=Colors.BORDER)
        treated_preview.grid(row=0, column=1, sticky="nsew")

        ctk.CTkLabel(treated_preview, text="Dados Tratados", font=Fonts.H3,
                     text_color=Colors.TEXT_PRIMARY).pack(
                         padx=Spacing.CARD_PAD, pady=(Spacing.CARD_PAD, Spacing.SM),
                         anchor="w")

        self.treated_preview_text = ctk.CTkTextbox(
            treated_preview, font=Fonts.MONO_SMALL, fg_color=Colors.BG_DARKEST,
            text_color=Colors.TEXT_SECONDARY, height=250, wrap="none",
            activate_scrollbars=True)
        self.treated_preview_text.pack(fill="both", expand=True,
                                        padx=Spacing.CARD_PAD,
                                        pady=(0, Spacing.CARD_PAD))
        self.treated_preview_text.insert("1.0", "Nenhum dado carregado.")
        self.treated_preview_text.configure(state="disabled")

        # ── Data Summary ──────────────────────────────────────────────────
        SectionHeader(scroll, title="Resumo Estatístico",
                      subtitle="Estatísticas descritivas rápidas dos datasets").pack(
                          fill="x", pady=(0, Spacing.MD))

        self.summary_frame = ctk.CTkFrame(scroll, fg_color=Colors.BG_CARD,
                                            corner_radius=Spacing.CORNER,
                                            border_width=1,
                                            border_color=Colors.BORDER)
        self.summary_frame.pack(fill="x")

        self.summary_text = ctk.CTkTextbox(
            self.summary_frame, font=Fonts.MONO_SMALL,
            fg_color="transparent", text_color=Colors.TEXT_SECONDARY,
            height=200, wrap="none", activate_scrollbars=True)
        self.summary_text.pack(fill="both", expand=True,
                                padx=Spacing.CARD_PAD, pady=Spacing.CARD_PAD)
        self.summary_text.insert("1.0", "Carregue os dados para ver o resumo estatístico.")
        self.summary_text.configure(state="disabled")

    def _build_upload_card(self, parent, title, desc, dtype):
        card = ctk.CTkFrame(parent, fg_color=Colors.BG_CARD,
                            corner_radius=Spacing.CORNER,
                            border_width=1, border_color=Colors.BORDER)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=Spacing.CARD_PAD,
                   pady=Spacing.CARD_PAD)

        # Title row
        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")

        ctk.CTkLabel(top, text=title, font=Fonts.H3,
                     text_color=Colors.TEXT_PRIMARY).pack(side="left")

        badge = StatusBadge(top, status="idle", text="NÃO CARREGADO")
        badge.pack(side="right")

        if dtype == "raw":
            self.raw_badge = badge
        else:
            self.treated_badge = badge

        # Description
        ctk.CTkLabel(inner, text=desc, font=Fonts.SMALL,
                     text_color=Colors.TEXT_MUTED, anchor="w",
                     wraplength=350).pack(fill="x", pady=(Spacing.SM, Spacing.MD))

        # File info
        info_lbl = ctk.CTkLabel(inner, text="Nenhum arquivo selecionado",
                                font=Fonts.SMALL,
                                text_color=Colors.TEXT_DISABLED, anchor="w")
        info_lbl.pack(fill="x", pady=(0, Spacing.MD))

        if dtype == "raw":
            self.raw_info = info_lbl
        else:
            self.treated_info = info_lbl

        # Buttons
        btn_row = ctk.CTkFrame(inner, fg_color="transparent")
        btn_row.pack(fill="x")

        color = Colors.PRIMARY if dtype == "raw" else Colors.SECONDARY
        ActionButton(btn_row, text="Selecionar Arquivo", icon="📂",
                     color=color,
                     command=lambda: self._load_file(dtype)).pack(
                         side="left", padx=(0, Spacing.SM))

        ActionButton(btn_row, text="Limpar", icon="🗑️",
                     color=Colors.BG_CARD_HOVER,
                     hover_color=Colors.DANGER,
                     command=lambda: self._clear_data(dtype)).pack(side="left")

        return card

    def _restore_state(self):
        """Restore previews if data was previously loaded in app_state."""
        if not self.app:
            return

        state = self.app.app_state

        # Restore raw data display
        raw_df = state.get("raw_df")
        if raw_df is not None:
            raw_path = state.get("raw_path", "")
            if raw_path and ", " in raw_path:
                filename = f"{len(raw_path.split(', '))} arquivos carregados"
            else:
                filename = os.path.basename(raw_path) if raw_path else "arquivo.csv"
            rows, cols = raw_df.shape
            self.raw_badge.set_status("ready", "CARREGADO")
            self.raw_info.configure(
                text=f"📄 {filename}  •  {rows:,} linhas  •  {cols} colunas",
                text_color=Colors.TEXT_SECONDARY)
            self._update_preview(self.raw_preview_text, raw_df)

        # Restore treated data display
        treated_df = state.get("treated_df")
        if treated_df is not None:
            treated_path = state.get("treated_path", "")
            if treated_path and ", " in treated_path:
                filename = f"{len(treated_path.split(', '))} arquivos carregados"
            else:
                filename = os.path.basename(treated_path) if treated_path else "arquivo.csv"
            rows, cols = treated_df.shape
            self.treated_badge.set_status("ready", "CARREGADO")
            self.treated_info.configure(
                text=f"📄 {filename}  •  {rows:,} linhas  •  {cols} colunas",
                text_color=Colors.TEXT_SECONDARY)
            self._update_preview(self.treated_preview_text, treated_df)

        # Restore summary
        if raw_df is not None or treated_df is not None:
            self._update_summary()

    def _extract_files_from_zip(self, zip_path: str) -> list:
        """Extract CSV/Excel files from a ZIP archive to a temp directory.
        Returns a list of extracted file paths."""
        extracted = []
        try:
            temp_dir = tempfile.mkdtemp(prefix="climaia_")
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for member in zf.namelist():
                    # Skip directories and hidden/system files
                    if member.endswith('/') or member.startswith('__MACOSX'):
                        continue
                    ext = os.path.splitext(member)[1].lower()
                    if ext in ('.csv', '.xlsx', '.xls'):
                        # Extract preserving just the filename (flatten)
                        filename = os.path.basename(member)
                        if not filename:
                            continue
                        target_path = os.path.join(temp_dir, filename)
                        # Handle duplicate filenames
                        counter = 1
                        base, fext = os.path.splitext(filename)
                        while os.path.exists(target_path):
                            target_path = os.path.join(temp_dir, f"{base}_{counter}{fext}")
                            counter += 1
                        with zf.open(member) as source, open(target_path, 'wb') as target:
                            target.write(source.read())
                        extracted.append(target_path)
            
            if self.app:
                self.app.log(f"ZIP extraído: {len(extracted)} arquivo(s) de dados encontrado(s) em {os.path.basename(zip_path)}")
        except zipfile.BadZipFile:
            messagebox.showerror("Erro no ZIP",
                                  f"O arquivo '{os.path.basename(zip_path)}' não é um ZIP válido.")
        except Exception as e:
            messagebox.showerror("Erro ao Extrair ZIP",
                                  f"Erro ao processar o ZIP:\n{e}")
        return extracted

    def _load_file(self, dtype: str):
        filepaths = filedialog.askopenfilenames(
            title=f"Selecionar {'Dados Brutos' if dtype == 'raw' else 'Dados Tratados'}",
            filetypes=[
                ("Dados Climáticos", "*.csv *.xlsx *.xls *.zip"),
                ("Arquivo ZIP", "*.zip"),
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx *.xls"),
                ("All files", "*.*"),
            ])

        if not filepaths:
            return

        dfs = []
        filenames = []

        # Expand ZIP files into individual data files
        expanded_paths = []
        for filepath in filepaths:
            ext = os.path.splitext(filepath)[1].lower()
            if ext == '.zip':
                zip_files = self._extract_files_from_zip(filepath)
                if zip_files:
                    expanded_paths.extend(zip_files)
                    filenames.append(f"{os.path.basename(filepath)} ({len(zip_files)} arquivos)")
                else:
                    messagebox.showwarning("ZIP Vazio",
                                            f"Nenhum arquivo CSV/Excel encontrado em '{os.path.basename(filepath)}'.")
            else:
                expanded_paths.append(filepath)

        if not expanded_paths:
            return

        for filepath in expanded_paths:
            try:
                ext = os.path.splitext(filepath)[1].lower()

                if ext in ('.xlsx', '.xls'):
                    # Excel file
                    df = pd.read_excel(filepath, engine='openpyxl')
                else:
                    # CSV file — get settings from app state
                    read_kwargs = {}
                    if self.app:
                        read_kwargs = self.app.get_csv_read_kwargs()

                    # Try with settings first, fallback to auto-detect separator
                    try:
                        df = pd.read_csv(filepath, **read_kwargs)
                        # If auto-detect parsed only 1 column, it likely failed. Try semicolon.
                        if len(df.columns) == 1 and read_kwargs.get('sep') is None:
                            df_alt = pd.read_csv(filepath, sep=';')
                            if len(df_alt.columns) > 1:
                                df = df_alt
                    except Exception:
                        # Fallback: try semicolon separator (common in BR data)
                        try:
                            df = pd.read_csv(filepath, sep=';')
                        except Exception:
                            df = pd.read_csv(filepath)

                dfs.append(df)
                # Only add filename if not already added (zip case)
                basename = os.path.basename(filepath)
                if basename not in filenames and not any(basename in f for f in filenames):
                    filenames.append(basename)
            except Exception as e:
                messagebox.showerror("Erro ao Carregar",
                                      f"Não foi possível ler o arquivo {os.path.basename(filepath)}:\n{e}")
                if self.app:
                    self.app.log(f"ERRO ao carregar arquivo {filepath}: {e}")

        if not dfs:
            return
            
        try:
            final_df = pd.concat(dfs, ignore_index=True)
            
            if len(filenames) == 1:
                display_filename = filenames[0]
                stored_path = filepaths[0]
            else:
                display_filename = f"{len(filenames)} arquivos carregados"
                stored_path = ", ".join(filepaths)
                
            rows, cols = final_df.shape

            if dtype == "raw":
                self.raw_badge.set_status("ready", "CARREGADO")
                self.raw_info.configure(
                    text=f"📄 {display_filename}  •  {rows:,} linhas  •  {cols} colunas",
                    text_color=Colors.TEXT_SECONDARY)
                self._update_preview(self.raw_preview_text, final_df)
            else:
                self.treated_badge.set_status("ready", "CARREGADO")
                self.treated_info.configure(
                    text=f"📄 {display_filename}  •  {rows:,} linhas  •  {cols} colunas",
                    text_color=Colors.TEXT_SECONDARY)
                self._update_preview(self.treated_preview_text, final_df)

            # Store in app state
            if self.app:
                if dtype == "raw":
                    self.app.app_state["raw_df"] = final_df
                    self.app.app_state["raw_path"] = stored_path
                    self.app.app_state["raw_columns"] = final_df.columns.tolist()
                else:
                    self.app.app_state["treated_df"] = final_df
                    self.app.app_state["treated_path"] = stored_path
                    self.app.app_state["treated_columns"] = final_df.columns.tolist()

                # Reset downstream results (analysis/comparison invalidated)
                self.app.app_state["analysis_ran"] = False
                self.app.app_state["analysis_results"] = None
                self.app.app_state["comparison_ran"] = False
                self.app.app_state["comparison_results"] = None

                self.app.log(
                    f"Dataset(s) {'bruto(s)' if dtype == 'raw' else 'tratado(s)'} carregado(s): "
                    f"{display_filename} ({rows:,} linhas, {cols} colunas)")

            self._update_summary()

        except Exception as e:
            messagebox.showerror("Erro ao Concatenar/Atualizar",
                                  f"Ocorreu um erro ao processar os arquivos carregados:\n{e}")
            if self.app:
                self.app.log(f"ERRO ao processar arquivos múltiplos: {e}")

    def _clear_data(self, dtype: str):
        """Clear loaded data and reset downstream analysis state."""
        if dtype == "raw":
            self.raw_badge.set_status("idle", "NÃO CARREGADO")
            self.raw_info.configure(text="Nenhum arquivo selecionado",
                                     text_color=Colors.TEXT_DISABLED)
            self._update_preview(self.raw_preview_text, None)
            if self.app:
                old_path = self.app.app_state.get("raw_path")
                self.app.app_state["raw_df"] = None
                self.app.app_state["raw_path"] = None
                self.app.app_state["raw_columns"] = []
                if old_path:
                    self.app.log(f"Dados brutos removidos ({os.path.basename(old_path)})")
        else:
            self.treated_badge.set_status("idle", "NÃO CARREGADO")
            self.treated_info.configure(text="Nenhum arquivo selecionado",
                                         text_color=Colors.TEXT_DISABLED)
            self._update_preview(self.treated_preview_text, None)
            if self.app:
                old_path = self.app.app_state.get("treated_path")
                self.app.app_state["treated_df"] = None
                self.app.app_state["treated_path"] = None
                self.app.app_state["treated_columns"] = []
                if old_path:
                    self.app.log(f"Dados tratados removidos ({os.path.basename(old_path)})")

        # Invalidate downstream results
        if self.app:
            self.app.app_state["analysis_ran"] = False
            self.app.app_state["analysis_results"] = None
            self.app.app_state["comparison_ran"] = False
            self.app.app_state["comparison_results"] = None

        self._update_summary()

    def _update_preview(self, textbox, df):
        textbox.configure(state="normal")
        textbox.delete("1.0", "end")
        if df is not None:
            textbox.insert("1.0", df.head(20).to_string())
        else:
            textbox.insert("1.0", "Nenhum dado carregado.")
        textbox.configure(state="disabled")

    def _update_summary(self):
        self.summary_text.configure(state="normal")
        self.summary_text.delete("1.0", "end")

        parts = []
        raw_df = self.app.app_state.get("raw_df") if self.app else None
        treated_df = self.app.app_state.get("treated_df") if self.app else None

        if raw_df is not None:
            parts.append("═══ DADOS BRUTOS ═══\n")
            parts.append(f"Colunas: {', '.join(raw_df.columns.tolist())}\n")
            parts.append(f"Tipos: {dict(raw_df.dtypes)}\n\n")
            parts.append(raw_df.describe().to_string())
            parts.append("\n\n")

        if treated_df is not None:
            parts.append("═══ DADOS TRATADOS ═══\n")
            parts.append(f"Colunas: {', '.join(treated_df.columns.tolist())}\n")
            parts.append(f"Tipos: {dict(treated_df.dtypes)}\n\n")
            parts.append(treated_df.describe().to_string())

        if not parts:
            parts.append("Carregue os dados para ver o resumo estatístico.")

        self.summary_text.insert("1.0", "".join(parts))
        self.summary_text.configure(state="disabled")
