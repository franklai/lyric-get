# coding: utf8
##### ##### ##### ##### ##### ##### ##### ##### ##### 
# Lyric Retriever Engine
# http://franks543.blogspot.com/
##### ##### ##### ##### ##### ##### ##### ##### ##### 
import logging
import os
import re
import sys

# load all engine
def filenameToModuleName(f):
    items = f.split('\\')
    if len(items) == 3:
        f = items[2]
    return os.path.splitext(f)[0]

def appendPath(dirs):
    for d in dirs:
        full_dir = os.path.join(os.path.dirname(__file__), d)
        if full_dir not in sys.path:
            sys.path.append(full_dir)
appendPath(['', 'modules', 'include'])

try:
    jibun = __import__('lyric_engine')
    # test if load from zip (py2exe)
    if hasattr(jibun, '__loader__'):
        loader = jibun.__loader__
        files = __import__('__init__').__loader__._files.keys()
        test = re.compile('lyric_engine.modules.[a-z]')
        files = [x for x in files if test.search(x)]
        moduleNames = [filenameToModuleName(x) for x in files]
        modules = [__import__(x) for x in moduleNames if x is not '__init__']
    else:
        raise Exception('do default')
except:
    module_dir = os.path.join(os.path.dirname(__file__), 'modules')
    files = os.listdir(module_dir)
#    print(files)
    test = re.compile('^[a-z].*\.py$')
    files = [x for x in files if test.search(x)]
    moduleNames = [filenameToModuleName(x) for x in files]
    modules = [__import__(x) for x in moduleNames]

#print(moduleNames)

site_dict = {}
for module in modules:
    site_dict[module.site_index] = module

class Lyric:
    def __init__(self, url):
        if type(url).__name__ == 'unicode':
            self.url = url.encode('utf8')
        else:
            self.url = url

    def get_lyric(self):
        handler = self.get_handler()
        
        if not handler:
            return 'This site is not support yet.'

        try:
            lyric = handler(self.url)
        except IOError:
            raise
        except TypeError:
            raise
        except IndexError:
            raise

        return lyric


    def get_handler(self):
        for key in site_dict:
            item = site_dict[key]

            if self.url.find(item.site_keyword) != -1:
                return item.get_lyric

        # no match handler
        return None


def get_site_url(site_index):
    if site_index in site_dict:
        return site_dict[site_index].site_url
    return None

def get_test_url(site_index):
    if site_index in site_dict:
        return site_dict[site_index].test_url
    return None

def get_test_result(site_index):
    if site_index in site_dict:
        if hasattr(site_dict[site_index], 'test_site'):
            return site_dict[site_index].test_site()
    return None

def get_all_index():
    return site_dict.keys()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    def runProfiling():
        import cProfile
        cProfile.run('getLyric()', 'profiling_result.txt')
    
    def testEverySite():
        output = '_____site.test.result.txt'
        out = open(output, 'wb')

        def echo(string):
            out.write(string + '\n')
            out.flush()
            print(string)

        keys = site_dict.keys()
        keys.sort()

        for key in keys:
            try:
                url = get_test_url(key)
                string = 'Testing site [%s], url[%s]' % (key, url, )
                echo(string)

                engine = Lyric(url)
                lyric = engine.get_lyric()

                string = '\t[%d] of site [%s] lyric' % (len(lyric), url, )
                echo(string)
                string = '\n == lyric ==\n'
                echo(string)
                echo(lyric.encode('utf-8'))
                string = '\n===== end =====\n\n'
                echo(string)
            except Exception, inst:
                string = '***** Caught exception, reason[%s]' % (inst, )
                echo(string)

        out.close()

    def callModuleTestSite():
        output = '___site.test.result.txt'
        out = open(output, 'wb')

        def echo(string):
            out.write(string + '\n')
            out.flush()
            print(string)

        keys = site_dict.keys()
        keys.sort()

        for key in keys:
            try:
                result = get_test_result(key)
                if not result:
                    string = '# module [%s] does not implement test function yet' % (key, )
                else:
                    if result and 'success' in result and result['success']:
                        string = 'OK, module [%s] test succeeded' % (key, )
                    else:
                        string = '! Failed, module [%s], obj dump[%s]' % (key, repr(result), )
                echo(string)
            except Exception, inst:
                string = '***** Caught exception, reason[%s]' % (inst, )
                echo(string)

        out.close()

        
                
    def getLyric():
        index = 'utaten'
        url = get_test_url(index)
        print url
        engine = Lyric(url)
        lyric = engine.get_lyric()
        print lyric
#         print(repr(lyric))

    getLyric()


#     testEverySite()

#     callModuleTestSite()

#     runProfiling()

