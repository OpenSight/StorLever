
import re,os
from tempfile import mkstemp


class Error(Exception):
    """Base class for ConfigParser exceptions."""

    def __init__(self, msg=''):
        self.message = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self.message

    __str__ = __repr__

class NoSectionError(Error):
    """Raised when no section matches a requested option."""

    def __init__(self, section):
        Error.__init__(self, 'No section: %r' % (section,))
        self.section = section

class DuplicateSectionError(Error):
    """Raised when a section is created twice."""

    def __init__(self, section):        
        Error.__init__(self, "Section %r already exists" % section)
        self.section = section

class NoOptionError(Error):
    """A requested option was not found."""

    def __init__(self, option, section):
        Error.__init__(self, "No option %r in section: %r" %
                       (option, section))
        self.option = option
        self.section = section

class EvaluationError(Error):
    """Base class for interpolation-related exceptions."""

    def __init__(self, option, section, msg):
        Error.__init__(self, msg)
        self.option = option
        self.section = section

class EvaluationMissingOptionError(EvaluationError):
    """A string substitution required a setting which was not available."""

    def __init__(self, option, section, rawval, reference):
        msg = ("Bad value substitution:\n"
               "\tsection: [%s]\n"
               "\toption : %s\n"
               "\tkey    : %s\n"
               "\trawval : %s\n"
               % (section, option, reference, rawval))
        EvaluationError.__init__(self, option, section, msg)
        self.reference = reference

class ParsingError(Error):
    """Raised when a configuration file does not follow legal syntax."""

    def __init__(self, filename):
        Error.__init__(self, 'File contains parsing errors: %s' % filename)
        self.filename = filename
        self.errors = []

    def append(self, lineno, line):
        self.errors.append((lineno, line))
        self.message += '\n\t[line %2d]: %s' % (lineno, line)

class MissingSectionHeaderError(ParsingError):
    """Raised when a key-value pair is found before any section header."""

    def __init__(self, filename, lineno, line):
        Error.__init__(
            self,
            'File contains no section headers.\nfile: %s, line: %d\n%r' %
            (filename, lineno, line))
        self.filename = filename
        self.lineno = lineno
        self.line = line


class proxy(object):
    """When you aggregate a 'proxy' to a dikshanary then the
    proxy s attribute are the dict s item. Can be convenient"""

    # [ off the record, this is still a bit voodoo I must say. Should have a look
    # at the optparse module where the idea comes from, in the first place]

    def __init__(self, _dict):
        object.__setattr__(self, '__dict', _dict)

    # The three following functions are the ones that are called when 
    # you get, set, or delete an attribute of the proxy
    def __getattr__(self, item):
        return getattr(self, '__dict')[ item ]
    
    def __setattr__(self, item, value):
        getattr(self, '__dict')[ item ] = value
        
    def __delattr__(self, item):
        del getattr(self, '__dict')[ item ]


