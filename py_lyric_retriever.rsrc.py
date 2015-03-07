{
    'application': {
        'type': 'Application',
        'name': 'Template',
        'backgrounds': [{
                'type': 'Background',
                'name': 'bgLyricRetriever',
                'title': u'Lyric Get 4.6.1 beta',
                'size': (626, 630),
                'statusBar': 1,
                'icon': 'lyric_ico.ico',

                'strings': {
                    u'error_IOError': u'IOError: the lyric site is not available now, or the network connection has problem.',
                },

                'components': [

                    {
                        'type': 'TextField',
                        'name': 'urlTextField',
                        'position': (50, 10),
                        'size': (455, 25),
                        'font': {
                            'faceName': u'Tahoma',
                            'family': 'sansSerif',
                            'size': 12
                        },
                        'text': u'please input the url of lyric',
                    },

                    {
                        'type': 'Button',
                        'name': 'queryButton',
                        'position': (520, 10),
                        'size': (80, 25),
                        'default': True,
                        'font': {
                            'faceName': u'Tahoma',
                            'family': 'sansSerif',
                            'size': 12
                        },
                        'label': u'Download',
                    },

                    {
                        'type': 'TextArea',
                        'name': 'lyricTextArea',
                        'position': (10, 40),
                        'size': (600, 500),
                        'editable': False,
                        'font': {
                            'faceName': u'Meiryo',
                            'family': 'sansSerif',
                            'size': 12
                        },
                    },

                    {
                        'type': 'StaticText',
                        'name': 'urlText',
                        'position': (10, 10),
                        'font': {
                            'faceName': u'Tahoma',
                            'family': 'sansSerif',
                            'size': 12
                        },
                        'text': u'URL:',
                    },

                ]# end components
            }# end background
        ]# end backgrounds
    }
}