import tkinter.ttk as ttk

# color_blue          = '#2B44FF'
# color_navy          = '#2026A1'
# color_navy_dark     = '#1E2FB1'
# color_white         = '#FFFFFF'
# color_white_broken  = '#F1F1F2'
# color_grey_light    = '#ECECED'
# color_grey_mid      = '#999999'
# color_grey_dark     = '#333333'

colors = {
    'blue'          : '#2B44FF',
    'navy'          : '#2026A1',
    'navy_dark'     : '#1E2FB1',
    'white'         : '#FFFFFF',
    'white_broken'  : '#F1F1F2',
    'grey_light'    : '#ECECED',
    'grey_mid'      : '#999999',
    'grey_dark'     : '#333333',
}

def init_style():
    style = ttk.Style()
    # style.configure('.',
    #                     font=('Arial', 12),
    #                     background=color_navy,
    #                     foreground=color_grey_light)

    style.configure('TButton',
                        font=('Arial', 12, 'bold'),
                        padding=12,
                        background=colors['white_broken'],
                        foreground=colors['grey_dark'],
                        borderwidth=0,
                        highlightthickness=0)

    style.map('TButton',
                        background=[('active', colors['grey_light']), ('pressed', colors['grey_mid'])])

    style.configure('P.TButton',
                        font=('Arial', 12, 'bold'),
                        padding=12,
                        background=colors['blue'],
                        foreground=colors['grey_light'],
                        borderwidth=0,
                        highlightthickness=0)

    style.map('P.TButton',
                        background=[('active', colors['navy']), ('pressed', colors['navy_dark'])],
                        foreground=[('active', colors['white_broken']), ('pressed', colors['white'])])
    
    style.configure('TEntry',
                        font=('Arial', 12),
                        padding=10,
                        background=colors['grey_light'],
                        fieldbackground=colors['grey_light'],
                        foreground=colors['grey_dark'],
                        borderwidth=0,
                        highlightthickness=0)
    style.map('TEntry',
                        background=[('active', colors['white_broken']), ('focus', colors['white_broken'])],
                        fieldbackground=[('active', colors['white_broken']), ('focus', colors['white_broken'])],)

    style.configure('TLabel',
                        font=('Arial', 12))
    
    style.configure('Display.TLabel',
                        font=('Arial', 36, 'bold'),
                        background=colors['navy'],
                        foreground=colors['white'])
    
    style.configure('Title.TLabel',
                        font=('Arial', 24),
                        background=colors['navy'],
                        foreground=colors['white'])

    style.configure('Subtitle.TLabel',
                        font=('Arial', 18),
                        background=colors['navy'],
                        foreground=colors['white'])
                        