##############################
###
###     Program structure:
###
##############################
#
# INITIAL SETUP BEGIN
# - Setup excel file access
# - Setup GUI
#   |- Create canvas object
#   |- Create four slider objects  
# - Setup scale coefficients for diagrams  
#   |- Space vetor scales
#   |- Hexagon diagram scale
#   |- Operational quadrant scales
# - Setup center point coordinates for diagrams  
#   |- Space vetor diagram center
#   |- Hexagon diagram center
#   |- Operational quadrant center
# INITIAL SETUP END
#
#
# MAINLOOP DEFINITION BEGIN
#   |- Write title
# - Time input  
#   |- Limit slider sum to simulation sample count
#   |- Final selected time point in ms
#   |- Write selected timepoint on screen
# - Read vectors from row contents of spreadsheet
# - DrawSspace vector diagram
#   |- dq axis dashed
#   |- dq axis labels
#   |- Space Vectors
#   |- Space Vector Labels
# - Draw Rotating hexagon diagram
#   |- Active vector
#   |- Rotating frame dashed
#   |- Labels at the tips of three base "spokes"
# - Draw Operational quadrant diagram
#   |- Quadrant labels
#   |- Quadrant frame
#   |- Axis and axis labels
#   |- Targe
#   |- Actual "Vector" and projections
# - Finalize mainloop
#   |- Print something to the console
#   |- Refresh GUI (update, wait 1ms and clear)
# MAINLOOP DEFINITION END
#
#
# CLASS AND FUNCTION DEFINITIONS BEGIN
# - ReadRow - Link variables to spreadsheet columns
# - VectorBuild - Design Space vector diagram 
#   |- Draw dq axis 
#   |- Place Voltage and Current space vectors
# - Hexagon - Design Rotating hexagon diagram
#   |- Inverter output phase states
#   |- Rotation adjustment
#   |- Calculation of rotating corners
#   |- Choose which one of the "spokes" carries the resulting voltage vector
#   |- Build resulting voltage vector
#   |- Build Radial hexagon lines - dashed
#   |- Label positions
#   |- Label texts and colors
#   |- Build Hexagon edges - dashed
# - TorqueSpeed - Design Operational quadrant diagram
#   |- Build quadrant frame
#   |- Buld load torque and reference rotor speed as levels
#   |- Buld actual "vector" pointing to the operational state
#   |- Buld the vector's projections towards axis
# - Function definitions
#   |- OriScale() - Place a vector
#   |- DrawCrosshair() - Draw reference target
# CLASS AND FUNCTION DEFINITIONS END
#
#
# - Run Mainloop






##############################################
###
###     INITIAL SETUP BEGIN
###
##############################################

import math
pi = math.pi

#############################
### Setup excel file access
#############################

import pandas as pd
file_name = 'SimulinkOutput.xlsx' # Spreadsheet filename
df = pd.read_excel(file_name, sheet_name=None, header=None)
sheet = df["dati5"] # Sheet selection within the spreadsheet
sim_len = len(sheet)
sim_time = 2 # Matlab Simulink simulation time in seconds

###################################
### Setup GUI (Canvas and Sliders)
###################################

canvas_width = 1300 
canvas_height = 500

from tkinter import Tk, Canvas, Scale, HORIZONTAL, LAST
import time
root=Tk()

### Create canvas object
canvas = Canvas(root,  width = canvas_width, height = canvas_height)
canvas.pack()

### Create four slider objects
slide_res = sim_len # Set the full resolution to be equal to simulation 
slide_len = canvas_width # Set slider to fill the width of the canvas

zoom1 = 1
zoom2 = 10
zoom3 = 500
zoom4 = 2000

slide_sc1 = Scale(root, from_ = 0, to = slide_res/zoom1, 
                  length = slide_len, orient=HORIZONTAL,
                  font="Times 12", label="zoom x{}".format(zoom1))

slide_sc2 = Scale(root, from_ = 0, to = (slide_res/zoom2), 
                  length = slide_len, orient=HORIZONTAL,
                  font="Times 12", label="zoom x{}".format(zoom2))

slide_sc3 = Scale(root, from_ = 0, to = (slide_res/zoom3), 
                  length = slide_len, orient=HORIZONTAL,
                  font="Times 12", label="zoom x{}".format(zoom3))

