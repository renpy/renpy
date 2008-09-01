init -100 python:

    style.stats_frame = Style(style.frame)
    style.stats_vbox = Style(style.vbox)

    style.stats_label = Style(style.label)
    style.stats_label_text = Style(style.label_text)

    style.stat_side = Style(style.default)

    style.stat_label = Style(style.label)
    style.stat_label_text = Style(style.label_text)
    style.stat_bar = Style(style.bar)
    style.stat_value_label = Style(style.label)
    style.stat_value_label_text = Style(style.label_text)
        
    __dse_stats = [ ]

    class __Stat(object):

        def __init__(self, name, var, default, max):
            self.name = name
            self.var = var
            self.default = default
            self.max = max

    def __init_stats():
        for s in __dse_stats:
            setattr(store, s.var, s.default)

    config.start_callbacks.append(__init_stats)
            
    def register_stat(name, var, default, max):
        __dse_stats.append(__Stat(name, var, default, max))

    def normalize_stats():
        for s in __dse_stats:

            v = getattr(store, s.var)

            if v > s.max:
                v = s.max
            if v < 0:
                v = 0

            setattr(store, s.var, v)


    def display_stats(name=True, bar=True, value=True, max=True):

        normalize_stats()
        
        ui.window(style=style.stats_frame)
        ui.vbox(style=style.stats_vbox)
            
        layout.label("Statistics", "stats")
        
        for s in __dse_stats:
            v = getattr(store, s.var)

            ui.side(['l', 'r', 'c'], style=style.stat_side)

            if name:
                layout.label(s.name, "stat")
            else:
                ui.nul()

            if value and max:
                layout.label("%d/%d" % (v, s.max), "stat_value")
            elif value:
                layout.label("%d" % (v,), "stat_value")
            elif max:
                layout.label("%d" % (max,), "stat_value")
            else:
                ui.null()

            if bar:
                ui.bar(s.max, v, style=style.stat_bar)
            else:
                ui.null()

            ui.close()
                
        ui.close()

        
    
    
