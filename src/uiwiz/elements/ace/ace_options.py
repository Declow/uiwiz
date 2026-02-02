from __future__ import annotations

from typing import Any, Literal, TypedDict


class SqlOptions(TypedDict):
    tables: list[str]
    columns: list[str]


class AceOptions(TypedDict):
    animated_scroll: bool | None
    auto_scroll_editor_into_view: bool | None
    behaviours_enabled: bool | None
    copy_with_empty_selection: bool | None
    cursor_style: Literal["ace", "slim", "smooth", "wide"] | None
    custom_scrollbar: bool | None
    display_indent_guides: bool | None
    drag_delay: int | None
    drag_enabled: bool | None
    enable_auto_indent: bool | None
    enable_basic_autocompletion: bool | list[Any] | None
    enable_codeLens: bool | None
    enable_keyboard_accessibility: bool | None
    enable_live_autocompletion: bool | list[Any] | None
    enable_mobile_menu: bool | None
    enable_multiselect: bool | None
    enable_snippets: bool | None
    fade_fold_widgets: bool | None
    first_line_number: int | None
    fixed_width_gutter: bool | None
    focus_timeout: int | None
    fold_style: Literal["markbegin", "markbeginend", "manual"] | None
    font_family: str | None
    font_size: str | int | None
    h_scroll_bar_always_visible: bool | None
    has_css_transforms: bool | None
    highlight_active_line: bool | None
    highlight_gutter_line: bool | None
    highlight_indent_guides: bool | None
    highlight_selected_word: bool | None
    indented_soft_wrap: bool | None
    keyboard_handler: str | None
    live_autocompletion_delay: int | None
    live_autocompletion_threshold: int | None
    max_lines: int | None
    max_pixel_height: int | None
    merge_undo_deltas: bool | Literal["always"] | None
    min_lines: int | None
    mode: str | None
    navigate_within_soft_tabs: bool | None
    newLine_mode: Literal["auto", "windows", "unix"] | None
    overwrite: bool | None
    placeholder: str | None
    print_margin: int | bool | None
    print_margin_column: int | None
    read_only: bool | None
    relative_line_numbers: bool | None
    scroll_past_end: int | None
    scroll_speed: int | None
    selection_style: Literal["line", "text", "fullLine", "screenLine"] | None
    show_fold_widgets: bool | None
    show_folded_annotations: bool | None
    show_gutter: bool | None
    show_invisibles: bool | None
    show_line_numbers: bool | None
    show_print_margin: bool | None
    tab_size: int | None
    text_input_aria_label: str | None
    theme: str | None
    tooltip_follows_mouse: bool | None
    use_resize_observer: bool | None
    use_soft_tabs: bool | None
    use_svg_gutter_icons: bool | None
    use_worker: bool | None
    v_scroll_bar_always_visible: bool | None
    value: str | None
    wrap: int | float | bool | Literal["off", "free", "printmargin"] | None
    wrap_behaviours_enabled: bool | None
    wrap_method: Literal["code", "text", "auto"] | None