slide_sc4 = Scale(root, from_ = 0, to = (slide_res/zoom4), 
                  length = slide_len, orient=HORIZONTAL,
                  font="Times 12", label="zoom x{}".format(zoom4))


slide_sc1.pack()
slide_sc2.pack()
slide_sc3.pack()
slide_sc4.pack()

# Get max speed for speed scale [Not yet implemented further]
# max_speed = sheet[13].max()


#########################################
### Setup scale coefficients for diagrams
#########################################
       
### Space vetor diagram scales
sc_u = 0.5  # voltage scale
sc_i = 100  # current scale

### Hexagon diagram scale
sc_h = 150  # hexagon scale

### Operational quadrant scales
sc_C = 150
C_V = 1*sc_C
C_H = 1*sc_C

sc_w = 0.9 * C_V  # speed scale
sc_T = 0.75 * C_H  # Torque scale

########################################################
### Setup center point coordinates for diagrams
########################################################

drop = 270 # Vertical distance from top
dist = 400 # Horizontal distance between diagram centers

### Space vector diagram center
ori_A = (0, 0, canvas_width/2 - dist, drop)  

### Hexagon diagram center center
ori_B = (0, 0, canvas_width/2, drop)

### Operational quadrant diagram center
ori_C = (0, 0, canvas_width/2 + dist, drop)  

##############################################
###
###     INITIAL SETUP END
###
##############################################



##############################################
###
###     MAINLOOP DEFINITION BEGIN
###
##############################################

