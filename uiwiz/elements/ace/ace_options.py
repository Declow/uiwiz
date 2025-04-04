from typing import Any, List, Literal, Optional, TypedDict, Union


class SqlOptions(TypedDict):
    tables: list[str]
    columns: list[str]


class AceOptions(TypedDict):
    animated_scroll: Optional[bool]
    auto_scroll_editor_into_view: Optional[bool]
    behaviours_enabled: Optional[bool]
    copy_with_empty_selection: Optional[bool]
    cursor_style: Optional[Literal["ace", "slim", "smooth", "wide"]]
    custom_scrollbar: Optional[bool]
    display_indent_guides: Optional[bool]
    drag_delay: Optional[int]
    drag_enabled: Optional[bool]
    enable_auto_indent: Optional[bool]
    enable_basic_autocompletion: Optional[Union[bool, List[Any]]]
    enable_codeLens: Optional[bool]
    enable_keyboard_accessibility: Optional[bool]
    enable_live_autocompletion: Optional[Union[bool, List[Any]]]
    enable_mobile_menu: Optional[bool]
    enable_multiselect: Optional[bool]
    enable_snippets: Optional[bool]
    fade_fold_widgets: Optional[bool]
    first_line_number: Optional[int]
    fixed_width_gutter: Optional[bool]
    focus_timeout: Optional[int]
    fold_style: Optional[Literal["markbegin", "markbeginend", "manual"]]
    font_family: Optional[str]
    font_size: Optional[Union[str, int]]
    h_scroll_bar_always_visible: Optional[bool]
    has_css_transforms: Optional[bool]
    highlight_active_line: Optional[bool]
    highlight_gutter_line: Optional[bool]
    highlight_indent_guides: Optional[bool]
    highlight_selected_word: Optional[bool]
    indented_soft_wrap: Optional[bool]
    keyboard_handler: Optional[str]
    live_autocompletion_delay: Optional[int]
    live_autocompletion_threshold: Optional[int]
    max_lines: Optional[int]
    max_pixel_height: Optional[int]
    merge_undo_deltas: Optional[Union[bool, Literal["always"]]]
    min_lines: Optional[int]
    mode: Optional[str]
    navigate_within_soft_tabs: Optional[bool]
    newLine_mode: Optional[Literal["auto", "windows", "unix"]]
    overwrite: Optional[bool]
    placeholder: Optional[str]
    print_margin: Optional[Union[int, bool]]
    print_margin_column: Optional[int]
    read_only: Optional[bool]
    relative_line_numbers: Optional[bool]
    scroll_past_end: Optional[int]
    scroll_speed: Optional[int]
    selection_style: Optional[Literal["line", "text", "fullLine", "screenLine"]]
    show_fold_widgets: Optional[bool]
    show_folded_annotations: Optional[bool]
    show_gutter: Optional[bool]
    show_invisibles: Optional[bool]
    show_line_numbers: Optional[bool]
    show_print_margin: Optional[bool]
    tab_size: Optional[int]
    text_input_aria_label: Optional[str]
    theme: Optional[str]
    tooltip_follows_mouse: Optional[bool]
    use_resize_observer: Optional[bool]
    use_soft_tabs: Optional[bool]
    use_svg_gutter_icons: Optional[bool]
    use_worker: Optional[bool]
    v_scroll_bar_always_visible: Optional[bool]
    value: Optional[str]
    wrap: Optional[Union[int, float, bool, Literal["off", "free", "printmargin"]]]
    wrap_behaviours_enabled: Optional[bool]
    wrap_method: Optional[Literal["code", "text", "auto"]]
