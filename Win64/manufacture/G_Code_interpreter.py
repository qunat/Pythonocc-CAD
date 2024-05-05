#coding=utf-8
import re
class G_code_interpreter(object):
    def __init__(self):
        self.patterm_dict= {}
        self.patterm_dict["F"] = r'[F](.*?)'  # 正则取出Z的内容
        self.patterm_dict["S"] = r'[S](.*?)[M]'  # 正则取出Z的内容
        self.patterm_dict["X"]=r'[X](.*?)[A-Z]'  # 正则取出X的内容
        self.patterm_dict["Y"] = r'[Y](.*?)[A-Z]'  # 正则取出Y的内容
        self.patterm_dict["Z"] = r'[Z](.*?)[F]'  # 正则取出Z的内容
        self.patterm_dict["I"] = r'[I](.*?)[A-Z]'  # 正则取出I的内容
        self.patterm_dict["J"] = r'[J](.*?)[A-Z]'  # 正则取出J的内容
        self.patterm_dict["K"] = r'[K](.*?)[F]'  # 正则取出K的内容
        self.patterm_dict["G"] = r'[G](.*?)[A-Z]'  # 正则取出G的内容
        self.Machining_paramater={"wcs":"G54","spindle_speed":90,"status_G":None,"X":["0"],"Y":["0"],"Z":["0"],"I":["0"],"J":["0"],"K":["0"]}
        self.Out_NC_simple=[]
    def Read_nc_code(self,filepath="./NC/o108.NC",mode=1):
        file = open(filepath, "r")
        self.nc_code_list = file.readlines()
        for i in self.nc_code_list:
            i = i.strip()
            self.Get_status_G(i)
            self.Interpreter_G_COode(i)
    def Interpreter_G_COode(self,G_code_str=str()):
        G_code_str=G_code_str.strip()+"F"#增加结束识别符
        out_code=[]
        #print(G_code_str)
        S=  re.findall(self.patterm_dict["S"], G_code_str)
        F = re.findall(self.patterm_dict["F"], G_code_str)
        X = re.findall(self.patterm_dict["X"], G_code_str)
        Y = re.findall(self.patterm_dict["Y"], G_code_str)
        Z = re.findall(self.patterm_dict["Z"], G_code_str)
        I = re.findall(self.patterm_dict["I"], G_code_str)
        J = re.findall(self.patterm_dict["J"], G_code_str)
        K = re.findall(self.patterm_dict["K"], G_code_str)
        if X==[]:
            X=self.Machining_paramater["X"]
        else:
            self.Machining_paramater["X"]=X
        if Y==[]:
            Y=self.Machining_paramater["Y"]
        else:
            self.Machining_paramater["Y"]=Y
        if Z==[]:
            Z=self.Machining_paramater["Z"]
        else:
            self.Machining_paramater["Z"]=Z
        if I==[]:
            I=self.Machining_paramater["I"]
        else:
            self.Machining_paramater["I"]=I
        if J==[]:
            J=self.Machining_paramater["J"]
        else:
            self.Machining_paramater["J"]=J
        if K==[]:
            K=self.Machining_paramater["K"]
        else:
            self.Machining_paramater["K"]=K

        if self.Machining_paramater["status_G"]=="G00":
            #print(self.Machining_paramater["status_G"],X[0],Y[0],Z[0])
            out_code=[self.Machining_paramater["status_G"],X[0],Y[0],Z[0]]
            self.Out_NC_simple.append(out_code)
        elif self.Machining_paramater["status_G"]=="G01":
            #print(self.Machining_paramater["status_G"], X[0], Y[0], Z[0])
            out_code=[self.Machining_paramater["status_G"], X[0], Y[0], Z[0]]
        elif self.Machining_paramater["status_G"]=="G02":
            #print(self.Machining_paramater["status_G"], X[0], [0], Z[0],I[0],J[0],K[0])
            out_code=[self.Machining_paramater["status_G"], X[0], Y[0], Z[0],I[0],J[0],K[0]]
        elif self.Machining_paramater["status_G"]=="G03":
            #print(self.Machining_paramater["status_G"], X[0], Y[0], Z[0],I[0],J[0],K[0])
            out_code=[self.Machining_paramater["status_G"], X[0], Y[0], Z[0],I[0],J[0],K[0]]
        self.Out_NC_simple.append(out_code)
    def Get_status_G(self,G_code_str=str()):
        G_code_str=G_code_str.strip()
        if 'G00' in G_code_str:
            self.Machining_paramater["status_G"]="G00"
            #print("G00")
        elif 'G01' in G_code_str:
            self.Machining_paramater["status_G"] = "G01"
            #print("G01")
        elif 'G02' in G_code_str:
            self.Machining_paramater["status_G"] = "G02"
            #print("G02")
        elif 'G03' in G_code_str:
            self.Machining_paramater["status_G"] = "G03"
            #print("G03")
        else:
            self.Machining_paramater["status_G"] = self.Machining_paramater["status_G"]



if __name__=="__main__":
    pass
    new_class=G_code_interpreter()
    new_class.Read_nc_code()
    for i in new_class.Out_NC_simple:
        print(i)