def main():
    global i

    while 1:
        ### TITLE
        canvas.create_text(canvas_width/2, 50,font="Times 16",text="Induction machine FOC with SVPWM.")
       
        ######################
        ### TIME INPUT
        ######################
        
        ### Limit slider sum to simulation sample count
        time_unsat = slide_sc1.get() + slide_sc2.get() + slide_sc3.get()  + slide_sc4.get()
        if time_unsat >= slide_res: time_sat = slide_res
        elif time_unsat <= 0: time_sat = 0
        else: time_sat = time_unsat
        tp =  int( round( (sim_len-1) * time_sat / slide_res ) )
        
        ### Final selected time point in ms
        time_abs = tp / sim_len * sim_time * 1000
        
        ### Print time point
        canvas.create_text(100, canvas_height-15, font="Times 14 bold", text = "Time: {:.3f} ms".format(time_abs))
        
        #################################################
        ### Read vectors from row contents of spreadsheet
        #################################################
        val = ReadRow(tp)
        vec = VectorBuild(val, ori_A)
        hxg = Hexagon(val, ori_B)
        trw = TorqueSpeed(val, ori_C)
        
        #######################################
        ### DRAW Space vector diagram
        #######################################
        
        ### dq axis dashed
        canvas.create_line(vec.daxis, arrow = LAST, dash=(4, 2), fill="black")
        canvas.create_line(vec.qaxis, arrow = LAST, dash=(4, 2), fill="black")
        
        ### dq axis labels
        canvas.create_text(vec.daxis[2] +10, vec.daxis[3],font="Times 12",text="d")
        canvas.create_text(vec.qaxis[2] +10, vec.qaxis[3],font="Times 12",text="q")
        
        ### Space Vectors 
        canvas.create_line(vec.u_s, arrow = LAST, fill="blue")        
        canvas.create_line(vec.i_s, arrow = LAST, fill="red")       
        DrawCrosshair(vec.i_s_[2], vec.i_s_[3], ori_A[3], 10, 30, "red")
        canvas.create_line(vec.i_mr, arrow = LAST, fill="red", width = 1)
        ### Space Vector Labels
        canvas.create_text(vec.u_s[2] -25, vec.u_s[3], fill="blue", font="Times 12",text="u_s*")
        canvas.create_text(vec.i_s[2] +25, vec.i_s[3] +15, fill="red", font="Times 12",text="i_s")
        canvas.create_text(vec.i_s_[2] +25, vec.i_s_[3] -7, fill="red", font="Times 12",text="i_s*")
        canvas.create_text(vec.i_mr[2] +15, vec.i_mr[3] +7, fill="red", font="Times 12",text="i_mr")
        
        ##########################################
        ### DRAW Rotating hexagon diagram
        ##########################################
        
        ### Draw active vector
        canvas.create_line(hxg.act, arrow = LAST, fill="blue", width = 4)
        
        ### Draw rotating frame dashed
        canvas.create_line(hxg.web1,  dash=(4, 2), fill="black")
        canvas.create_line(hxg.web2,  dash=(4, 2), fill="black")
        canvas.create_line(hxg.web3,  dash=(4, 2), fill="black")
        canvas.create_line(hxg.web4,  dash=(4, 2), fill="black")
        canvas.create_line(hxg.web5,  dash=(4, 2), fill="black")
        canvas.create_line(hxg.web6,  dash=(4, 2), fill="black")
        canvas.create_line(hxg.edg1,  dash=(4, 2), fill="black")
        canvas.create_line(hxg.edg2,  dash=(4, 2), fill="black")
        canvas.create_line(hxg.edg3,  dash=(4, 2), fill="black")
        canvas.create_line(hxg.edg4,  dash=(4, 2), fill="black")
        canvas.create_line(hxg.edg5,  dash=(4, 2), fill="black")
        canvas.create_line(hxg.edg6,  dash=(4, 2), fill="black")
        
        ### Place labels at the tips of three base "spokes"
        canvas.create_text(hxg.l1_pos[2], hxg.l1_pos[3], fill=hxg.l1_clr, 
                           font="Times 12 bold",text="A")
        canvas.create_text(hxg.l2_pos[2], hxg.l2_pos[3], fill=hxg.l2_clr, 
                           font="Times 12 bold",text="B")
        canvas.create_text(hxg.l3_pos[2], hxg.l3_pos[3], fill=hxg.l3_clr, 
                           font="Times 12 bold",text="C")
        
        ##########################################
        ### DRAW Operational quadrant diagram
        ##########################################
        
        ### Drwaw quadrant labels
        canvas.create_text(ori_C[2] +70, ori_C[3] -70,fill="black", 
                           font="Times 16",text="I")    
        canvas.create_text(ori_C[2] -70, ori_C[3] -70,fill="black", 
                           font="Times 16",text="IV")    
        canvas.create_text(ori_C[2] -70, ori_C[3] +70,fill="black", 
                           font="Times 16",text="III")    
        canvas.create_text(ori_C[2] +70, ori_C[3] +70,fill="black", 
                           font="Times 16",text="II") 
        
        ### Quadrant frame
        canvas.create_rectangle(trw.rect, dash=(4, 2), outline="black",)
        
        ### Axis labels
        canvas.create_line(trw.line_H, arrow = LAST, dash=(4, 2), fill="black")
        canvas.create_line(trw.line_V, arrow = LAST, dash=(4, 2), fill="black")
        
        
        canvas.create_text(trw.line_V[2], trw.line_V[3] - 15, 
                           font="Times 12 bold",text="T_el", fill="purple")
        canvas.create_text(trw.line_H[2] + 15, trw.line_H[3], 
                           font="Times 12 bold", text="\u03c9_r", fill="green")        
        
        
        
        canvas.create_line(trw.T_ld, dash=(4, 2), fill="purple", width=2)
        canvas.create_line(trw.w_r_, dash=(4, 2), fill="green", width=2)
        canvas.create_text(ori_C[2]- 50, trw.T_ld[3] - 10, 
                           font="Times 12 ",text="T_load", fill="purple")
        canvas.create_text(trw.w_r_[2]+ 17, ori_C[3] + 50, 
                           font="Times 12",text="\u03c9_r*", fill="green")
        
        
        ### Actual "Vector" and projections
        canvas.create_line(trw.act, arrow = LAST, width=2, fill="black") 

        canvas.create_line(trw.pr_T_el, dash=(4, 2), fill="purple", width=2)
        canvas.create_line(trw.pr_w_r, dash=(4, 2), fill="green", width=2)
        
        ###############################
        ### Finalize mainloop
        ###############################
        
        ### Print something to the console

        #print (max_speed)
        print (tp)
        #print (sheet.loc[tp,0]) # Print spreadsheet cell at timepoint
        #print (vec.u_s) #Print the coordinates of u_s space vector
        print (hxg.comb)       
        
        ### Refresh GUI
        root.update()
        time.sleep(0.001)
        canvas.delete("all")  

##############################################
###
###     MAINLOOP DEFINITION END
###
##############################################        



##############################################
###
###     CLASS AND FUNCTION DEFINITIONS BEGIN
###
##############################################  

#########################################
### Link variables to spreadsheet columns
#########################################

