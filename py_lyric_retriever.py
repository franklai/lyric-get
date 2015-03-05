#!/usr/bin/python
# coding: utf-8
import os
import wx
import wx.animate
import threading
from PythonCard import model, dialog, log
import lyric_engine

class UrlThread(threading.Thread):
    def __init__(self, url, window):
        threading.Thread.__init__(self)
        self.window = window
        self.url = url

    def run(self):
        engine = lyric_engine.Lyric(self.url)

        try:
            log.debug('in UrlThread')
            lyric = engine.get_lyric()
            self.window.thread_finished(lyric)
        except IOError:
            self.window.error_io_erorr()
        except TypeError:
            self.window.error_type_error()

class Main(model.Background):
    def on_initialize(self, event):
        self.components.urlTextField.setFocus()
        self.lyric = ''

        ag_fname = 'waiting.gif'
        ag = wx.animate.Animation(ag_fname)
        self.ag_ctrl = wx.animate.AnimationCtrl(self, -1, ag)
        self.ag_ctrl.SetPosition((289, 100))
        self.ag_ctrl.Hide()

        # default timeout test
        import socket
        timeout = 5.0
        result = socket.setdefaulttimeout(timeout)

    def on_menuFileSave_select(self, event):
        """Save content in urlTextField using UTF-8 encoding"""
        # default save directory in home dir
        save_dir = os.path.expanduser('~')
        if os.name == 'nt':
            # windows default in Desktop
            save_dir = os.path.join(save_dir, u'Desktop')

        result = dialog.fileDialog(self, 
            'Save', 
            save_dir,
            'lyric.txt',
            'Text Files (*.txt)|*.txt|All Files (*.*)|*.*',
            wx.SAVE | wx.OVERWRITE_PROMPT,
        )

        if result.accepted:
            f = open(result.paths[0], 'wb')
            string = self.components.lyricTextArea.text
            f.write(string.encode('utf8'))
            f.close()

    def on_activate(self, event):
        self.components.urlTextField.setFocus()
        self.components.urlTextField.SetSelection(-1, -1)

    def on_queryButton_mouseClick(self, event):
        # get lyric page url
        url = self.components.urlTextField.text

        # processing 
        self.process_url(url)

    def on_testUrl_command(self, event):
        """based on the name of menu item, do lyric site test"""
        raw_name = event.target.name
        site_name = raw_name[raw_name.find('_') + 1:] 
        self.components.urlTextField.text = lyric_engine.get_test_url(site_name)

        # do query
        self.on_queryButton_mouseClick(event)

    def on_launchBrowser_command(self, event):
        """ based on the name of menu item, launch browser to the site"""
        raw_name = event.target.name
        site_name = raw_name[raw_name.find('_') + 1:] 
        self.open_web_link(lyric_engine.get_site_url(site_name))

    def open_web_link(self, url):
        import webbrowser
        webbrowser.open_new(url)

    def process_url(self, url):
        url = url.strip()

        # verify url, if invalid, popu a warning dialog
        url = self.verify_url(url)
        if url == False:
            self.show_invalid()
            return False

        # 
        self.lock_input()

        # call lyric engine to get lyric
        self.url = url
        thread = UrlThread(url, self)
        thread.start()
    
    def thread_finished(self, lyric):
        # show lyric
        self.show_lyric(self.url, lyric)

        self.statusBar.text = 'lyric retrieved!'

        self.unlock_input()

    def show_lyric(self, url, lyric):
        # set the first line as the url of lyric
        #       then the following is the lyric
        self.statusBar.text = 'showing lyric'
#         string = unicode('lyric from '+url) + u'\n\n' + lyric
        string = lyric
        self.components.lyricTextArea.text = string

    def get_lyric(self, url):
        """ choose different processing function to handle """
        self.statusBar.text = 'processing url...'
        engine = lyric_engine.Lyric(url)

        try:
            lyric = engine.get_lyric()
        except IOError:
            raise

        return lyric

    def verify_url(self, url):
        """ check if 'http://' is in the input string """
        if url.find('http://') != 0:
            return False
        else:
            return url

    def show_invalid(self):
        self.statusBar.text = 'invalid url'
        result = dialog.alertDialog(self, 'Invalid URL', 'Error')

    def error_type_error(self):
        log.debug('TypeError')
        self.unlock_input()
        result = dialog.alertDialog(self, 'this URL is not supported', 'Error')

    def error_io_erorr(self):
        log.debug('IOError')
        self.unlock_input()
#         result = dialog.alertDialog(self, 'IOError', 'Error')
        strings = self.resource.strings
        result = dialog.alertDialog(self, strings.error_IOError, 'Error')

    def lock_input(self):
        # clear status
        self.statusBar.text = ''

        # disable query button (avoid multiple queries) and url text field 
        self.components.queryButton.enabled = False
        self.components.urlTextField.enabled = False

        # show loading icon
        self.components.lyricTextArea.visible = False
        #self.ag_ctrl.SetBackgroundColour(wx.Colour('PINK1'))
        self.ag_ctrl.Play()
        self.ag_ctrl.Show()

    def unlock_input(self):
        # enable query button and url text field
        self.components.queryButton.enabled = True
        self.components.urlTextField.enabled = True

        # hide loading icon
        self.ag_ctrl.Stop()
        self.ag_ctrl.Hide()
        self.components.lyricTextArea.visible = True

if __name__ == '__main__':
#     try:
#         import psyco
#         psyco.full()
#     except ImportError:
#         pass
    app = model.Application(Main)
    app.MainLoop()

