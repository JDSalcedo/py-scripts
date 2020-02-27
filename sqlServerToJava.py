import re

import tkinter as tk
from tkinter import *
from tkinter import scrolledtext

DATA_TYPE = {
    'int': 'Integer',
    'varchar': 'String',
    'datetime': 'Date',
    'bit': 'Boolean'
}
DATA_TYPE_LIST = ['int', 'varchar', 'datetime', 'bit']

pattern_FIELD_DATA_TYPE = r'(\w+) (\w+)'
pattern_NULL = r'NULL'
pattern_NOT_NULL = r'NOT NULL'
pattern_IDENTITY = r'IDENTITY'

class Application(Frame):

    def clean(self):
        self.inputScrolledtxt.delete('1.0', tk.END)
        self.outputScrolledtxt.delete('1.0', tk.END)

    def getSingular(self, var):
        if var[-1] == 's':
            var = var[:-1]
        return var

    def getFirstLower(self, var):
        if var[0] == var[0].upper():
            var = var[0].lower() + var[1:]
        return var

    def processLine(self, line):
        pattern_CREATE_TABLE = r'CREATE TABLE SIGH.dbo.(\w+)'
        c = re.search(pattern_CREATE_TABLE, line)
        if c and c.group is not None:
            msg = "public class %s implements Serializable {\n" % self.getSingular(c.group(1))
            self.outputScrolledtxt.insert('end', """@Data\n@Entity\n""")
            self.outputScrolledtxt.insert('end', """@Table(name = "%s")\n""" % c.group(1))
            self.outputScrolledtxt.insert('end', msg)

        i = re.search(pattern_FIELD_DATA_TYPE, line)
        if i and i.group is not None:
            msg = ""
            if i.group(2) is not None:
                if i.group(2) in DATA_TYPE_LIST:
                    msg = "\tprivate %s %s;\n" % (DATA_TYPE[i.group(2)], self.getFirstLower(i.group(1)))
                    if i.group(2) == 'int':
                        is_identity = re.search(pattern_IDENTITY, line)
                        if is_identity and is_identity is not None:
                            self.outputScrolledtxt.insert('end', "\t@GeneratedValue(strategy = GenerationType.IDENTITY)\n")

                    is_not_null = re.search(pattern_NOT_NULL, line)
                    if is_not_null and is_not_null.group is not None:
                        str_column = """\t@Column(name = "%s", nullable = false)\n""" % i.group(1)
                    else:
                        is_null = re.search(pattern_NULL, line)
                        if is_null and is_null.group is not None:
                            str_column = """\t@Column(name="%s")\n""" % i.group(1)
                    self.outputScrolledtxt.insert('end', str_column)
                    if len(msg):
                        self.outputScrolledtxt.insert('end', msg)


    def clicked(self):
        res = self.inputScrolledtxt.get('1.0', tk.END)
        self.outputScrolledtxt.delete('1.0', tk.END)
        self.outputScrolledtxt.insert('1.0', """import java.io.Serializable;\nimport java.util.Date;\n\nimport javax.persistence.Column;\nimport javax.persistence.Entity;\nimport javax.persistence.GeneratedValue;\nimport javax.persistence.GenerationType;\nimport javax.persistence.Id;\nimport javax.persistence.JoinColumn;\nimport javax.persistence.ManyToOne;\nimport javax.persistence.Table;\nimport javax.persistence.Temporal;\nimport javax.persistence.TemporalType;\n\nimport lombok.Data;\n\n\n""")
        for line in res.splitlines():
            self.processLine(line)
        self.outputScrolledtxt.insert('end', "}")

    def createWidgets(self):
        self.inputScrolledtxt = scrolledtext.ScrolledText(self.master, width=60, height=20)
        self.inputScrolledtxt.grid(column=0, row=0)

        self.outputScrolledtxt = scrolledtext.ScrolledText(self.master, width=60, height=20)
        self.outputScrolledtxt.grid(column=1, row=0)
        
        self.btnLimpiar = Button(self.master, text="Limpiar", command=self.clean)
        self.btnLimpiar.grid(column=0, row=1)
        self.btn = Button(self.master, text="Generar Java Class", command=self.clicked)
        self.btn.grid(column=1, row=1)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("SQLServer To Java(Juan Salcedo Salazar)")
        self.master.maxsize(1000, 400)
        self.master.geometry('1000x400')
        self.createWidgets()

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()