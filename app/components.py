"""
CLIMAIA – Reusable UI Components
Custom widgets built on top of CustomTkinter for a consistent, premium look.
"""

import customtkinter as ctk
from app.theme import Colors, Fonts, Spacing


# ─── Stat Card ────────────────────────────────────────────────────────────────
class StatCard(ctk.CTkFrame):
    """A compact card showing a single metric with icon, value & label."""

    def __init__(self, master, icon: str, label: str, value: str = "—",
                 accent: str = Colors.PRIMARY, **kwargs):
        super().__init__(master, fg_color=Colors.BG_CARD,
                         corner_radius=Spacing.CORNER, **kwargs)

        self._accent = accent
        self.configure(border_width=1, border_color=Colors.BORDER)

        # Inner padding frame
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=Spacing.CARD_PAD,
                   pady=Spacing.CARD_PAD)

        # Top row: icon + label
        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")

        icon_lbl = ctk.CTkLabel(top, text=icon, font=(Fonts.FAMILY, 20),
                                text_color=accent)
        icon_lbl.pack(side="left")

        label_lbl = ctk.CTkLabel(top, text=label, font=Fonts.SMALL,
                                 text_color=Colors.TEXT_SECONDARY)
        label_lbl.pack(side="left", padx=(Spacing.SM, 0))

        # Value
        self._value_lbl = ctk.CTkLabel(inner, text=value, font=Fonts.HERO,
                                       text_color=Colors.TEXT_PRIMARY,
                                       anchor="w")
        self._value_lbl.pack(fill="x", pady=(Spacing.SM, 0))

    def set_value(self, value: str):
        self._value_lbl.configure(text=value)


