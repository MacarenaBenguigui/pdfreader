
icon_url = "https://i.postimg.cc/mDCmmtp8/Logo2-sinfondo-x1024.png"

# HTML para el título e ícono
title_html = f"""
<div style="font-size: 35px; font-weight: bold; display: flex; align-items: center;">
    <img src="{icon_url}" style="width: 48px; margin-right: 15px;">
    Inneva Chat
</div>
"""

html_hide = f"""
<head>
<link rel="shortcut icon" type="image/png" href="{icon_url}">
</head>
<style>

    #[data-testid="stToolbar"] {{visibility: hidden !important;}}

    #MainMenu {{visibility: hidden;}}

    #footer {{visibility: hidden !important;}}
  
    #header {{visibility: hidden;}} 
</style>
"""



def generate_html_with_icon(icon_url, text, icon_size="100px", text_margin="20px", space_between="30px", text_size="20px"):
    """Genera una cadena HTML para mostrar un ícono y texto con tamaño, margen, espacio entre conjuntos personalizados y tamaño de texto."""
    html_string = f'''
    <div style="margin-bottom: {space_between}; display: flex; align-items: center;">
        <img src="{icon_url}" style="width: {icon_size}; display: inline-block; margin-right: {text_margin};">
        <span style="font-size: {text_size};">{text}</span>
    </div>
    '''
    return html_string
