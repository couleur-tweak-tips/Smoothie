from functions import config, init, info
from os import path
from sys import exit
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
            add_button(label='Load', tag='load', callback=config.load)
            add_button(label='About', tag='about', callback=info.about)
            add_button(label='Help', tag='help', callback=info.help)
            
        with child_window(tag='child', border=False):
            with tab_bar(label='tabbar'):
                with tab(label='Settings', tag='settings'):

                    with collapsing_header(label='Interpolation', default_open=True):
                        add_separator()
                        add_checkbox(tag='ip_enabled', label='Enabled')
                        add_checkbox(tag='ip_gpu', label='GPU Rendering')
                        add_text('')

                        add_slider_int(tag='ip_fps', label="FPS",
                                       min_value=120, max_value=3840)
                        add_text('')

                        add_combo(tag='ip_speed', label="Speed", items=[
                            'Medium', 'Fast', 'Faster'], width=default_width)

                        with group(horizontal=True):
                            add_combo(tag='ip_tuning', label="Tuning   ", items=[
                                'Animation', 'Film', 'Smooth', 'Weak'], width=default_width)
                            add_button(tag='ip_tuning_tooltip',
                                       label='?', height=20, width=20)
                            with tooltip('ip_tuning_tooltip'):
                                add_text('''Determines the accuracy of smoothness of the interpolated video.\n
Animation - Least Accuracy + Best Clarity
Smooth - Balanced Accuracy & Clarity
Film - Better Accuracy + Weak Clarity
Weak - Best Accuracy + Least Clarity'''.strip('\n'))

                        with group(horizontal=True):
                            add_combo(tag='ip_algo', label="Algorithm", items=[
                                1, 2, 10, 11, 13, 21, 23], width=default_width)
                            add_button(tag='ip_algo_tooltip',
                                        label='?', height=20, width=20)
                            with tooltip('ip_algo_tooltip'):
                                add_text('''Determines the algorithm used to interpolate the video.\n
1 -  Fastest
2 -  Sharp
10 - By Blocks (CPU Only)
11 - Simple Lite
13 - Standard 
21 - Simple
23 - Complicated'''.strip('\n'))

                        add_text('')
                        add_separator()

                    with collapsing_header(label='Frame Blending', default_open=True):
                        add_separator()
                        add_checkbox(tag='fb_enabled', label='Enabled')
                        add_text('')

                        add_slider_int(tag='fb_fps', label="FPS",
                                       min_value=30, max_value=120)
                        add_slider_float(tag='fb_intensity',
                                         label='Intensity', max_value=4)

                        add_text('')
                        add_combo(tag='fb_weighting', label='Weighting', items=[
                            'Equal', 'Gaussian', 'Gaussian Sym', 'Pyramid', 'Pyramid Sym'], width=default_width)
                        add_text('')
                        add_separator()

                    with collapsing_header(label='Miscellaneous'):
                        add_separator()
                        add_text('Flowblur')
                        add_checkbox(tag='flb_enabled', label='Enabled')
                        add_text('')
                        add_slider_int(tag='flb_amount',
                                       label="Amount", max_value=200)
                        add_input_text(tag='flb_mask', label='Mask')

                        add_separator()
                        add_text('Deduplication')
                        add_text('')
                        add_slider_float(tag='deduplthreshold',
                                         label='Deduplication Threshold', max_value=1)

                        add_separator()
                        add_text('Timescale')
                        add_text('')
                        add_slider_float(tag='timescale_in',
                                         label='Input',  max_value=4)
                        add_slider_float(tag='timescale_out',
                                         label='Output', max_value=4)

                with tab(label='Output', tag='output'):
                    add_text('Video')
                    add_input_text(tag='folder', label='Output Folder')
                    add_input_text(tag='container',
                                   label='Container', width=default_width)
                    add_combo(tag='flavors', label='Flavors',
                              items=['Fruits', 'Smoothie'], width=default_width)

                    add_separator()
                    add_text('Encoding')
                    add_input_text(tag='process', label='Process')
                    add_input_text(tag='args', label='Arguments')

                with tab(label='Extras'):
                    add_checkbox(label='Verbose', tag='verbose')
                    add_checkbox(label='Stay on Top', tag='stay on top')
                    add_input_text(label='MPV', tag='mpv bin')
                    add_input_int(label='Ding', tag='ding after',
                                  width=default_width)

    init(f"{path.dirname(__file__)}/../../settings/recipe.yaml")
    create_viewport(title='Smoothie GUI', width=800, height=600)
    set_viewport_resizable(False)
    setup_dearpygui()
    show_viewport()
    set_primary_window("main", True)
    start_dearpygui()
    destroy_context()
    exit(0)