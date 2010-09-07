from rdflib.serializer import Serializer
from rdflib.term import Literal
import warnings

class TupleSerializer(Serializer):
    """
    Serialize RDF graphs to NTuples format (NTriples and NQuads), taking
    care to escape literals as per http://www.w3.org/TR/rdf-testcases/#ntrip_strings.
    """
    
    def serialize(self, stream, base=None, encoding=None, **args):
        if base is not None:
            warnings.warn("TupleSerializer does not support base.")
        if encoding is not None:
            warnings.warn("TupleSerializer does not use custom encoding.")
        encoding = self.encoding
        for tuple in self.tuples:
            stream.write(_nt_row(tuple).encode(encoding, "replace"))
        stream.write("\n")    

class NTSerializer(TupleSerializer):
    
    def __init__(self, store):
        Serializer.__init__(self, store)
        self.tuples = self.store.triples((None, None, None))
        
class NQSerializer(TupleSerializer):
    """
    Serializes RDF graphs to NQuads format, like NTriples, but adding the 
    graph context name as a 4th tuple.
    """

    def __init__(self, store):
        Serializer.__init__(self, store)
        self.tuples = self.store.quads((None, None, None))

def _nt_row(tuple, context=None):
    c = ''
    if len(tuple) > 3:
        c = '%s ' % tuple[3].identifier.n3()
    if (isinstance(tuple[2], Literal)):
        return u"%s %s %s %s.\n" % (
            tuple[0].n3(),
            tuple[1].n3(),
            _n3(tuple[2]), c)
    else:
        return u"%s %s %s %s.\n" % (
            tuple[0].n3(),
            tuple[1].n3(),
            tuple[2].n3(), c)
    
def _n3(l):
    escaped_ascii = ''.join(_escape(c) for c in l)
    if l.datatype:
        return '"%s"^^<%s>' % (escaped_ascii, l.datatype)
    elif l.language:
        return '"%s"@%s' % (escaped_ascii, l.language)
    else:
        return '"%s"' % escaped_ascii
    
def _escape(c):
    """
    Escape the (potentially unicode) character c according to the
    table at http://www.w3.org/TR/rdf-testcases/#ntrip_strings,
    producing an ASCII character or sequence of ASCII characters.
    """
    u = ord(c)
    if u <= 0x8:        return '\\u%04X' % u
    elif u == 0x9:      return '\\t'
    elif u == 0xA:      return '\\n'
    elif u <= 0xC:      return '\\u%04X' % u
    elif u == 0xD:      return '\\r'
    elif u <= 0x1F:     return '\\u%04X' % u
    elif u <= 0x21:     return chr(u)
    elif u == 0x22:     return '\\"'
    elif u <= 0x5B:     return chr(u)
    elif u == 0x5C:     return '\\\\'
    elif u <= 0x7E:     return chr(u)
    elif u <= 0xFFFF:   return '\\u%04X' % u
    else:               return '\\U%08X' % u