class ReadRow: ## ENTER COLUMN NR \/ HERE
    def __init__(self, tp):
        self.u_sd = sheet.loc[tp, 5]
        self.u_sq = sheet.loc[tp, 6]
        
        self.i_sd = sheet.loc[tp, 3]
        self.i_sq = sheet.loc[tp, 4]
        
        self.i_sd_ = sheet.loc[tp, 1]
        self.i_sq_ = sheet.loc[tp, 2]
        
        self.i_mr = sheet.loc[tp, 8]  
        
        self.w_r_ = sheet.loc[tp, 9]
        self.w_r  = sheet.loc[tp, 10]
        
        self.T_el = sheet.loc[tp, 11]
        self.T_ld = sheet.loc[tp, 12]
        
        self.theta = sheet.loc[tp, 13]
        
        self.hb1 = sheet.loc[tp, 17]
        self.hb2 = sheet.loc[tp, 18]
        self.hb3 = sheet.loc[tp, 19]   
        

#######################################################    
### DESIGN Space Vector Diagram
#######################################################    

class VectorBuild: 
    def __init__(self, val, ori_A):  
        A = ori_A
        raxis = 180 # "Radius" of dq axis
        
        ### Build dq axis
        self.daxis = (A[2] -raxis, A[3], A[2] + raxis, A[3])
        self.qaxis = (A[2], A[3] +raxis, A[2], A[3] -raxis)
        
        
        ### Place Voltage and Current space vectors        
        self.u_s = OriScale(val.u_sd, val.u_sq, A, sc_u)   
        self.i_s = OriScale(val.i_sd, val.i_sq, A, sc_i)  
        self.i_s_ = OriScale(val.i_sd_, val.i_sq_, A, sc_i)
        self.i_mr = OriScale(val.i_mr, 0, A, sc_i)
        

'''       
        self.i_mr_abs = sheet.loc[tp, c_i_mr]
        self.i_mrq = math.sqrt(self.i_mr_abs^2 - sheet.loc[tp, c_i_sd]^2)
        self.i_mr = (A[2], A[3], 
                     A[2]+sheet.loc[tp, c_i_sd]*sc_i, 
                     A[3]-self.i_mrq*sc_i)
'''        

###########################
### DESIGN rotating hexagon 
###########################    
class Hexagon: 
    def __init__(self, val, ori_B):
        B = ori_B
        
        ### Inverter output phase states
        hb1 = val.hb1
        hb2 = val.hb2
        hb3 = val.hb3
        
        ### Rotation adjustment
        offset = -pi/2 # Offset to align to Space vector diagram
        theta = -val.theta + offset # Instantaneous rotation angle
        dire = 1 # Direction of rotation: +1 or -1
        
        ### Calculation of rotating corners
        h0dq = (0, 0)
        h1dq = (math.cos((theta + 0*pi/3)*dire), math.sin((theta + 0*pi/3)*dire))
        h2dq = (math.cos((theta + 1*pi/3)*dire), math.sin((theta + 1*pi/3)*dire))
        h3dq = (math.cos((theta + 2*pi/3)*dire), math.sin((theta + 2*pi/3)*dire))
        h4dq = (math.cos((theta + 3*pi/3)*dire), math.sin((theta + 3*pi/3)*dire))
        h5dq = (math.cos((theta + 4*pi/3)*dire), math.sin((theta + 4*pi/3)*dire))
        h6dq = (math.cos((theta + 5*pi/3)*dire), math.sin((theta + 5*pi/3)*dire))
        
        ### Choose which one of the "spokes" carries the resulting voltage vector
        if   hb1==0 and hb2==0 and hb3==0: comb = h0dq
        elif hb1==0 and hb2==1 and hb3==1: comb = h1dq
        elif hb1==0 and hb2==0 and hb3==1: comb = h2dq
        elif hb1==1 and hb2==0 and hb3==1: comb = h3dq
        elif hb1==1 and hb2==0 and hb3==0: comb = h4dq
        elif hb1==1 and hb2==1 and hb3==0: comb = h5dq
        elif hb1==0 and hb2==1 and hb3==0: comb = h6dq
        elif hb1==1 and hb2==1 and hb3==1: comb = h0dq
        else: comb = 'error'
        self.comb = comb
        
        ### Build resulting voltage vector
        self.act = OriScale(comb[0], comb[1], B, sc_h)
        
        ### Build Radial hexagon lines - dashed
        self.web1 = OriScale(h1dq[0], h1dq[1], B, sc_h)
        self.web2 = OriScale(h2dq[0], h2dq[1], B, sc_h)
        self.web3 = OriScale(h3dq[0], h3dq[1], B, sc_h)
        self.web4 = OriScale(h4dq[0], h4dq[1], B, sc_h)
        self.web5 = OriScale(h5dq[0], h5dq[1], B, sc_h)
        self.web6 = OriScale(h6dq[0], h6dq[1], B, sc_h)
        
        ### Label positions
        self.l1_pos = OriScale(h1dq[0], h1dq[1], B, sc_h*1.1)
        self.l2_pos = OriScale(h3dq[0], h3dq[1], B, sc_h*1.1)
        self.l3_pos = OriScale(h5dq[0], h5dq[1], B, sc_h*1.1)
        
        ### Label texts and colors
        if hb1 == 1: self.l1_clr = "red"
        else: self.l1_clr = "black"
        if hb2 == 1: self.l2_clr = "red"
        else: self.l2_clr = "black"
        if hb3 == 1: self.l3_clr = "red"
        else: self.l3_clr = "black"
                
        ### Build Hexagon edges - dashed
        self.edg1 = (self.web1[2], self.web1[3], self.web2[2], self.web2[3])
        self.edg2 = (self.web2[2], self.web2[3], self.web3[2], self.web3[3])
        self.edg3 = (self.web3[2], self.web3[3], self.web4[2], self.web4[3])
        self.edg4 = (self.web4[2], self.web4[3], self.web5[2], self.web5[3])
        self.edg5 = (self.web5[2], self.web5[3], self.web6[2], self.web6[3])
        self.edg6 = (self.web6[2], self.web6[3], self.web1[2], self.web1[3])

