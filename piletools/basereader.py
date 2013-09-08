#!/usr/bin/env python

class Base(object):
    """
    """
    forward = ('A', 'C', 'G', 'T', '.', '>')
    reverse = ('a', 'c', 'g', 't', ',', '<')
    reference = ('.', ',')
    def __init__(self, reference, nucleotide, quality, is_start=False,
        is_end=False):
        """
        """
        self.nucleotide = nucleotide.upper()
        if nucleotide in self.reference:
            self.nucleotide = reference
        self.quality = quality
        self.is_start = is_start
        self.is_end = is_end
        self.is_forward = nucleotide in self.forward
    #__init__

    def __str__(self):
        return ("  nucleotide: {}\n  quality: {}\n  forward: {}\n  start: {}\n"
            "  end: {}\n".format(self.nucleotide, self.quality,
            self.is_forward, self.is_start, self.is_end))
#Base

class Variant(object):
    def __init__(self, content, is_insertion=False, is_deletion=False):
        """
        """
        self.content = content
        self.is_insertion = is_insertion
        self.is_deletion = is_deletion
    #__init__

    def __str__(self):
        return "insertion: {}\ndeletion: {}\nnucleotides:\n{}".format(
            self.is_insertion, self.is_deletion,
            '\n'.join(map(str, self.content)))
#Variant

class BaseReader(object):
    start = '^'
    end = '$'

    indel = ('+', '-')
    insertion = '+'

    def __init__(self, reference, bases, qualities):
        """
        """
        self.reference = reference
        self.bases = bases
        self.qualities = qualities
        self.base_offset = -1
        self.qual_offset = -1
        self.parsing_indel = False
    #__init__

    def __iter__(self):
        return self

    def get_indel(self):
        """
        """
        insertion = self.bases[self.base_offset] == self.insertion
        self.base_offset += 1

        len_str = ""
        while self.bases[self.base_offset].isdigit():
            len_str += self.bases[self.base_offset]
            self.base_offset += 1
        #while
        length = int(len_str)

        bases = []
        for i in range(length):
            bases.append(Base(self.reference,
                self.bases[self.base_offset + i],
                self.qualities[self.qual_offset + i]))

        self.base_offset += length - 1
        self.qual_offset += length - 1

        return insertion, bases
    #get_indel

    def next(self):
        self.base_offset += 1
        self.qual_offset += 1

        if self.base_offset >= len(self.bases):
            raise StopIteration

        if self.bases[self.base_offset] in self.indel:
            is_insertion, bases = self.get_indel()

            return Variant(bases, is_insertion=is_insertion,
                is_deletion=not is_insertion)
        #if
        return Variant([Base(self.reference, self.bases[self.base_offset], 
            self.qualities[self.qual_offset])])
    #next
#BaseReader

def main():
    x = ",,,,..,..,,.+1C..,.+1A,,.,..,,."
    y = "IIIIIIIIIIIIIIIIIIIIIIIIIII"
    #x = "+2ACGG"
    #y = "IJNN"
    #x = "Ccc.CcC"
    #y = "IIIIIII"
    
    b = BaseReader("T", x, y)
    for i in b:
        print i, '\n'
#main

if __name__ == "__main__":
    main()
