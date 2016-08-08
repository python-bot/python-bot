_color_names = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')
_foreground = {_color_names[x]: '3%s' % x for x in range(8)}
_background = {_color_names[x]: '4%s' % x for x in range(8)}

_RESET = '0'
_opt_dict = {'bold': '1', 'underscore': '4', 'blink': '5', 'reverse': '7', 'conceal': '8'}


def colorize(text='', opts=(), **kwargs):
    """
    Returns your text, enclosed in ANSI graphics codes.
    Depends on the keyword arguments 'fg' and 'bg', and the contents of
    the opts tuple/list.
    Returns the RESET code if no parameters are given.
    Valid colors:
        'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
    Valid options:
        'bold'
        'underscore'
        'blink'
        'reverse'
        'conceal'
        'noreset' - string will not be auto-terminated with the RESET code
    Examples:
        colorize('hello', fg='red', bg='blue', opts=('blink',))
        colorize()
        colorize('goodbye', opts=('underscore',))
        print(colorize('first line', fg='red', opts=('noreset',)))
        print('this should be red too')
        print(colorize('and so should this'))
        print('this should not be red')
    """
    code_list = []
    if text == '' and len(opts) == 1 and opts[0] == 'reset':
        return '\x1b[%sm' % _RESET
    for k, v in kwargs.items():
        if k == 'fg':
            code_list.append(_foreground[v])
        elif k == 'bg':
            code_list.append(_background[v])
    for o in opts:
        if o in _opt_dict:
            code_list.append(_opt_dict[o])
    if 'noreset' not in opts:
        text = '%s\x1b[%sm' % (text or '', _RESET)
    return '%s%s' % (('\x1b[%sm' % ';'.join(code_list)), text or '')


def make_style(opts=(), **kwargs):
    """
    Returns a function with default parameters for colorize()
    Example:
        bold_red = make_style(opts=('bold',), fg='red')
        print(bold_red('hello'))
        KEYWORD = make_style(fg='yellow')
        COMMENT = make_style(fg='blue', opts=('bold',))
    """
    return lambda text: colorize(text, opts, **kwargs)


NOCOLOR_PALETTE = 'nocolor'
DARK_PALETTE = 'dark'
LIGHT_PALETTE = 'light'


class PaletteStyle:
    error = "ERROR"
    success = "SUCCESS"
    warning = "WARNING"
    notice = "NOTICE"
    quick_reply = "QUICK_REPLY"
    button = "BUTTON"
    text = "TEXT"
    caption = "CAPTION"
    typing = "TYPING"


PALETTES = {
    NOCOLOR_PALETTE: {
        PaletteStyle.error: {},
        PaletteStyle.success: {},
        PaletteStyle.warning: {},
        PaletteStyle.notice: {},
        PaletteStyle.quick_reply: {},
        PaletteStyle.button: {},
        PaletteStyle.text: {},
        PaletteStyle.typing: {},
        PaletteStyle.caption: {},
        # 'SQL_COLTYPE': {},
        # 
        # 'SQL_TABLE': {},
        # 'HTTP_INFO': {},
        # 'HTTP_REDIRECT': {},
        # 'HTTP_NOT_MODIFIED': {},
        # 'HTTP_BAD_REQUEST': {},
        # 'HTTP_NOT_FOUND': {},
        # 'HTTP_SERVER_ERROR': {},
        # 'MIGRATE_HEADING': {},
        #
        # 'MIGRATE_SUCCESS': {},
        # 'MIGRATE_FAILURE': {},
    },
    DARK_PALETTE: {
        PaletteStyle.error: {'fg': 'red', 'opts': ('bold',)},
        PaletteStyle.success: {'fg': 'green', 'opts': ('bold',)},
        PaletteStyle.warning: {'fg': 'yellow', 'opts': ('bold',)},
        PaletteStyle.notice: {'fg': 'red'},
        PaletteStyle.quick_reply: {'fg': 'green', 'opts': ('bold',)},
        PaletteStyle.button: {'fg': 'yellow'},
        PaletteStyle.text: {},
        PaletteStyle.typing: {'fg': 'white'},
        PaletteStyle.caption: {'opts': ('bold',)},
        # 'SQL_COLTYPE': {'fg': 'green'},
        # 
        # 'SQL_TABLE': {'opts': ('bold',)},
        # 'HTTP_INFO': {'opts': ('bold',)},
        # 'HTTP_SUCCESS': {},
        # 'HTTP_REDIRECT': {'fg': 'green'},
        # 'HTTP_NOT_MODIFIED': {'fg': 'cyan'},
        # 'HTTP_BAD_REQUEST': {'fg': 'red', 'opts': ('bold',)},
        # 'HTTP_NOT_FOUND': {'fg': 'yellow'},
        # 'HTTP_SERVER_ERROR': {'fg': 'magenta', 'opts': ('bold',)},
        # 'MIGRATE_HEADING': {'fg': 'cyan', 'opts': ('bold',)},
        #
        # 'MIGRATE_SUCCESS': {'fg': 'green', 'opts': ('bold',)},
        # 'MIGRATE_FAILURE': {'fg': 'red', 'opts': ('bold',)},
    },
    LIGHT_PALETTE: {
        PaletteStyle.error: {'fg': 'red', 'opts': ('bold',)},
        PaletteStyle.success: {'fg': 'green', 'opts': ('bold',)},
        PaletteStyle.warning: {'fg': 'yellow', 'opts': ('bold',)},
        PaletteStyle.notice: {'fg': 'red'},
        PaletteStyle.quick_reply: {'fg': 'green', 'opts': ('bold',)},
        PaletteStyle.button: {'fg': 'blue'},
        PaletteStyle.text: {},
        PaletteStyle.typing: {'fg': 'white'},
        PaletteStyle.caption: {'opts': ('bold',)},
        # 'SQL_COLTYPE': {'fg': 'green'},
        # 
        # 'SQL_TABLE': {'opts': ('bold',)},
        # 'HTTP_INFO': {'opts': ('bold',)},
        # 'HTTP_SUCCESS': {},
        # 'HTTP_REDIRECT': {'fg': 'green', 'opts': ('bold',)},
        # 'HTTP_NOT_MODIFIED': {'fg': 'green'},
        # 'HTTP_BAD_REQUEST': {'fg': 'red', 'opts': ('bold',)},
        # 'HTTP_NOT_FOUND': {'fg': 'red'},
        # 'HTTP_SERVER_ERROR': {'fg': 'magenta', 'opts': ('bold',)},
        # 'MIGRATE_HEADING': {'fg': 'cyan', 'opts': ('bold',)},
        #
        # 'MIGRATE_SUCCESS': {'fg': 'green', 'opts': ('bold',)},
        # 'MIGRATE_FAILURE': {'fg': 'red', 'opts': ('bold',)},
    }
}

DEFAULT_PALETTE = DARK_PALETTE


def print_palette(text, style_name):
    print(colorize(text, **PALETTES[DEFAULT_PALETTE][style_name]))


def centralize(s, length=80):
    if s is None:
        s = ""
    sep_length = (length - len(s)) / 2
    if s:
        sep_length -= 1
        s = " " + s + " "
    result = "=" * int(sep_length) + s + "=" * round(sep_length)
    return result
