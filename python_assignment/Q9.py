class Names:
    def get_string(self,name):
        self.name = name
    
    def print_string(self):
        print(self.name.upper())

x = Names()    
x.get_string("michael")
x.print_string()