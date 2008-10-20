from DataField import DataField
import types

class EnumField(DataField):
    def __init__(self, codes, value=None):
        if type(codes) is types.DictType:
            self._encode = codes
            self._decode = {}
            for name in self._encode.keys():
                self._decode[self._encode[name]] = name
        else:
            self._encode = {}
            self._decode = {}
            for i in range(len(codes)):
                self._encode[codes[i]] = i
                self._decode[i] = codes[i]
        DataField.__init__(self, self.encode(value))
        
    def encode(self, value):
        if self._encode.has_key(value):
            return self._encode[value]
        return None
        
    def decode(self, value):
        if self._decode.has_key(value):
            return self._decode[value]
        return None
        
    def _setInner(self, value):
        self._value = self.encode(value)
        
    def get(self):
        return self.decode(DataField.get(self))
    
    def equals(self, value):
        return DataField.equals(self, self.encode(value))