"""
Generic reported class, may be dumped to memory, to .txt or to Visum log
"""


import time
import os


# report semantics
bigspace = "\n" * 2
space = "\n" * 1
doubleline = "=" * 100 + "\n"
spaces = " "*10
spacer = "-" * 100 + "\n"
bullet = spaces + "* "
ender = "\n" + spacer


def makeheader(n, *args):
    ret = space + doubleline + spaces + n + "\n"
    for arg in args:
        ret += spaces + str(arg) + "\n"
    ret += spacer
    return ret


def makesubheader(n, *args):
    ret = "\n" + spacer + spaces + n + "\n"
    for arg in args:
        ret += spaces + str(arg) + "\n"
    ret += spacer
    return ret


class Report:

    _msg = ""
    curr_section = None
    section_start_time = None

    def __init__(self, _f=None, _txt=None):
        self.start_time = time.time()
        self.add(doubleline)
        if _f is not None:
            self.add(spaces + _f.__name__ + " report " + self.timestamp())
        else:
            self.add(spaces + "DataScience report " + time.strftime('%b %d, %Y'))
        self.add(spacer)
        if _txt is not None:
            self.add(_txt)
            self.name = _txt
        if _f is not None:
            self.adddesc(_f.__doc__)
            self.name = _f.__name__


    def timestamp(self):
        return time.strftime("%d %b %H:%m:%S")

    def adddesc(self, t):
        self.add(doubleline, "Description:", t)

    def adddf(self, _df, n):
        self.addline(
            "Using ", n,
            " DataFrames of ",
            _df.shape[0], " rows and ", _df.shape[1], " columns.")

    def addhd5(self, _dfs):
        self.addline(
            "Using ",
            str(len(_dfs.keys())),
            " DataFrame from: ",
            _dfs.filename.split("/")[-1],
            " file of ",
            int(os.path.getsize(_dfs.filename) / 1024 / 1024.0),
            "MB.")

    def addsection(self, section_name):
        if self.curr_section is not None:
            self.endsection()
        self.add(space, doubleline, section_name, spacer)
        self.curr_section = section_name
        self.section_start_time = time.time()

    def endsection(self):
        self.addline(spacer, self.timestamp(),
                     " ",
                     self.curr_section,
                     " finished in ",
                     str(int(time.time() - self.section_start_time)), "s\n",
                     doubleline)

    def addend(self):
        self.addline(spacer, self.timestamp(), " ",
                     self.name, " finished in ", str(int(time.time() - self.start_time)), "s\n", doubleline)

    def addline(self, *args):
        for a in args:
            self._msg += str(a)
        self._msg += "\n"

    def add(self, *args):
        for a in args:
            self._msg += str(a)+"\n"

    def dump(self, f):
        self.addend()
        text_file = open(f, "w")
        text_file.write(self._msg)
        text_file.close()

    def show(self):
        print(self._msg)


if __name__ == "__main__":
    r = Report(None, "REPORT") # Header
    r.addsection("SECTION 1") # section header
    r.addline("some", "\ttext", "one line")  # text in single line
    time.sleep(2)
    r.addsection("SECTION 2") # another section
    time.sleep(1)
    r.add("some", "text", "new lines") # text in multiline
    r.endsection()
    r.addend() # footer
    r.show()  # plot
    r.dump("rep.txt") # dump