# ─── Section Header ──────────────────────────────────────────────────────────
class SectionHeader(ctk.CTkFrame):
    """A styled section header with title and optional subtitle."""

    def __init__(self, master, title: str, subtitle: str = "", **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        ctk.CTkLabel(self, text=title, font=Fonts.H2,
                     text_color=Colors.TEXT_PRIMARY, anchor="w").pack(
                         fill="x")

        if subtitle:
            ctk.CTkLabel(self, text=subtitle, font=Fonts.SMALL,
                         text_color=Colors.TEXT_MUTED, anchor="w").pack(
                             fill="x", pady=(2, 0))


# ─── Action Button (Gradient-like) ───────────────────────────────────────────
class ActionButton(ctk.CTkButton):
    """A primary action button with glow styling."""

    def __init__(self, master, text: str, icon: str = "",
                 color: str = Colors.PRIMARY,
                 hover_color: str = Colors.PRIMARY_HOVER,
                 **kwargs):
        display = f"{icon}  {text}" if icon else text
        height = kwargs.pop('height', 40)
        super().__init__(
            master,
            text=display,
            font=Fonts.BODY_BOLD,
            fg_color=color,
            hover_color=hover_color,
            text_color="#ffffff",
            corner_radius=Spacing.CORNER_SM,
            height=height,
            **kwargs,
        )


# ─── Icon Button (ghost style) ───────────────────────────────────────────────
class IconButton(ctk.CTkButton):
    """Small icon-only button with transparent background."""

    def __init__(self, master, icon: str, tooltip: str = "", **kwargs):
        super().__init__(
            master,
            text=icon,
            font=(Fonts.FAMILY, 16),
            fg_color="transparent",
            hover_color=Colors.BG_CARD_HOVER,
            text_color=Colors.TEXT_SECONDARY,
            width=36, height=36,
            corner_radius=Spacing.CORNER_SM,
            **kwargs,
        )


# ─── Sidebar Nav Item ────────────────────────────────────────────────────────
class NavItem(ctk.CTkButton):
    """A sidebar navigation button."""

    def __init__(self, master, icon: str, text: str, active: bool = False,
                 **kwargs):
        self._icon = icon
        self._text = text
        fg = Colors.PRIMARY_GLOW if active else "transparent"
        text_col = Colors.PRIMARY_HOVER if active else Colors.TEXT_SECONDARY
        border_w = 0

        super().__init__(
            master,
            text=f"  {icon}   {text}",
            font=Fonts.BODY_BOLD if active else Fonts.BODY,
            fg_color=fg,
            hover_color=Colors.BG_CARD_HOVER,
            text_color=text_col,
            anchor="w",
            height=44,
            corner_radius=Spacing.CORNER_SM,
            border_width=border_w,
            **kwargs,
        )

    def set_active(self, active: bool):
        if active:
            self.configure(
                fg_color=Colors.PRIMARY_GLOW,
                text_color=Colors.PRIMARY_HOVER,
                font=Fonts.BODY_BOLD,
            )
        else:
            self.configure(
                fg_color="transparent",
                text_color=Colors.TEXT_SECONDARY,
                font=Fonts.BODY,
            )


# ─── Status Badge ────────────────────────────────────────────────────────────
class StatusBadge(ctk.CTkLabel):
    """A small coloured badge for status indicators."""

    STATUS_COLORS = {
        "ready":    (Colors.SUCCESS, "#064e3b"),
        "running":  (Colors.INFO,    "#1e3a5f"),
        "warning":  (Colors.WARNING, "#78350f"),
        "error":    (Colors.DANGER,  "#7f1d1d"),
        "idle":     (Colors.TEXT_MUTED, Colors.BG_CARD),
    }

    def __init__(self, master, status: str = "idle", text: str = "", **kwargs):
        colors = self.STATUS_COLORS.get(status, self.STATUS_COLORS["idle"])
        super().__init__(
            master,
            text=f" {text or status.upper()} ",
            font=Fonts.TINY,
            text_color=colors[0],
            fg_color=colors[1],
            corner_radius=4,
            **kwargs,
        )

    def set_status(self, status: str, text: str = ""):
        colors = self.STATUS_COLORS.get(status, self.STATUS_COLORS["idle"])
        self.configure(
            text=f" {text or status.upper()} ",
            text_color=colors[0],
            fg_color=colors[1],
        )


# ─── Labeled Input Row ───────────────────────────────────────────────────────
class LabeledEntry(ctk.CTkFrame):
    """A label + entry pair, stacked vertically."""

    def __init__(self, master, label: str, placeholder: str = "",
                 width: int = 200, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        ctk.CTkLabel(self, text=label, font=Fonts.SMALL_BOLD,
                     text_color=Colors.TEXT_SECONDARY, anchor="w").pack(
                         fill="x")

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            font=Fonts.BODY,
            fg_color=Colors.BG_INPUT,
            border_color=Colors.BORDER,
            text_color=Colors.TEXT_PRIMARY,
            width=width,
            height=36,
            corner_radius=Spacing.CORNER_SM,
        )
        self.entry.pack(fill="x", pady=(4, 0))

    def get(self) -> str:
        return self.entry.get()

    def set(self, value: str):
        self.entry.delete(0, "end")
        self.entry.insert(0, value)


# ─── Labeled Option Menu ─────────────────────────────────────────────────────
class LabeledOptionMenu(ctk.CTkFrame):
    """A label + dropdown pair, stacked vertically."""

    def __init__(self, master, label: str, values: list,
                 default: str = None, command=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        ctk.CTkLabel(self, text=label, font=Fonts.SMALL_BOLD,
                     text_color=Colors.TEXT_SECONDARY, anchor="w").pack(
                         fill="x")

        self.option = ctk.CTkOptionMenu(
            self,
            values=values,
            font=Fonts.BODY,
            fg_color=Colors.BG_INPUT,
            button_color=Colors.PRIMARY,
            button_hover_color=Colors.PRIMARY_HOVER,
            dropdown_fg_color=Colors.BG_CARD,
            dropdown_hover_color=Colors.BG_CARD_HOVER,
            dropdown_text_color=Colors.TEXT_PRIMARY,
            text_color=Colors.TEXT_PRIMARY,
            height=36,
            corner_radius=Spacing.CORNER_SM,
            command=command,
        )
        if default:
            self.option.set(default)
        self.option.pack(fill="x", pady=(4, 0))

    def get(self) -> str:
        return self.option.get()

    def set(self, value: str):
        self.option.set(value)


# ─── Console / Log Box ───────────────────────────────────────────────────────
class ConsoleBox(ctk.CTkFrame):
    """A dark console-style log viewer."""

    def __init__(self, master, height: int = 200, **kwargs):
        super().__init__(master, fg_color=Colors.BG_DARKEST,
                         corner_radius=Spacing.CORNER_SM,
                         border_width=1, border_color=Colors.BORDER,
                         **kwargs)

        header = ctk.CTkFrame(self, fg_color="transparent", height=30)
        header.pack(fill="x", padx=Spacing.MD, pady=(Spacing.SM, 0))

        ctk.CTkLabel(header, text="⬤", font=(Fonts.FAMILY, 8),
                     text_color=Colors.ACCENT_EMERALD).pack(side="left")
        ctk.CTkLabel(header, text="  Console Output", font=Fonts.MONO_SMALL,
                     text_color=Colors.TEXT_MUTED).pack(side="left")

        self.textbox = ctk.CTkTextbox(
            self,
            font=Fonts.MONO_SMALL,
            fg_color="transparent",
            text_color=Colors.ACCENT_EMERALD,
            height=height,
            wrap="word",
            activate_scrollbars=True,
        )
        self.textbox.pack(fill="both", expand=True, padx=Spacing.MD,
                          pady=(4, Spacing.MD))
        self.textbox.configure(state="disabled")

    def log(self, message: str, color: str = None):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f">>> {message}\n")
        self.textbox.see("end")
        self.textbox.configure(state="disabled")

    def clear(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")