class properties(dict):


    def __init__(self, _fileordict=None, _order=[], **kwargs):
        """The constructor accepts a filename or a list of filenames. It
        can also be a dictionnary or another properties instance. Lastly,
        it can accept the entries of the form key1='value1', key2='value2'.
        """

   
        self.dustbin, self.template = [], ""
        self.order = _order
        self.proxy=proxy(self)

        if isinstance( _fileordict, str ) or isinstance( _fileordict, list):
            self.template=_fileordict
            self.read( _fileordict )

        elif hasattr( _fileordict, '__setitem__' ):
            self.update( _fileordict )
            if  hasattr( _fileordict, 'dustbin' ):
                self.dustbin = _fileordict.dustbin[:]
            if  hasattr( _fileordict, 'order' ):
                self.order = _fileordict.order[:]
                
        if kwargs:
            for k,v in kwargs.items():
                self[k] = str( v )

    def copy(self):
        return properties(self)

    line=re.compile("""
(^
			\s*
        (?P<option>	[^\#;]+?)
        	 	(\s* (=|:) \s*)
        (?P<value>	.+?)?
        		(\s+((\#|;).*)?)?
$)|(^
    			(\s*(\#|;)+\s*
        (?P<cmted>	.*))
$)|(^
			\s+
        (?P<cont>	[^\#;]*?)
    			(\s+(\#|;).*)?
$)""", re.VERBOSE)

    variable=re.compile(r'(?<!\\)\$(?P<name>\w+)')

    def interpolate(self, value):
        """Recursively evaluates the variables as keys of the
        properties instance, and replace them with the corresponding
        value. The variables are defined by a dollar sign followed by
        alphanumeric characters. If the $ sign is preceded by a \ it
        is not a variable. If the variable is not a key of the
        instance, a key error is raised."""
        if value:
            if self.variable.search(value):
                try:
                    return self.variable.sub( lambda m:self.interpolate( self[m.group('name')]) , value)
                except RuntimeError:
                    print  "Error: Loop in assignments"
                    return value.replace("\$","$")
            else:
                return value.replace("\$","$")
        else:
            return ''

    def get(self, item, default=""):
        """If there is no value in the dict for item, get returns the
        'default'. A evaluation of a missing variable raise a KeyError
        exception. Variables in values are evaluated. Item and default
        can both be list. In this case, get behaves as if it had been called
        on each elements of items and returns the lists of values.""" 
        if isinstance(item,list):
            was_list = True
        else: item, was_list = [ item ], False

        if not isinstance(default,list):
            default = [ default ]

        if len(item)==len(default):
            ret = map( lambda i: self.interpolate(dict.get(self, i[0], i[1])), zip (item, default))
        else:
            ret = [ self.interpolate(dict.get(self, i)) for i in item ]


        if was_list:
            return ret
        else:
            return ret[0]

            
    def __setitem__(self, item, value):
        """Sets a value for the item. If the item was in the dustbin,
        it is removed from the dustbin"""
        if item in self.dustbin:
            self.dustbin.remove(item)
        dict.__setitem__( self, item, str(value))
    

    def __delitem__(self, item):
        """Suppress the item and value from the instance. The deleted
        option is flagged to be skipped when writing or updated a file
        so that the option is effectively deleted"""
        self.dustbin.append(item)
        if item in self:
            dict.__delitem__( self, item)

    def delete(self, item):
        if isinstance(item, list):
            map(self.__delitem__, item)
        else:
            self.__delitem__(item)

        return self

    def items(self, default={}, **kwargs):
        d=default.copy()
        d.update(kwargs)
        d.update(dict.items(self))
        return d

    def linerepr ( self, k ) :
        if k in self: return k + '=' + self[k].replace('\n','\n\t') + '\n'
        else : return ""

    def __repr__(self):
        """The read and write methods will update the filename
        attribute. This file, if exist, is taken as a template for the
        layout and comments. Deleted options are not
        represented. Then, keys in the instance but not found in the
        file (or if the filename attribute is empty) are added, sorted
        by the order attribute. Finally, left options are added
        alphabetically."""

        def replace_value_in_line (mo, value):
            """Handy function that replace a named group by a string
            in the string that the matched object was generated from"""
            return mo.string[ :mo.start('value') ] + value.replace( '\n', '\n\t' ) + mo.string[ mo.end('value'): ]
            
        # Because we pop the written lines, we need to pop on a _copy_
        a_copy = properties(self)

        result=""
        try: fp = file( self.template )
        except: fp = []


        for line in fp:

            mo = a_copy.line.match(line)

            if not mo:
                result += line
                continue

            option, cont, cmted = mo.group('option', 'cont', 'cmted')

            if option and option in a_copy:
                result += replace_value_in_line (mo, a_copy[option] )
                del a_copy[option]
                            
            elif cmted:
                mo = a_copy.line.match(cmted)
                if not mo:
                    result += line
                    continue
                
                option = mo.group( 'option' )
                if option and option in a_copy:
                    result += replace_value_in_line ( mo, a_copy[option] )
                    del a_copy[option]
                else:
                    result += line
                                                          
            # skip the line whose option is in the dustbin
            elif option and option in a_copy.dustbin: pass

            # skip the continuation lines, already handled by the 'option' block
            elif cont: pass
            
            else: result += line

        for k in a_copy.order[:] :
            result += a_copy.linerepr( k )
            del a_copy[k]

        result += ''.join( [ a_copy.linerepr( k ) for k in sorted(a_copy.keys()) ] )

        return result

    def read(self,filenames=[]):
        """read and parse the list of named configuration files, given
        by name.  A single filename is also allowed.  Non-existing
        files are ignored.  Return list of successfully read
        files. The filename attribute is update with the last element
        of the list, so that the write methods can be called with no
        argument"""

        if isinstance(filenames, basestring):
            self._read( file(filenames), filenames)
            self.template=filenames
            
        for filename in filenames:
            try:
                fp = open(filename)
            except IOError:
                continue
            self._read(fp, filename)
            fp.close()

            self.template=filename
            
        return self.proxy


    def _read( self, fp, fn):
        """Parses each line of an open file, and detects options,
        values, and continuation lines."""

        for l in fp:
            m = self.line.match( l )
            if m:
                option, value, cont = m.group('option', 'value', 'cont')

                if option: 	cur_opt, self[option] = option, value
                elif cont: 	self[cur_opt] += '\n' + cont.lstrip()
                

    def write(self, destination=None, order=None):
        """write can be called with an open file, with a filename, or
        without argument. The filename is the destination file, if
        missing, the filename attribute is the destination file. If
        both are empty, the representation of the instance is written
        on stdout"""

        if isinstance( destination, basestring):
            self.template = destination
            fd, tmp = mkstemp()
            os.close(fd)
            f = file(tmp,'w')

        elif isinstance(destination,file):
            f = destination

        elif self.template:
            destination = self.template
            fd, tmp = mkstemp()
            os.close(fd)
            f = file(tmp,'w')
        
        if not self.template:
            print repr(self)
        else:
            f.write(repr(self))

        if isinstance(destination, basestring):
            f.close()
            try:
                os.rename(tmp,destination)
            except:
                open(destination,'w').write(open(tmp).read())
                os.unlink(tmp)

    apply_to = write


