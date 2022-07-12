from functions import config, init, get_scoop_dir
from dearpygui.dearpygui import *

def start():
    """
    Start the GUI.
    """
    default_width = 200
    create_context()
    with window(tag="main"):
        with menu_bar():
            add_button(label='Save', tag='save', callback=config.write)

        with child_window(tag='child', border=False):
            with tab_bar(label='tabbar'):
                with tab(label='Settings', tag='settings'):

                    add_text('Interpolation')
                    add_checkbox(tag='ip_enabled', label='Enabled')
                    add_checkbox(tag='ip_gpu', label='GPU Rendering')
                    add_slider_int(tag='ip_fps', label="FPS",
                                   min_value=120, max_value=3840)
                    add_combo(tag='ip_speed', label="Speed", items=[
                        'Medium', 'Fast', 'Faster'], width=default_width)
                    add_combo(tag='ip_tuning', label="Tuning", items=[
                        'Film', 'Animation', 'Smooth', 'Weak'], width=default_width)
                    add_combo(tag='ip_algo', label="Algorithm", items=[
                        '1', '2', '11', '13', '22', '23'], width=default_width)

                    add_separator()
                    add_text('Frame Blending')
                    add_checkbox(tag='fb_enabled', label='Enabled')

                    add_slider_int(tag='fb_fps', label="FPS",
                                   min_value=30, max_value=120)
                    add_slider_float(tag='fb_intensity',
                                     label='Intensity', max_value=4)
                    add_combo(tag='fb_weighting', label='Weighting', items=[
                        'Equal', 'Gaussian', 'Gaussian Sym', 'Pyramid', 'Pyramid Sym'], width=default_width)

                    add_separator()
                    add_text('Flowblur')
                    add_checkbox(tag='flb_enabled', label='Enabled')
                    add_slider_int(tag='flb_amount', label="Amount")
                    add_input_text(tag='flb_mask', label='Mask')

                    add_separator()
                    add_text('Deduplication')
                    add_slider_float(tag='deduplthreshold',
                                     label='Deduplication Threshold', max_value=1)

                    add_separator()
                    add_text('Timescale')
                    add_slider_float(tag='timescale_in',
                                     label='Input',  max_value=4)
                    add_slider_float(tag='timescale_out',
                                     label='Output', max_value=4)

                with tab(label='Output', tag='output'):
                    add_text('Video')
                    add_input_text(tag='folder', label='Folder')
                    add_input_text(tag='container',
                                   label='Container', width=default_width)
                    add_combo(tag='flavors', label='Flavors',
                              items=['Fruits', 'Smoothie'], width=default_width)

                    add_separator()
                    add_text('Encoding')
                    add_input_text(tag='process', label='Process')
                    add_input_text(tag='args', label='Arguments')

                with tab(label='Miscellaneous', tag='misc'):
                    add_checkbox(label='Verbose', tag='verbose')
                    add_checkbox(label='Stay on Top', tag='stay on top')
                    add_input_text(label='MPV', tag='mpv bin')
                    add_input_int(label='Ding', tag='ding after',
                                  width=default_width)
            

    init(fr"{get_scoop_dir()}\apps\smoothie\current\Smoothie\settings\recipe.yaml")
    create_viewport(title='Smoothie GUI', width=800, height=600)
    set_viewport_resizable(False)
    setup_dearpygui()
    show_viewport()
    set_primary_window("main", True)
    start_dearpygui()
    destroy_context()