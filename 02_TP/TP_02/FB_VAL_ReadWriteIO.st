FUNCTION_BLOCK VAL_ReadWriteIO
    (* Update the digital outputs of the controller with values passed as parameter.
    Return the state of the digital inputs available on the controller *)
    VAR_INPUT
        Enable : BOOL ; (*function block content is executed as long as this input is TRUE *)
        Valve1 : BOOL ; (* 6 axis robot only : the internal valve *)
        Valve2 : BOOL ; (* 6 axis robot only : the internal valve *)
        Fout0 : BOOL ; (* Command Fast output (J212-4 / J212-9) CS9 controller *)
        Fout1 : BOOL ; (* Command Fast output (J212-1 / J212-5) CS9 controller *)
        EnableValve1 : BOOL ; (* 6 axis robot only : the internal valve 5-3 closed middle *)
        EnableValve2 : BOOL ; (* 6 axis robot only : the internal valve 5-3 closed middle *)
    END_VAR
    VAR_IN_OUT
        AxesGroup : T_StaeubliRobot; (* Data block for a robot *)
    END_VAR
    VAR_OUTPUT
        Valid : BOOL ; (*Set when function block is executing. Reset when Done or Error*)
        UsrInput0 : BOOL ; (* Digital input (J109-11 / J109-30) CS8 controller *)
        UsrInput1 : BOOL ; (* Digital input (J109-16 / J109-35) CS8 controller *)
        Fin0 : BOOL ; (* Fast input (J111-2/7) CS8 controller, J212-2/7 CS9 controller *)
        Fin1 : BOOL ; (* Fast input (J111-3/8) CS8 controller, J212-3/8 CS9 controller *)
        ValvesSafeState : BOOL ; (* CS9 controlling 5-3 ways valves ONLY *)
    END_VAR