#########################################  
### DESIGN Operational quadrant diagram
#########################################
class TorqueSpeed:
    def __init__(self, val, ori_C):
        C = ori_C
        
        ### Draw quadrant frame
        self.line_H = (C[2]-C_H, C[3], C[2]+C_H*1.3, C[3])
        self.line_V = (C[2], C[3]+C_V*1.3, C[2], C[3]-C_V*1.3)
        self.rect = (C[2]-C_H, C[3]-C_V, C[2]+C_H, C[3]+C_V)
        
        ### Draw load torque and reference rotor speed as levels
        self.T_ld = (C[2]-C_H, C[3]-val.T_ld*sc_T, C[2]+C_H, C[3]-val.T_ld*sc_T)
        self.w_r_ = (C[2]+val.w_r_*sc_w, C[3]-C_V, C[2]+val.w_r_*sc_w, C[3]+C_V)
        
        
        ### Draw actual "vector" pointing to the operational state
        self.act = OriScale(val.w_r*sc_w, val.T_el*sc_T, C, 1)
        
        ### Draw the vector's projections towards axis
        self.pr_T_el = (C[2], C[3] - val.T_el*sc_T, 
                        C[2] + val.w_r*sc_w, C[3] - val.T_el*sc_T)
        self.pr_w_r =  (C[2] + val.w_r*sc_w, C[3], 
                        C[2] + val.w_r*sc_w, C[3] - val.T_el*sc_T)

    
    
    
###########################
### Function definitions 
########################### 

### For placing a vector at a given origin and scale.
def OriScale(x, y, origin, scale):
    return(
        origin[2],
        origin[3],
        origin[2] + x * scale,
        origin[3] - y * scale,
        )

### For drawing a crosshair (target) instead of the reference vector.
### This enhances the distinguishability of the two vectors.
def DrawCrosshair(x, y, tie, radius, width, color):
    hw = width/2
    # This accounts for changing directions
    top = min (y-hw, tie)
    bottom = max (y+hw, tie)
    canvas.create_line(x-hw, y, x+hw, y,  
                       dash=(4, 2), fill=color) #horizontal crosshair
    canvas.create_line(x, top, x, bottom,  
                       dash=(4, 2), fill=color) #vertical crosshair
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius,  
                       dash=(4, 2), outline=color) #circle
    
##############################################
###
###     CLASS AND FUNCTION DEFINITIONS END
###
##############################################  


        
###########################
### Run Mainloop
###########################
    
main()







