class ini(dict):

    # Shortcut to the dict set and del methods (Hosts do no override get)
    def dget(self, item): return 	dict.__getitem__(self, item )
    def dset(self, item, value): 	dict.__setitem__(self, item, value )
    def ddel(self, item): 	 	dict.__delitem__(self, item )            

    def __init__(self, _fileordict=None, **kwargs):

        self.dustbin, self.defaults, self.template = [], {}, ""
        self.proxy=proxy(self)

        if type(_fileordict)==str:
            self.template=_fileordict
            self.read(_fileordict)

        elif hasattr(_fileordict,'__setitem__'):
            for (k, v) in _fileordict.items():
                if hasattr(v, '__setitem__'):
                    self[k]=v.copy()
            else:
                self.defaults.update(_fileordict)
            if hasattr(_fileordict, 'dustbin'):
                self.dustbin = _fileordict.dustbin[:]
                
        if kwargs:
            self.defaults.update(kwargs)

    line=re.compile('''
(^
			\[
        (?P<section>	.+) \]
        		(\s+((\#|;).*)?)?
$)|(^
    			\s*
        (?P<option>	[^\#;]+?)
        		(\s* (=|:) \s*)
        (?P<value>	.+?)?
        		(\s+((\#|;).*)?)?
$)|(^
		       	(\s*(\#|;)+\s*
        (?P<cmted>	.*))
$)|(^
        		\s+
        (?P<cont>	[^\#;]*?)
        		(\s+(\#|;).*)?
$)''', re.VERBOSE)

    
    def __setitem__(self, item, value):
        item = str( item )
        if item in self.dustbin:
            self.dustbin.remove(item)
        dict.__setitem__(self,item, value)

    def __delitem__(self, item):
        item = str( item )
        self.dustbin.append(item)

        if item in self:
            dict.__delitem__(self, item)

    def get(self, section, option, default=None):
        try:
            return self[section][option]
        except KeyError:
            return self.defaults[option]

    def simple_line ( self, section, key ) :
        if key in self.section:
            return key + '=' + a_copy[section][key].replace('\n','\n\t') + '\n'
        else : return ""

    def __repr__(self):
    
        def replace_value_in_line (mo, value):
            return mo.string[ :mo.start('value') ] + value.replace( '\n', '\n\t' ) + mo.string[ mo.end('value'): ]
        
        # Because we pop the written lines, we need to pop on a _copy_
        a_copy, result, cur_sect = ini(self), '', ''

        try: fp = file( self.template )
        except: fp = []
        
        for line in fp :

            mo = a_copy.line.match(line)
            
            if not mo:
                result += line
                continue
            
            # if section then dump the remaining options and supppres the a_copy[cur_sect]
            # then only then can you write the option
            
            section, option, cont, cmted = mo.group('section', 'option', 'cont', 'cmted')
            
            if section:

                if cur_sect and cur_sect in a_copy:
                    result += repr ( a_copy[cur_sect] )
                    del a_copy[cur_sect]
                
                if section not in self.dustbin:
                    result += line

                cur_sect = section

            # skip the line whose option is in the dustbin
            elif option and option in a_copy[cur_sect].dustbin:
                pass    
            
            elif option and option in a_copy[cur_sect]:
                result += replace_value_in_line (mo, a_copy[cur_sect][option])
                del a_copy[cur_sect][option]
                                
            elif cmted:
                mo = a_copy.line.match( cmted )
                if not mo:
                    result += line
                    continue
                option = mo.group( 'option' )
                
                if option and option in a_copy[cur_sect]:
                    result += replace_value_in_line (mo, a_copy[cur_sect][option])
                    del a_copy[cur_sect][option]
                            
                else: result += line

            # skip the continuation lines, already handled by the 'option' block
            elif cont: pass
            
            else: result += line

        if cur_sect and cur_sect in a_copy:
            result += repr ( a_copy[cur_sect] )
            del a_copy[cur_sect]

        for section in sorted(a_copy.keys()):
            result += '[' + section + ']\n' + repr ( a_copy[section] ) + '\n'

        return result
        
    def read(self,filenames):

        if isinstance(filenames, basestring):
            filenames = [filenames]
        read_ok = []
        for filename in filenames:
            try:
                fp = open(filename)
            except IOError:
                continue
            self._read(fp, filename)
            fp.close()
            read_ok.append(filename)
            self.template=filename
        return read_ok


    def _read( self, fp, fn ):
        '''Can read ifcfg files, java properties files as well as ini
        files with section, and updates self accordingly'''

        for line in fp:
            m = self.line.match( line )
            if m:
                section, option, value, cont = m.group('section', 'option', 'value', 'cont')
                
                if section:
                    cur_sect = self[section] = properties()
                    
                elif option:
                    cur_sect[option], cur_opt,  = value, option
                    
                elif cont:
                    cur_sect[cur_opt] += '\n' + cont.lstrip()


    def write(self, destination=None, order=None):

        if isinstance( destination, basestring):
            self.template = destination
            fd, tmp = mkstemp()
            os.close(fd)
            f = file(tmp,'w')

        elif isinstance(destination,file):
            f = destination

        elif self.template:
            destination = self.template
            fd, tmp = mkstemp()
            os.close(fd)
            f = file(tmp,'w')
        
        if not self.template:
            repr(self)
        else:
            f.write(repr(self))

        if isinstance(destination, basestring):
            f.close()
            try:
                os.rename(tmp,destination)
            except:
                open(destination,'w').write(open(tmp,'r').read())
                os.unlink(tmp)


if __name__=='__main__':
    # je veux un second dict qui contienne les defauts
    i=properties( {'abc':'changed','titi':'toutou'}, abd="Trans go#a")
    import sys
    print i
    i.write(sys.stdout)
    c=i.read()
    print c.titi
    print c.abc
    c.tata=123
    print c.tata
    del c.tata
    del c.titi
    print i
